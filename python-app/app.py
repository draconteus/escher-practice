import requests
import sys
from flask import Flask, request, Response
from http import HTTPStatus
from urllib.parse import urlparse
from escherauth_go.escher_validator import EscherValidator, EscherValidatorError
from escherauth_go.escher_signer import EscherSigner

import json
import os

validator = EscherValidator(os.getenv('ESCHER_CREDENTIAL_SCOPE'),
                            json.loads(os.getenv('ESCHER_KEYPOOL')),
                            authHeaderName='X-Ems-Auth',
                            dateHeaderName='X-Ems-Date')
signer = EscherSigner(os.getenv('NODE_ESCHER_KEY_ID'),
                      os.getenv('NODE_ESCHER_SECRET'),
                      os.getenv('NODE_ESCHER_CREDENTIAL_SCOPE'))

def escher_validate(incoming_request):
    parsed_url = urlparse(incoming_request.url)
    url_with_query_params = (parsed_url.path + '?' + parsed_url.query).rstrip('?')
    validator.validateRequest(
        incoming_request.method,
        url_with_query_params,
        incoming_request.data.decode('utf-8'),
        incoming_request.headers
    )
    
def escher_request(method, path):
    host = os.getenv('NODE_HOST')
    port = os.getenv('NODE_PORT')
    headers = signer.signRequest(method, path, None, {'host': host})
    return requests.get('http://' + host + ':' + port + path, headers=headers)

app = Flask(__name__)

@app.route("/")
def unauth():
    return "Ok, that's fine!"

@app.route("/start")
def start_ping_pong():
    app.logger.info('\nStart the ping-pong\n')
    response = escher_request('GET', '/ping')
    app.logger.info('\nResponse from node service:' + response.text)
    return Response(response.text, response.status_code)

@app.route("/ping", methods=['GET'])
def authenticated():
    try:
        escher_validate(request)
        return Response('\nPong\n', HTTPStatus.OK)
    except EscherValidatorError as e:
        app.logger.error(e)
        return Response(str(e), HTTPStatus.UNAUTHORIZED)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
