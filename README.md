# Escher Practice

It's purpose to show how two services (written in 2 different languages) can communicate securely with Escher signing the requests. I wanted to show clearly and with the bare minimum how a signed request can be made and received.

### Communicating services

Node (`localhost:5001`) <===> Python (`localhost:5000`)


Endpoints (on both sides):
- `/`      => no authentication (not every route need authentication, eg.: checking service health)
- `/start` => no authentication (send a singed request to the other service)
- `/ping`  => authenticated route, with proper singning responds with Pong

You can curl Node `/start` to make it send a signed request to Python:
```
$ curl http://localhost:5000/start -v
```
or fabricate your own signed request with [httpie](https://github.com/jakubroztocil/httpie) with [escher plugin](https://github.com/emartech/httpie-ems-auth) to send it (in the name of the Python service) to `/ping`:

```
$ http -v --verify=no --auth-type ems-auth -a eu/node/scope/python-node_v1:PythonNode GET http://localhost:5001/ping
```

You can do the same things with the Python service:
```
$ curl http://localhost:5001/start -v
```
```
$ http -v --verify=no --auth-type ems-auth -a eu/python/scope/node-python_v1:NodePython GET http://localhost:5000/ping
```
