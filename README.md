# Escher Practice

It's purpose to show how two services (written in 2 different languages) can communicate securely with Escher signing the requests. I wanted to show clearly and with the bare minimum how a signed request can be made and received.

Communicating services:

<Node> <===> <Python>


Endpoints (on both sides):
`/`      => no authentication (not every route need authentication, eg.: checking service health)
`/start` => no authentication (send a singed request to the other service)
`/ping`  => authenticated route, with proper singning responds with Pong
