# Stella Kim
# Assignemt 4: WSGI Calculator

import traceback


def home(*args):
    """Returns homepage that explains how to perform calculations"""

    body = """
    <h1>WSGI Calculator</h1>
    <p><i>Here's how to use this page...</i></p>

    <p>This application allows you to add, subtract, multiply or divide two
    numbers based on the user's URL input.  The first part of the path
    indicates the operand.  The operand is followed by two numbers to solve
    the operation.</p>

    <p>Some examples are:
    <ul>
    <li>http://localhost:8080/multiply/3/5  yields a result of 15</li>
    <li>http://localhost:8080/add/23/42  yields a result of 65</li>
    <li>http://localhost:8080/subtract/23/42  yields a result of -19</li>
    <li>http://localhost:8080/divide/22/11  yields a result of 2</li>
    </ul>
    </p>
    """
    return body


def add(*args):
    """Returns a STRING with the sum of the arguments"""

    result = str(int(args[0]) + int(args[1]))
    body = 'Your total is: {}'.format(result)

    return(body + '<p><a href="/">Back to the homepage</a></p>')


def subtract(*args):
    """Returns a STRING with the difference of the arguments"""

    result = str(int(args[0]) - int(args[1]))
    body = 'Your total is: {}'.format(result)

    return(body + '<p><a href="/">Back to the homepage</a></p>')


def multiply(*args):
    """Returns a STRING with the product of the arguments"""

    result = str(int(args[0]) * int(args[1]))
    body = 'Your total is: {}'.format(result)

    return(body + '<p><a href="/">Back to the homepage</a></p>')


def divide(*args):
    """Returns a STRING with the quotient of the arguments"""

    try:
        result = str(int(args[0]) / int(args[1]))
        body = 'Your total is: {}'.format(result)
    except ZeroDivisionError:
        body = 'Error dividing by zero, please enter a non-zero value'

    return(body + '<p><a href="/">Back to the homepage</a></p>')


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    funcs = {
        '': home,
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide
    }

    path = path.strip('/').split('/')

    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args


def application(environ, start_response):
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = '200 OK'
    except NameError:
        status = '404 Not Found'
        body = '<h1>Not Found</h1>'
    except Exception:
        status = '500 Internal Server Error'
        body = '<h1>Internal Server Error</h1>'
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
