# zonefile

Use this script when you need to create a zonefile, mostly for bind, but have
no access to the original zonefile and can't use AXFR transfers.

## Installation

### Pure python

``` sh
virtualenv -p /usr/bin/python3 env
env/bin/pip install -r requirements.txt
env/bin/python3 zonefile.py <domain>
```

Note: If you go for the pure python way, you will either have to call this
every time with the env/bin/python3 interpreter or you must active the
virtualenv which will set your PATH accordingly. Then you can call it simly
with `./zonefile.py`.

### Debian

``` sh
apt-get install python3-dnspython
./zonefile.py <domain>
```

### Configuration

Edit `config.py` to match your needs. You will most likely want to change the
`ZONE_TPL` to reflect your SOA and NS entries.

If you expect interesting other subdomains which should be scanned, just add
them to the list of `DEFAULT_SUBDOMAINS`.

The `DEFAULT_SUBSUBDOMAINS` will be prepended to any existing subdomain, so
for example the `_domainkey` subsubdomain will be tried as
`_domainkey.sub.domain.com`. Just extend that list to your needs.

Finally, the `LINE_TPL` creates a nicely formatted list of entries for all the
found subdomains and domain-entries (which will start with '@').

## Usage

Use the help:

``` sh
env/bin/python3 zonefile.py -h
usage: zonefile.py [-h] [--subdomain SUBDOMAIN] [--quiet] domain

Get domain information as zonefile.

positional arguments:
  domain                The domain to lookup

optional arguments:
  -h, --help            show this help message and exit
  --subdomain SUBDOMAIN, -s SUBDOMAIN
  --quiet, -q           Do not write commented out entries with lookup
                        failures
```

So if you simply run it, you will get output like this (Note: this will take a
few seconds):

``` sh
./zonefile.py d9t.de
; d9t.de
$TTL 3600               ; Default TTL in secs(1 hour)
@       SOA ns1.d9t.de. domainmaster.d9t.de. (
        2017030801      ; Serial number yyyymmddvv
        10800           ; Refresh  (3, was 8 hours)
        3600            ; Retry (1, was 2 hours)
        604800          ; Expire (7 days)
        3600            ; 
)

@                    NS         ns1.d9t.de.
@                    NS         ns2.d9t.de.


@                    IN A       94.186.147.152
@                    IN MX      10 mail.d9t.de.
@                    IN AAAA    2a02:c98:ffff:f100::2
www                  IN A       94.186.147.152
www                  IN AAAA    2a02:c98:ffff:f100::2
mail                 IN A       94.186.148.130
_jabber._tcp         IN SRV     0 0 5222 xmpp.trusted.b.d9tcloud.de.
_xmpp-client._tcp    IN SRV     0 0 5222 xmpp.trusted.b.d9tcloud.de.
static               IN CNAME   d1.pool.b.d9tcloud.de.
```

The serial number will be the current date with an appended '01'. Always.

In case there is a `SERVFAIL` from one of the dns queries, this query will be
shown by default in the resulting zonefile like this:

```
;aws                 IN CNAME   UNABLE TO RESOLVE
```

This is a commented-out section. Some resolver libs tend to give `SERVFAIL` even
when there's just a `NXDOMAIN`. For this reason, you can use the `-q` parameter
which silences these `UNABLE TO RESOLVE` entries:

``` sh
./zonefile.py d9t.de -q
```

### pro usage

``` sh
for domain in domaina.com domainb.com domainc.com; do ./zonefile.py $domain > db.$domain; done
```

