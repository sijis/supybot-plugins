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

import pepper
import json
import urllib
import urllib2

class Salt(callbacks.Plugin):
    """Add the help for "@plugin help Salt" here
    This should describe *how* to use this plugin."""
    threaded = True

    def __init__(self, irc):
        self.__parent = super(Salt, self)
        self.__parent.__init__(irc)
        self.api_url = self.registryValue('api_url')
        self.api_user = self.registryValue('api_user')
        self.api_password = self.registryValue('api_password')
        self.api_eauth = self.registryValue('api_eauth')
        self.paste_api_url = self.registryValue('paste_api_url')

    def paste_code(self, code):
        ''' Post the output to pastebin '''
        request = urllib2.Request(
            self.paste_api_url,
            urllib.urlencode([('content', code)]),
        )
        response = urllib2.urlopen(request)
        return response.read()[1:-1]


    def pepper(self, irc, msg, args, systems, action, params):
        """{vm-name | vm-glob} <module> [<params>]
        Example: .pepper dil-vm-app-*.* cmd.rum 'cat /etc/hosts'

        Returns the link to pastebin of the pepper output
        """

        tgt, fun = systems, action
        api = pepper.Pepper(self.api_url, debug_http=False)
        auth = api.login(self.api_user, self.api_password, self.api_eauth)
        ret = api.local(tgt, fun, arg=params, kwarg=None, expr_form='pcre')
        results = json.dumps(ret, sort_keys=True, indent=4)
        irc.reply(self.paste_code(results))
    pepper = wrap(pepper, ['somethingWithoutSpaces', 'somethingWithoutSpaces', optional('text')])


Class = Salt


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
