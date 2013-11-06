###
# Copyright (c) 2013, Sijis Aviles
# All rights reserved.
#
#
###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks

import requests

class Zendesk(callbacks.Plugin):
    """Add the help for "@plugin help Zendesk" here
    This should describe *how* to use this plugin."""
    threaded = True

    def __init__(self, irc):
        self.__parent = super(Zendesk, self)
        self.__parent.__init__(irc)
        self.user = self.registryValue('apiUser')
        self.password = self.registryValue('apiPass')
        self.url = self.registryValue('apiUrl')
        self.domain = self.registryValue('domain')
        
    def zendesk(self, irc, msg, args, id):
        """<id>

        Returns the subject of the ticket along with a link to it.
        """

        url = '%s/tickets/%s.json' % (self.url, id)
        display_url = '%s/tickets/%s' % (self.domain, id)
        req = requests.get(url, auth=(self.user, self.password))
        data = req.json()

        user = self._get_name_by_id(data['ticket']['assignee_id'])
        irc.reply(str('%s created on %s by %s - %s' % 
                (data['ticket']['subject'], data['ticket']['created_at'], user, display_url)))
    zendesk = wrap(zendesk, ['int'])

    def _get_name_by_id(self, id):
        url = '%s/users/%s.json' % (self.url, id)
        req = requests.get(url, auth=(self.user, self.password))
        data = req.json()
        return data['user']['name']

Class = Zendesk


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
