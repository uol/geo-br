# GeoBR

A geolocation library developed in Python to retrieve the user's location in Brazil.

## Download

https://github.com/uol/geo-br.git


## Prerequisites

The module depends on a KML file containing the coordinates of all Brazilian counties, which can be downloaded from:
http://www.gmapas.com/poligonos-ibge/municipios-do-brasil

Instaled virtualenv
```sh
pip install virtualenv
```

## Installing

Run within the project folder

Before start using the project you need converting the downloaded kml file into a binary file

```sh
python convert.py data.kml.gz

```

Create a virtual environment
```sh
make help           # show available options
make python-reqs    # install python packages in requirements.txt
make start          # launch a server from the local virtualenv
make test           # run the project tests
```

## Examples

```
curl -v "localhost:8080/?lat=-3.119856&lon=-60.045" -H "X-Token: fc0ae500c04c13425dc306c0342ebf85d6f260243c2bf0a9f6b7dbaa040db461";echo
```
```
HTTP/1.1 200 OK
Connection: close
Access-Control-Allow-Origin: *
X-Profile: 0
X-Req: 1ee3f430-43aa-49aa-b096-12861e4e90ff
X-Version: 2.1.0
X-Id: 127.0.0.1:44052
Content-Length: 43
Content-Type: application/json

{"city":"Manaus","state":"AM","found":true}
```

Response data

```
X-Profile : execution time in ms
X-Req : request ID
X-Version : module version
found: true => lat+long was found
found: false => lat+long not found, return the fallback result
```

Running the tests
Explain how to run the automated tests for this system

Give an example
And coding style tests
Explain what these tests test and why

Give an example
Deployment
Add additional notes about how to deploy this on a live system

## Built With
Sanic - The web framework used

## Contributing
Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning
We use SemVer for versioning. For the versions available, see the tags on this repository.

## Authors
Ivan Rocha - Initial work

## License
This project is licensed under the GNU GENERAL PUBLIC LICENSE - see the LICENSE.md file for details