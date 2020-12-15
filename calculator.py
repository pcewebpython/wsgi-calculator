"""
Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

"""

# Stella Kim
# Assignemt 4: WSGI Calculator

import traceback


def home(*args):
    """Returns homepage that explains how to perform calculations"""
    return 'this is the homepage'


def add(*args):
    """Returns a STRING with the sum of the arguments"""

    result = str(int(args[0]) + int(args[1]))
    body = 'Your total is: {}'.format(result)

    return body


def subtract(*args):
    """Returns a STRING with the difference of the arguments"""

    result = str(int(args[0]) - int(args[1]))
    body = 'Your total is: {}'.format(result)

    return body


def multiply(*args):
    """Returns a STRING with the product of the arguments"""

    result = str(int(args[0]) * int(args[1]))
    body = 'Your total is: {}'.format(result)

    return body


def divide(*args):
    """Returns a STRING with the quotient of the arguments"""

    result = str(int(args[0]) / int(args[1]))
    body = 'Your total is: {}'.format(result)

    return body


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

    # TODO (bonus): Add error handling for a user attempting
    # to divide by zero.


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
