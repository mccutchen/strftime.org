#!/usr/bin/env python

import datetime
import sys
import urllib2

from bs4 import BeautifulSoup
import pystache


def main():
    url = 'http://docs.python.org/2/library/datetime.html'
    body = urllib2.urlopen(url).read()
    soup = BeautifulSoup(body)

    table = soup.find(id='strftime-and-strptime-behavior').find('table')
    example_date = datetime.datetime(2013, 9, 30, 7, 6, 5)

    directives = []
    for row in table.select('tbody > tr'):
        tds = row.find_all('td')
        directive = tds[0].find('span').string
        # we use getText() here because some of the meanings have extra markup
        meaning = tds[1].getText().replace('\n', ' ')
        example = example_date.strftime(directive)
        directives.append({
            'directive': directive,
            'meaning': meaning,
            'example': example
        })

        # also add the non zero padded version for some of them
        # http://stackoverflow.com/questions/28894172/why-does-d-or-e-remove-the-leading-space-or-zero

        exclude = ['%f', '%y']
        if 'zero-padded' in meaning and directive not in exclude:
            non_zero_padding_decimal = directive.replace("%", "%-")
            non_zero_padding_example = example_date.strftime(
                non_zero_padding_decimal
            )

            non_zero_padding_meaning = (
                meaning.replace("zero-padded", "") + " (Platform specific)")

            directives.append({
                'directive': non_zero_padding_decimal,
                'meaning': non_zero_padding_meaning,
                'example': non_zero_padding_example
            })

    template = open('templates/index.html.mustache').read()
    context = {
        'example_date': str(example_date),
        'example_date_repr': repr(example_date),
        'directives': directives,
        'timestamp': datetime.datetime.utcnow().strftime('%Y-%m-%d'),
    }
    print pystache.render(template, context).encode('utf8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
