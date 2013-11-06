###
# Copyright (c) 2013, Sijis Aviles
# All rights reserved.
#
#
###

import supybot.conf as conf
import supybot.registry as registry

def configure(advanced):
    # This will be called by supybot to configure this module.  advanced is
    # a bool that specifies whether the user identified himself as an advanced
    # user or not.  You should effect your configuration by manipulating the
    # registry as appropriate.
    from supybot.questions import expect, anything, something, yn
    conf.registerPlugin('Zendesk', True)

    user = something('What is your api username?')
    password = something('What is your password for that username?')
    api_url = something('What is your api url (eg. https://<instance>.zendesk.com/api/v2)?')
    url = something('What is your domain (eg. https://<instance>.zendesk.com)?')

    conf.supybot.plugins.Zendesk.apiUser.setValue(user)
    conf.supybot.plugins.Zendesk.apiPass.setValue(password)
    conf.supybot.plugins.Zendesk.apiUrl.setValue(api_url)
    conf.supybot.plugins.Zendesk.domain.setValue(url)

Zendesk = conf.registerPlugin('Zendesk')
conf.registerGlobalValue(Zendesk, 'apiUser',
    registry.String('', """Defines the username used to access the API."""))
conf.registerGlobalValue(Zendesk, 'apiPass',
    registry.String('', """Defines the password used to access the API."""))
conf.registerGlobalValue(Zendesk, 'apiUrl',
    registry.String('', """Defines the full base api url to access the API.
    (eg. https://<instance>.zendesk.com/api/v2)"""))
conf.registerGlobalValue(Zendesk, 'domain',
    registry.String('', """Defines the url to access the website.
    (eg. https://<instance>.zendesk.com)"""))

# This is where your configuration variables (if any) should go.  For example:
# conf.registerGlobalValue(Zendesk, 'someConfigVariableName',
#     registry.Boolean(False, """Help for someConfigVariableName."""))


# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
