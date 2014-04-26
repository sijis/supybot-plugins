###
# Copyright (c) 2014, Sijis Aviles
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import supybot.log as log
import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks

from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect
import time
import datetime
import random

vmutils = utils.python.universalImport('local.vmutils')

class VMware(callbacks.Plugin):
    """Add the help for "@plugin help VMware" here
    This should describe *how* to use this plugin."""
    threaded = True


    def __init__(self, irc):
        self.__parent = super(VMware, self)
        self.__parent.__init__(irc)
        self.user = self.registryValue('user')
        self.password = self.registryValue('password')
        self.template = self.registryValue('template')
        self.vcenter = self.registryValue('vcenter')
        self.pool = self.registryValue('resource_pool')
        self.vm_username = self.registryValue('vm_username')
        self.vm_password = self.registryValue('vm_password')
        self.vm_dnsdomain = self.registryValue('vm_dnsdomain')

    def migrate(self, irc, msg, args, vmname, hostname):

        username = self.user
        password = self.password
        vcenter = self.vcenter

        try:
            si = SmartConnect(host=vcenter, user=username, pwd=password, port=443)
        except:
            err_text = 'Error connecting to {0}'.format(vcenter)
            log.info(err_text)
            irc.reply(err_text)
            return

        if hostname:
            try:
                host = vmutils.get_host_by_name(si, hostname)
                hostname = host.name
            except:
                irc.reply('{0} not found'.format(hostname))
                return
        else:
            # hostname was not passed
            all_hosts = vmutils.get_hosts(si)
            host = vmutils.get_host_by_name(si, random.choice(all_hosts.values()))
            hostname = host.name

        # Finding source VM
        try:
            vm = vmutils.get_vm_by_name(si, vmname)
        except:
            irc.reply('{0} not found.'.format(vmname))
            return

        # relocate spec, to migrate to another host
        # this can do other things, like storage and resource pool
        # migrations
        relocate_spec = vim.vm.RelocateSpec(host=host)

        # does the actual migration to host
        vm.Relocate(relocate_spec)
        irc.reply('Migrating {0} to {1}'.format(vmname, hostname))

        Disconnect(si)
    migrate = wrap(migrate, ['somethingWithoutSpaces', optional('somethingWithoutSpaces')])

    def reboot(self, irc, msg, args, vmname):

        username = self.user
        password = self.password
        vcenter = self.vcenter

        try:
            si = SmartConnect(host=vcenter, user=username, pwd=password, port=443)
        except:
            err_text = 'Error connecting to {0}'.format(vcenter)
            log.info(err_text)
            irc.reply(err_text)
            return

        # Finding source VM
        try:
            vm = vmutils.get_vm_by_name(si, vmname)
        except:
            irc.reply('{0} not found.'.format(vmname))
            return

        try:
            vm.RebootGuest()
        except:
            vm.ResetVM_Task()

        irc.reply('Rebooting {0}'.format(vmname))
        Disconnect(si)
    reboot = wrap(reboot, ['somethingWithoutSpaces'])

    def clone(self, irc, msg, args, optlist, vmname):

        opts = dict(optlist)

        conf = {}
        conf['mem'] = opts.get('mem', 1024)
        conf['cpu'] = opts.get('cpu', 1)
        conf['tmpl'] = opts.get('tmpl', self.template)
        conf['pool'] = opts.get('pool', self.pool)
        conf['dnsdomain'] = opts.get('dnsdomain', self.vm_dnsdomain)
        conf['vcenter'] = opts.get('vcenter', self.vcenter)
        conf['name'] = vmname.lower()

        username = self.user
        password = self.password
        vm_username = self.vm_username
        vm_password = self.vm_password

        try:
            si = SmartConnect(host=conf['vcenter'], user=username, pwd=password, port=443)
        except IOError, e:
            log.info('Error connecting to {0}'.format(conf['vcenter']))
            return

        # Finding source VM
        template_vm = vmutils.get_vm_by_name(si, conf['tmpl'])

        # mem / cpu
        vmconf = vim.vm.ConfigSpec(numCPUs=conf['cpu'], memoryMB=conf['mem'],
                                   annotation='Created by {0} on {1}'.format(msg.nick, str(datetime.datetime.now())))

        # Network adapter settings
        adaptermap = vim.vm.customization.AdapterMapping()
        adaptermap.adapter = vim.vm.customization.IPSettings(ip=vim.vm.customization.DhcpIpGenerator(),
                                                             dnsDomain=conf['dnsdomain'])

        # IP
        globalip = vim.vm.customization.GlobalIPSettings()

        # Hostname settings
        ident = vim.vm.customization.LinuxPrep(domain=conf['dnsdomain'],
                                               hostName=vim.vm.customization.FixedName(name=conf['name']))

        # Putting all these pieces together in a custom spec
        customspec = vim.vm.customization.Specification(nicSettingMap=[adaptermap],
                                                        globalIPSettings=globalip,
                                                        identity=ident)

        # Creating relocate spec and clone spec
        resource_pool = vmutils.get_resource_pool(si, conf['pool'])
        relocateSpec = vim.vm.RelocateSpec(pool=resource_pool)
        cloneSpec = vim.vm.CloneSpec(powerOn=True, template=False,
                                     location=relocateSpec,
                                     customization=customspec,
                                     config=vmconf)

        # Creating clone task
        clone = template_vm.Clone(name=conf['name'],
                                  folder=template_vm.parent,
                                  spec=cloneSpec)

        irc.reply('{0}: Cloning in progress'.format(conf['name']))

        # Checking clone progress
        time.sleep(5)
        while True:
            progress = clone.info.progress
            if progress == None:
                break
            time.sleep(2)
        irc.reply('{0}: Cloning is done'.format(conf['name']))

        # let's get clone vm info
        vm_clone = vmutils.get_vm_by_name(si, conf['name'])

        vmutils.is_ready(vm_clone)

        # Credentials used to login to the guest system
        creds = vmutils.login_in_guest(username=vm_username, password=vm_password)

        irc.reply('{0}: Running post setup'.format(conf['name']))
        vmutils.start_process(si=si, vm=vm_clone, auth=creds, program_path='/bin/touch',
                            args='/tmp/sample.txt')


        irc.reply('{0}: Request completed'.format(conf['name']))
        Disconnect(si)

    clone = wrap(clone, [getopts({
                                'mem':'int',
                                'cpu':'int',
                                'tmpl':'somethingWithoutSpaces',
                                'pool':'somethingWithoutSpaces',
                                'dnsdomain':'somethingWithoutSpaces',
                                'vcenter':'somethingWithoutSpaces',
                                }), 'somethingWithoutSpaces'])

Class = VMware

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
