###
# Copyright (c) 2013, Sijis Aviles
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

import requests

class Jira(callbacks.Plugin):
    """Add the help for "@plugin help Jira" here
    This should describe *how* to use this plugin."""
    threaded = True

    def __init__(self, irc):
        self.__parent = super(Jira, self)
        self.__parent.__init__(irc)
        self.user = self.registryValue('apiUser')
        self.password = self.registryValue('apiPass')
        self.url = self.registryValue('apiUrl')
        self.domain = self.registryValue('domain')

    def jira(self, irc, msg, args, ticket):
        """<ticket>

        Returns the subject of the ticket along with a link to it.
        """

        url = '%s/issue/%s' % (self.url, ticket)
        url_display = '%s/browse/%s' % (self.domain, ticket)
        req = requests.get(url, auth=(self.user, self.password))
        data = req.json()

        irc.reply(str('%s created on %s by %s - %s' %
                (data['fields']['summary'], data['fields']['created'], data['fields']['reporter']['displayName'], url_display)))
    jira = wrap(jira, ['text'])

    def _get_name_by_id(self, id):
        url = '%s/users/%s.json' % (self.url, id)
        req = requests.get(url, auth=(self.user, self.password))
        data = req.json()
        return data['user']['name']


Class = Jira


# vim:set shiftwidth=4 softtabstop=4 expandtab:
