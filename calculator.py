#!/usr/bin/env python
"""
# ------------------------------------------------------------------------ #
# Title: Lesson 4 - WSGI (The Web Server Gateway Interface) example.  This script
# is a set of simple calculator web pages allowing the user to pass values in and get
# calculated values back.
# Description: This is the main "calculator.py" script.
# ChangeLog (Who,When,What):
# ASimpson, 10/21/2020, Modified code to complete lesson4 - Assignment04
# ------------------------------------------------------------------------ #
"""

import re
import functools

DEFAULT = "No Value Set"


def index():
    funcs = ['add', 'subtract', 'multiply', 'divide']

    body = ['<h1>Calculator!!</h1>', '<h2>To use this calculator, select the<br>'
            ' operation below and add a "/" between each<br>'
            ' number in the URL address bar.  <br> <br>   Ex: /multiply/3/5</h2>', '<br>']

    item_template = '<ul><li><a href="/{0}/">{0} numbers</a></li>'
    for func in funcs:
        body.append(item_template.format(func))
        body.append('</ul>')
    return '\n'.join(body)


def add(*args):
    """ Returns a STRING with the sum of the arguments """
    response_body = '<h1>Your total is: {0}</h1><br><a href="/">Back to the ' \
                    'list of operations</a>'.format(str(sum(map(int, args))))
    return response_body


def subtract(*args):
    """ Returns a STRING with the sum of the arguments """
    if len(args) == 0:
        sum = 0
    else:
        sum = functools.reduce(lambda a, b: a - b, map(int, args))
    response_body = '<h1>Your total is: {0}</h1><br><a href="/">Back to the list of operations</a>'.format(str(sum))
    return response_body


def multiply(*args):
    """ Returns a STRING with the sum of the arguments """
    if len(args) == 0:
        sum = 0
    else:
        sum = functools.reduce(lambda a, b: a * b, map(int, args))
    response_body = '<h1>Your total is: {0}</h1><br><a href="/">Back to the list of operations</a>'.format(str(sum))
    return response_body


def divide(*args):
    """ Returns a STRING with the sum of the arguments """
    try:
        sum = 0
        if "0" in args:
            raise ZeroDivisionError
        if 0 in args:
            raise ZeroDivisionError
        if len(args) == 0:
            raise ValueError
        sum = functools.reduce(lambda a, b: a / b, map(int, args))
        response_body = '<h1>Your total is: {0}</h1><br><a href="/">Back to the list of operations</a>'.format(str(sum))
        return response_body
    except ZeroDivisionError:
        response_body = '<h1>Cannot divide by zero. Try Again!</h1><br><a href="/">Back to the list of operations</a>'
        return response_body
    except ValueError:
        response_body = '<h1>No values were provided for Division Operation.<br>Please provide values and Try Again!' \
                        '</h1><br><a href="/">Back to the list of operations</a>'
        return response_body


def application(environ, start_response):
    """Application function used to create a response in bytes bak to the client"""
    try:
        headers = [("Content-type", "text/html")]
        func, args = resolve_path(environ.get('PATH_INFO', DEFAULT))
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
    except ZeroDivisionError:
        status = "Can not divide by zero"
        body = "<h1>Zero Division Error.  Please Try again!!</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """
    funcs = {"": index, "add": add, "subtract": subtract,
             "multiply": multiply, "divide": divide}

    path = path.strip('/').split('/')
    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError
    return func, args


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
