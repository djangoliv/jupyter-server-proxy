def mappathf(path):
    p = path + 'mapped'
    return p

def translate_ciao(path, host, response, orig_response, port):
    # Assume that the body has not been modified by any previous rewrite
    assert response.body == orig_response.body

    response.code = 418
    response.reason = "I'm a teapot"
    response.headers["i-like"] = "tacos"
    response.headers["Proxied-Host-Port"] = f"{host}:{port}"
    response.headers["Proxied-Path"] = path
    response.body = response.body.replace(b"ciao", b"hello")

def hello_to_foo(response):
    response.body = response.body.replace(b"hello", b"foo")

# Example from the rewrite_response docstring
def dog_to_cat(response):
    response.headers["I-Like"] = "tacos"
    response.body = response.body.replace(b'dog', b'cat')


# Example from the rewrite_response docstring
def cats_only(response, path):
    if path.startswith("/cat-club"):
        response.code = 403
        response.body = b"dogs not allowed"

c.ServerProxy.servers = {
    'python-http': {
        'command': ['python3', './tests/resources/httpinfo.py', '{port}'],
    },
    'python-http-abs': {
        'command': ['python3', './tests/resources/httpinfo.py', '{port}'],
        'absolute_url': True
    },
    'python-http-port54321': {
        'command': ['python3', './tests/resources/httpinfo.py', '{port}'],
        'port': 54321,
    },
    'python-http-mappath': {
        'command': ['python3', './tests/resources/httpinfo.py', '{port}'],
        'mappath': {
            '/': '/index.html',
        }
    },
    'python-http-mappathf': {
        'command': ['python3', './tests/resources/httpinfo.py', '{port}'],
        'mappath': mappathf,
    },
    'python-websocket' : {
        'command': ['python3', './tests/resources/websocket.py', '--port={port}'],
        'request_headers_override': {
            'X-Custom-Header': 'pytest-23456',
        }
    },
    'python-request-headers': {
        'command': ['python3', './tests/resources/httpinfo.py', '{port}'],
        'request_headers_override': {
            'X-Custom-Header': 'pytest-23456',
        }
    },
    'python-gzipserver': {
        'command': ['python3', './tests/resources/gzipserver.py', '{port}'],
    },
    'python-http-rewrite-response': {
        'command': ['python3', './tests/resources/httpinfo.py', '{port}'],
        'rewrite_response': translate_ciao,
        'port': 54323,
    },
    'python-chained-rewrite-response': {
        'command': ['python3', './tests/resources/httpinfo.py', '{port}'],
        'rewrite_response': [translate_ciao, hello_to_foo],
    },
    'python-cats-only-rewrite-response': {
        'command': ['python3', './tests/resources/httpinfo.py', '{port}'],
        'rewrite_response': [dog_to_cat, cats_only],
    },
    'python-dogs-only-rewrite-response': {
        'command': ['python3', './tests/resources/httpinfo.py', '{port}'],
        'rewrite_response': [cats_only, dog_to_cat],
    },
}

c.ServerProxy.non_service_rewrite_response = hello_to_foo

import sys
sys.path.append('./tests/resources')
c.ServerApp.jpserver_extensions = { 'proxyextension': True }
c.NotebookApp.nbserver_extensions = { 'proxyextension': True }
#c.Application.log_level = 'DEBUG'
