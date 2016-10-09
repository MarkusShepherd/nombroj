# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals, with_statement

import argparse
import sys

from neo4j.v1 import GraphDatabase, basic_auth
from num2words import num2words

from spell import eo

driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "numbers"))

def gen_words(lang, max_number=10000):
    for n in range(max_number + 1):
        if lang == 'eo':
            yield eo(n)
        else:
            yield num2words(n, lang=lang)

def create_links(lang, words=None, max_number=None):
    if not lang:
        raise ValueError('no language provided')

    session = driver.session()

    if not words:
        words = gen_words(lang, max_number)

    for n1, word in enumerate(words):
        n2 = len(word.replace(' ', '').replace('-', '').replace(',', ''))
        cypher = '''
            MERGE (n1:Number {{value: {n1}}})
            MERGE (n2:Number {{value: {n2}}})
            CREATE UNIQUE (n1)-[e:LINK {{lang: '{lang}', word: '{word}'}}]->(n2)
            RETURN n1, e, n2;
        '''.format(
            n1=n1,
            n2=n2,
            lang=lang,
            word=word,
        )

        result = session.run(cypher)
        for record in result:
            print(record.values())

        if max_number and n1 >= max_number:
            break

    session.close()

def get_args():
    parser = argparse.ArgumentParser(description='description')
    parser.add_argument('-l', '--lang', required=True,
        help='target language')
    parser.add_argument('-f', '--file',
        help='file containing the words')
    parser.add_argument('-n', '--numbers', type=int, default=1000,
        help='numbers to be processed')
    parser.add_argument('-v', '--verbose', action='count', default=0,
        help='increase verbosity (specify multiple times for more)')

    return parser.parse_args()

def main():
    args = get_args()

    if args.file:
        with open(args.file, 'r') as f:
            words = filter(None, [word.strip() for word in f])
    else:
        words = None

    create_links(lang=args.lang, words=words, max_number=args.numbers)

if __name__ == '__main__':
    main()

'''
MATCH (n1:Number)
WHERE (n1)<-[:LINK {lang: 'eo'}]-(:Number)
OPTIONAL MATCH (n1)<-[e1:LINK {lang: 'eo'}]-(n2:Number)
WHERE (n2)<-[:LINK {lang: 'eo'}]-(:Number)
RETURN n1, e1, n2
'''
