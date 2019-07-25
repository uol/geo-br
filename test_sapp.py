import unittest
import gzip
import json
import sys

import sapp

from types import SimpleNamespace

class TestSearchMethod(unittest.TestCase):
    def test_cities(self):
        print ("running test_cities...")
        with gzip.open('data.json.gz', 'rb') as db:
            cities = json.load(db)
        
        states = set()
        errors, count = 0, 0
        for city in cities:
            c = SimpleNamespace(**city)
            states.add(c.uf)
            r = sapp._search(c.latitude, c.longitude)
            if r is None:
                errors += 1
            else:
                if r["found"]:
                    if c.nome_municipio == r["city"] and c.uf == r["state"]:
                        count += 1
                    else:
                        errors += 1
                else:
                    errors += 1
        
        self.assertTrue(errors==0)
        self.assertTrue(count==5540)
        self.assertTrue(len(states)==27)

    def test_states(self):
        print ("running test_states...")
        with gzip.open('capitais.json.gz', 'rb') as db:
            all_br_states = json.load(db)

        with gzip.open('data.json.gz', 'rb') as db:
            cities = json.load(db)

        all_br_states = [x['sigla'] for x in all_br_states]
        all_states = [x['uf'] for x in cities if x['capital']]
        
        self.assertTrue(len(all_states)==27)
        self.assertTrue(len(all_br_states)==27)
        
        results = all(elm in all_states for elm in all_br_states)
        self.assertTrue(results)

    def test_capitals(self):
        print ("running test_capitals...")
        with gzip.open('capitais.json.gz', 'rb') as db:
            all_capitals = json.load(db)

        with gzip.open('data.json.gz', 'rb') as db:
            cities = json.load(db)
        
        cities = [x for x in cities if x['capital']]

        found = []
        for capital in all_capitals:
            c = SimpleNamespace(**capital)
            for city in cities:
                d = SimpleNamespace(**city)
                if({d.nome_municipio, d.uf, d.estado} & {c.capital, c.sigla, c.estado}):
                    found.append(capital)
                    break

        self.assertTrue(len(found)==27)


if __name__ == '__main__':
    unittest.main()