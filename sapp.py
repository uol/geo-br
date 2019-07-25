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

import copy
import functools
import json
import geohash
import gzip
import multiprocessing
import pickle
import socket
import time
import uuid
import sys

from collections import namedtuple, Counter
from datetime import datetime

from sanic import Sanic
from sanic.response import json as jsonify
from sanic.exceptions import SanicException
from sanic_cors import CORS, cross_origin

from fastkml import kml
from shapely.geometry import Point

from types import SimpleNamespace


with gzip.open('data.dat.gz', 'rb') as k:
    d = pickle.load(k)

print(sys.version_info)
C = { "global": Counter(), "stats": Counter() }
G = SimpleNamespace(**{"config": None})

with open('sapp.json', 'rt', encoding='utf-8') as j:
    G.config = json.load(j)
    G.config = SimpleNamespace(**G.config)
    G.config.tokens = set(G.config.tokens)
    for token in G.config.tokens:
        if token not in C:
            C["stats"][token[:6]] = Counter()
    DG = copy.deepcopy(G)
    DG.config.tokens = [t[:6] for t in G.config.tokens]
    print(DG)


@functools.lru_cache(maxsize=G.config.maxsize)
def search(ghash):
    latitude, longitude = geohash.decode(ghash)
    return _search(latitude, longitude)


def _search(latitude, longitude):
    p = Point(longitude, latitude)
    for i, c in enumerate(d):
        g = c.geometry
        if p.within(g):
            t = list(c.extended_data.elements[0].data)
            h = {e["name"]:e["value"] for e in t if e["name"] in ["SIGLA", "NOME_MUNIC"]}
            return {"city": h["NOME_MUNIC"], "state": h["SIGLA"], "found": True}
    return None


app = Sanic()
app.config.KEEP_ALIVE = False


@app.middleware('request')
async def before_request(request):
    g = namedtuple("g", ["start_time", "request_id"])
    request["g"] = g(datetime.now(), str(uuid.uuid4()))


@app.middleware('response')
async def after_request(request, response):
    g = request["g"]
    dt = datetime.now() - g.start_time
    ms = str(round((dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0))
    response.headers['X-Profile'] = ms
    response.headers['X-Req'] = g.request_id
    response.headers['X-Version'] = G.config.version
    response.headers['X-Id'] = f"{request.ip}:{request.port}"


@app.route('/check')
async def check(request):
    return jsonify(C)


@app.route('/', methods=['GET'])
@cross_origin(app, origins=G.config.origins, automatic_options=True)
async def index(request):
    token = request.headers.get("X-Token")
    if token not in G.config.tokens:
        C["global"].update({"401": 1})
        raise SanicException("Unauthorized", status_code=401)
    try:
        latitude = float(request.args.get("lat", default=None))
        longitude = float(request.args.get("lon", default=None))
        ghash = geohash.encode(latitude, longitude, G.config.precision)
    except:
        C["stats"][token[:6]].update({"400": 1})
        raise SanicException("Bad Request", status_code=400)
    try:
        data = search(ghash)
        if data is None:
            C["stats"][token[:6]].update({"404": 1})
            return jsonify(G.config.fallback)
        else:
            C["stats"][token[:6]].update({"200": 1})
            return jsonify(data)
    except:
        C["stats"][token[:6]].update({"500": 1})
        return jsonify(G.config.fallback)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "--console":
        pass
    else:
        app.run(host='0.0.0.0', port=8080, workers=multiprocessing.cpu_count())


"""
_search(-23.643414, -46.759600)

http -v "http://localhost:8080/?lat=-23.643414&lon=-46.759600" X-Token:fc0ae500c04c13425dc306c0342ebf85d6f260243c2bf0a9f6b7dbaa040db461
http -v "http://localhost:8080/?lat=-3.119856&lon=-60.045" X-Token:fc0ae500c04c13425dc306c0342ebf85d6f260243c2bf0a9f6b7dbaa040db461
"""