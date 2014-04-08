Supybot Plugins
================================

This contains a compilation of supybot plugins.

Jira
----

The plugin currently returns a summary of the ticket along with a link.

Usage:
```
.jira <project-code>-<number>
.jira BUG-253
```

Zendesk
-------

The plugin currently returns a summary of the ticket along with a link.

Usage:
```
.zendesk <ticket-number>
.zendesk 3512
```

Centrify
-------

The plugin currently returns a summary of a user or group from Active Directory

Usage:
```
.aduser <username>
.adgroup <groupname>
```

Notes: requires the centrify package being installed on the bot server and joined to
a domain
