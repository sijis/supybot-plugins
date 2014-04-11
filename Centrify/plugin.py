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

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks

import os
import subprocess

class Centrify(callbacks.Plugin):
    """Add the help for "@plugin help Centrify" here
    This should describe *how* to use this plugin."""
    threaded = True
    adquerycmd = ['/usr/bin/adquery']

    def _query_ad(self, method, query):
        '''
        method = user|group
        query  = list of params
        '''

        lcmd = list(self.adquerycmd)
        lcmd.append(method)

        if type(query) == list:
            lcmd.extend(query)
        else:
            lcmd.append(query)

        inst = subprocess.Popen(lcmd, close_fds=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=file(os.devnull))

        (stdout, stderr) = inst.communicate()
        return (stdout, stderr)


    def aduser(self, irc, msg, args, username):
        (out, error) = self._query_ad('user', username)
        (groups_in, groups_err) = self._query_ad('user', ['-G', username])
        try:
            response = out.split(':')
            groups = groups_in.replace('\n', ', ').rstrip(', ')
            results = ( 'User: {0}, '
                        'Name: {1}, '
                        'Uid: {2}, '
                        'Groups: {3}'
                        ).format(
                            username,
                            response[4],
                            response[3],
                            groups
                        )
        except IndexError:
            results = 'User "{0}" not found.'.format(username)

        irc.reply(results)
    aduser = wrap(aduser, ['somethingWithoutSpaces'])

    def adgroup(self, irc, msg, args, group):

        (out, error) = self._query_ad('group', group)
        try:
            response = out.split(':')
            members = response[3].replace(',', ', ').rstrip('\n')
            results = ( 'Group: {0}, '
                        'Gid: {1}, '
                        'Members: {2}'
                        ).format(
                            group,
                            response[2],
                            members
                        )
        except IndexError:
            results = 'Group "{0}" not found.'.format(group)

        irc.reply(results)
    adgroup = wrap(adgroup, ['somethingWithoutSpaces'])

Class = Centrify


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
