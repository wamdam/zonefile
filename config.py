#!/usr/bin/env python3

DEFAULT_LABELS = [
    'www',
    'mail',
    'autodiscover',
    'cm._domainkey',
    'news',
    'post',
    'owa',
    'gw',
    '_sip._tls',
    '_amazonses',
    '_jabber._tcp',
    '_sip._tls',
    '_sipfederationtls._tcp',
    '_xmpp-client._tcp',
    'aktion',
    'api',
    'aws',
    'blog',
    'chat',
    'de',
    'en',
    'fr',
    'edm',
    'email.mailgun',
    'static',
    'img',
    'images',
    'cdn',
    'lyncdiscover',
    'mailgun',
    'm',
    'mobil',
    'sharepoint',
    'sip',
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
