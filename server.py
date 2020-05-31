from json import dumps

from bottle import get, post, run, request, static_file

from main import find_relevant


@post('/find')
def find():
    terms = request.body.read().decode('utf-8').split()
    data = find_relevant(terms)
    return dumps([a.__dict__ for a in data[:10]])


@get('/')
def index():
    return static_file('index.html', '.')


run(host='localhost', port=8080, debug=True)