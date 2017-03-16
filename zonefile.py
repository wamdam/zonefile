#!/usr/bin/env python3
import argparse
import datetime
import dns.resolver
import dns.name
from config import DEFAULT_LABELS, DEFAULT_2NDLABELS, ZONE_TPL, LINE_TPL


def get_resolver(domain):
    nameservers = []
    _a_ns = dns.resolver.query(domain, 'NS')
    for _a in _a_ns:
        _a_ns_ips = dns.resolver.query(_a.to_text(), 'A')
        for _a_ip in _a_ns_ips:
            nameservers.append(_a_ip.to_text())

    # create a resolver that resolves only against the currently entered nameservers
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = nameservers
    return resolver


def get_domain_data(resolver, domain, dont_check_these_rrtypes=None):
    # this gets for exactly this domain all available data
    # by asking the responsible nameserver for ANY.
    #
    # Params:
    #   resolver: a dns.resolver.Resolver instance
    #   domain: The domain to resolve
    #   dont_check_these_rrtypes: a set / list of rrtypes which should not be checked
    # Returns a list of LINE_TPLs filled with the found data.

    if not dont_check_these_rrtypes:
        dont_check_these_rrtypes = set()
    answers = []
    candidates = []  # new subdomain candidates
    _domain = dns.name.from_text(domain)
    zone_name = _domain.split(3)[0].to_text()  # mail.d9t.de -> mail, d9t.de -> @, ...
    _super_domain = _domain.split(3)[1]        # **.d9t.de -> d9t.de
    if _super_domain == _domain:
        rrq = ('A', 'MX', 'AAAA', 'DNSKEY', 'RRSIG', 'TXT', 'SRV')
    else:
        rrq = ('CNAME', 'NS', 'A', 'MX', 'AAAA', 'DNSKEY', 'RRSIG', 'TXT', 'SRV')
    for rrtype in rrq:
        if rrtype in dont_check_these_rrtypes or 'CNAME' in dont_check_these_rrtypes or 'NS' in dont_check_these_rrtypes:
            continue
        try:
            _answer = resolver.query(domain, rrtype)
        except dns.resolver.NoAnswer:
            continue
        except dns.resolver.NXDOMAIN:
            continue
        except dns.resolver.NoNameservers:
            # This is a servfail most likely
            # Add a notification into the answers that there's a problem
            answers.append({
                'name': ';' + zone_name,
                'type': rrtype,
                'data': 'UNABLE TO RESOLVE',
                'success': False,
                })
            #break
            continue
        for _a in _answer:
            answers.append({
                'name': zone_name,
                'type': rrtype,
                'data': _a.to_text(),
                'success': True,
                })
            # if MX or CNAME contains own domain, add to list!
            if rrtype == 'MX' and _a.exchange.is_subdomain(_super_domain) and _a.exchange != _super_domain:
                candidates.append(_a.exchange.split(3)[0].to_text())  # mail
            if rrtype == 'CNAME' and _a.target.is_subdomain(_super_domain) and _a.target != _super_domain:
                candidates.append(_a.target.split(3)[0].to_text())    # server

        # When a subdomain has a NS, stop, because there are no other entries allowed.
        if rrtype == 'NS':  # TODO: This breaks on my nameserver
            break
        # When a domain has a cname, stop, because there are no other entries allowed.
        if rrtype == 'CNAME':
            break
    return candidates, answers


def format_answers(answers, quiet=False):
    lines = []
    for answer in answers:
        if quiet and not answer['success']:
            continue
        lines.append(LINE_TPL.format(**answer))
    return '\n'.join(lines) + '\n\n'


def resolve(domain, subdomains):
    resolver = get_resolver(domain)

    candidates = []
    answers = []
    wildcard_rrtypes = set()

    _candidates, _answers = get_domain_data(resolver, domain)
    candidates.extend(_candidates)
    answers.extend(_answers)

    # TODO: refacture, this is duplicate code

    # see if there is a wildcard entry (in depth 1)
    WILDCARD_TEST_SUBDOMAIN = 'thisdoesn0texisthaha'
    _candidates, _answers = get_domain_data(resolver, WILDCARD_TEST_SUBDOMAIN+'.'+domain)
    candidates.extend(_candidates)
    if _answers and any([a['success'] for a in _answers]):
        for _answer in _answers:  # check for all rrtypes which are wildcard
            if not _answer['success']:
                continue
            _answer['name'] = '*'
            answers.append(_answer)
            wildcard_rrtypes.add(_answer['type'])  # = which rrtypes are wildcard in depth 1

    # check subdomains
    for subdomain in subdomains:
        _candidates, _answers = get_domain_data(resolver, subdomain+'.'+domain, wildcard_rrtypes)
        candidates.extend(_candidates)
        answers.extend(_answers)

        if _answers and any([a['success'] for a in _answers]):
            # also generated entries
            for subsub in DEFAULT_2NDLABELS:
                _candidates, _answers = get_domain_data(resolver, subsub+'.'+subdomain+'.'+domain)
                candidates.extend(_candidates)
                answers.extend(_answers)

    # check the subdomains which came back from previous queries as candidates,
    # like an mx entry
    for subdomain in candidates:
        if subdomain not in subdomains:
            _candidates, _answers = get_domain_data(resolver, subdomain+'.'+domain)
            candidates.extend(_candidates)
            answers.extend(_answers)

            if _answers and any([a['success'] for a in _answers]):
                # also generated entries
                for subsub in DEFAULT_2NDLABELS:
                    _candidates, _answers = get_domain_data(resolver, subsub+'.'+subdomain+'.'+domain)
                    candidates.extend(_candidates)
                    answers.extend(_answers)

    return answers


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get domain information as zonefile.')
    parser.add_argument('domain', help='The domain to lookup')
    parser.add_argument('--subdomain', '-s', action='append')
    parser.add_argument('--quiet', '-q', help='Do not write commented out entries with lookup failures', action='store_true')
    args = parser.parse_args()

    subdomain = args.subdomain if args.subdomain else DEFAULT_LABELS

    data = resolve(args.domain, subdomain)

    print(ZONE_TPL.format(
        domainname=args.domain,
        serial=datetime.datetime.now().strftime('%Y%m%d01'),
        ))
    print(format_answers(data, args.quiet))
