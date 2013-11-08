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

import supybot.conf as conf
import supybot.registry as registry

def configure(advanced):
    # This will be called by supybot to configure this module.  advanced is
    # a bool that specifies whether the user identified himself as an advanced
    # user or not.  You should effect your configuration by manipulating the
    # registry as appropriate.
    from supybot.questions import expect, anything, something, yn
    conf.registerPlugin('Jira', True)
    user = something('What is your api username?')
    password = something('What is your password for that username?')
    api_url = something('What is your api url (eg. https://jira.com/api/v2)?')
    url = something('What is your domain (eg. https://jira.com)?')

    conf.supybot.plugins.Jira.apiUser.setValue(user)
    conf.supybot.plugins.Jira.apiPass.setValue(password)
    conf.supybot.plugins.Jira.apiUrl.setValue(api_url)
    conf.supybot.plugins.Jira.domain.setValue(url)


Jira = conf.registerPlugin('Jira')
# This is where your configuration variables (if any) should go.  For example:
# conf.registerGlobalValue(Jira, 'someConfigVariableName',
#     registry.Boolean(False, """Help for someConfigVariableName."""))
conf.registerGlobalValue(Jira, 'apiUser',
    registry.String('', """Defines the username used to access the API."""))
conf.registerGlobalValue(Jira, 'apiPass',
    registry.String('', """Defines the password used to access the API."""))
conf.registerGlobalValue(Jira, 'apiUrl',
    registry.String('', """Defines the full base api url to access the API.
    (eg. https://<instance>.Jira.com/api/v2)"""))
conf.registerGlobalValue(Jira, 'domain',
    registry.String('', """Defines the url to access.
    (eg. https://jira.com)"""))


# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
