#!/usr/bin/env python3

DEFAULT_LABELS = [
    '_amazonses',
    '_autodiscover._tcp',
    '_imap._tcp.privat',
    '_jabber._tcp',
    '_pop._tcp.privat',
    '_sip._tls',
    '_sipfederationtls._tcp',
    '_xmpp-client._tcp',
    'adsl',
    'aktion',
    'api',
    'autodiscover',
    'aws',
    'bewerbung',
    'blog',
    'bremskerl.no-ip-biz',
    'cdn',
    'chat',
    'china',
    'cloud',
    'cm._domainkey',
    'cms',
    'cms.bewerbung',
    'companyconnect',
    'confluence',
    'coza',
    'de',
    'edm',
    'email.mailgun',
    'en',
    'exchange',
    'files',
    'fr',
    'ftp',
    'gw',
    'icee',
    'images',
    'img',
    'international',
    'jira',
    'lyncdiscover',
    'm',
    'mail',
    'mailgun',
    'mobil',
    'mobile',
    'msoid',
    'news',
    'northernaccess',
    'notfall',
    'ns',
    'owa',
    'post',
    'privat',
    'rootserver',
    'sdsl',
    'seafile',
    'sentry',
    'sharepoint',
    'sip',
    'static',
    'survey',
    'teamdrive',
    'teamviewer',
    'uk',
    'voip',
    'vpn',
    'webmail',
    'www',
    'www.bewerbung',
    'www2',
    ]
DEFAULT_2NDLABELS = [
    's1024._domainkey',
    '_adsp._domainkey',
    '_domainkey',
    ]
ZONE_TPL = """; {domainname}
$TTL 3600               ; Default TTL in secs(1 hour)
@       SOA ns1.d9t.de. domainmaster.d9t.de. (
        {serial}      ; Serial number yyyymmddvv
        10800           ; Refresh  (3, was 8 hours)
        3600            ; Retry (1, was 2 hours)
        604800          ; Expire (7 days)
        3600            ; 
)

@                    NS         ns1.d9t.de.
@                    NS         ns2.d9t.de.

"""

LINE_TPL = """{name:<20} IN {type:<7} {data}"""
