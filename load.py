import sys
from spell import eo
from num2words import num2words
from neo4j.v1 import GraphDatabase, basic_auth

driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "numbers"))
session = driver.session()

def create_links(lang, max_number=10000):
    for n1 in range(max_number + 1):
        if lang == 'eo':
            word = eo(n1)
        else:
            word = num2words(n1, lang=lang)
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

    session.close()

def main():
    lang = sys.argv[1]
    max_number = int(sys.argv[2]) if len(sys.argv) > 2 else 10000
    create_links(lang, max_number)

if __name__ == '__main__':
    main()
