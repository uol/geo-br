"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License 
along with this program. If not, see <http://www.gnu.org/licenses/>.

Created on 2019-05-11
By P&D Aplicativos
"""

import gzip
import pickle
import sys

from fastkml import kml

E = {
    "SP": 0,
    "MG": 1,
    "RJ": 2,
    "DF": 3,
    "PR": 4,
    "BA": 5,
    "CE": 6,
    "SC": 7,
    "RS": 8,
    "ES": 9,
    "PA": 10,
    "PE": 11,
    "TO": 12,
    "AM": 13,
    "PB": 14,
    "MS": 15,
    "GO": 16,
    "AL": 17,
    "MA": 18,
    "PI": 19,
    "RN": 20,
    "SE": 21,
    "MT": 22,
    "RR": 23,
    "AP": 24,
    "RO": 25,
    "AC": 26,
}

C = {
    "São Paulo": (0, "SP"),
    "Belo Horizonte": (1, "MG"),
    "Rio de Janeiro": (2, "RJ"),
    "Brasília": (3, "DF"),
    "Curitiba": (4, "PR"),
    "Salvador": (5, "BA"),
    "Fortaleza": (6, "CE"),
    "Florianópolis": (7, "SC"),
    "Porto Alegre": (8, "RS"),
    "Vitória": (9, "ES"),
    "Belém": (10, "PA"),
    "Recife": (11, "PE"),
    "Palmas": (12, "TO"),
    "Manaus": (13, "AM"),
    "João Pessoa": (14, "PB"),
    "Campo Grande": (15, "MS"),
    "Goiânia": (16, "GO"),
    "Alagoas": (17, "AL"),
    "São Luis": (18, "MA"),
    "Teresina": (19, "PI"),
    "Natal": (20, "RN"),
    "Aracaju": (21, "SE"),
    "Cuiabá": (22, "MT"),
    "Boa Vista": (23, "RR"),
    "Macapá": (24, "AP"),
    "Porto Velho": (25, "RO"),
    "Rio Branco": (26, "AC"),
}

with gzip.open('data.kml.gz', 'rb') as k:
    doc = k.read()

k = kml.KML()
k.from_string(doc)

f = list(k.features())
d = list(f[0].features())

def helper(v):
    t = v.extended_data.elements[0].data
    h = {}
    for e in list(t):
        h[e["name"]] = e["value"]
    if "NOME_MUNIC" not in h:
        return (999, "")
    if h["NOME_MUNIC"] in C:
        s = C[h["NOME_MUNIC"]]
        if h["SIGLA"] == s[1]:
            return (s[0], h["NOME_MUNIC"])
    elif h["SIGLA"] in E:
        s = E[h["SIGLA"]] + len(C) + 1
        return (s, h["SIGLA"])
    return (99, h["NOME_MUNIC"])

d.sort(key=helper)

with gzip.open("data.dat.gz", "wb") as f:
    pickle.dump(d, f)

