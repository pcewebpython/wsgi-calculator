import traceback

"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

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

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""


def home():

    body = """
    <h2>Calculator Home</h2>
    <h3>To use this calculator, input the operator and two "/" separated values in the url path:
    <ul><li>http://localhost:8080/multiply/3/5   => 15</li>
    <li>http://localhost:8080/add/23/42      => 65</li>
    <li>http://localhost:8080/subtract/23/42 => -19</li>
    <li>http://localhost:8080/divide/22/11   => 2</li></ul>"""

    return body


def add(*args):
    """ Returns a STRING with the sum of the arguments """

    body = '<h2>Sum of {} and {}: {}</h2>'.format(*args, sum(args))
    return body


def subtract(*args):
    """ Returns a STRING with the difference of the arguments """

    body = '<h2> Difference of {} and {}: {}</h2>'.format(*args, args[0]-args[1])
    return body


def multiply(*args):
    """ Returns a STRING with the product of the arguments """

    body = '<h2> Product of {} and {}: {}</h2>'.format(*args, args[0]*args[1])
    return body


def divide(*args):
    """ Returns a STRING with the quotient of the arguments """

    try:
        body = '<h2> Quotient of {} and {}: {}</h2>'.format(*args, args[0]/args[1])
    except ZeroDivisionError:
        body = '<h2> Cannot divide by zero!</h2>'
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
        'divide': divide,
    }
    path = path.strip('/').split('/')
    func_name = path[0]
    args = path[1:]
    args = [int(i) for i in args]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args


def application(environ, start_response):
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        print('path: {}'.format(path))
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = ['<h1>WSGI Calculator</h1>']
        body.append(func(*args))
        body = '\n'.join(body)
        status = "200 OK"
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
        print(body)
        return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
