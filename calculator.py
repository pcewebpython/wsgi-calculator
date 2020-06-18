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
import traceback
from numpy import prod


def add(*args):
    """ Returns a STRING with the sum of the arguments """
    return sum(map(int, args))


def subtract(*args):
    """ Returns a STRING, in which the first number retains its value, the remaining numbers
    take their negative value, and all numbers are summed."""
    args_mut = []
    for i in range(len(args)):
        args_mut.append('')
        if i == 0:
            args_mut[i] = int(args[i])
        else:
            args_mut[i] = int(args[i]) * -1
    return sum(map(int, args_mut))


def multiply(*args):
    """ Returns a STRING, in which all numbers are multiplied in sequence."""
    return prod(list(map(int, args)))


def divide(*args):
    """ Returns a STRING, in which the numbers are divided in sequence.
    ZeroDivisionError included."""
    if '0' in args[1:]:
        raise ZeroDivisionError

    args_mut = []
    for arg in args:
        args_mut.append(int(arg))
    quotient = args_mut[0]
    for i in range(1, len(args_mut)):
        quotient /= args_mut[i]

    return quotient


def instructions():
    """Return an html string of instructions."""
    page = """
<h1>Instructions</h1>
<ul>
<li>add, subtract, multiply, or divide goes after root</li>
<li>any sequence of integers separated by / goes next</li>
<li>example: http://127.0.0.1:8080/divide/2/5/9/10</li>
</ul>
"""

    return page


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """
    funcs = {'': instructions, 'add': add, 'subtract': subtract, 'multiply': multiply,
             'divide': divide}

    path = path.strip('/').split('/')

    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args


def application(environ, start_response):
    """Provide the response, including for raised ZeroDivisionError."""
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1> Not Found</h1>"
    except ZeroDivisionError:
        status = "403 Forbidden"
        body = "<h1>Division by Zero Not Permitted</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(str(body)))))
        start_response(status, headers)
    return [str(body).encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('127.0.0.1', 8080, application)
    srv.serve_forever()
