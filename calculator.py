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
from functools import reduce


def base(*args):
    """returns base index page"""
    return """<html>
    <h1>WSGI Calculator How To</h1>
    The page works through entering data into the url.  
    <ul>
    <li>add: /add/23/42      => 65 </li>
    </ul>Here's how to use this page...</html>"""


def add(*args):
    """ Returns a STRING with the sum of the arguments """
    return str(sum([float(i) for i in args]))


def multiply(*args):
    """ Returns STRING with inputs multiplied"""
    return str(reduce(lambda x, y: float(x) * float(y), args))


def divide(*args):
    """ Returns STRING with inputs multiplied"""
    try:
        return str(reduce(lambda x, y: float(x) / float(y), args))
    except ZeroDivisionError:
        raise ValueError


def subtract(*args):
    """ Returns a STRING with the sum of the arguments """
    return str(float(args[0]) - float(args[1]))


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """
    funcs = {
        "": base,
        "add": add,
        "multiply": multiply,
        "divide": divide,
        "subtract": subtract,
    }

    path = path.strip("/").split("/")

    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args


def application(environ, start_response):
    # TODO: Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.
    #
    # TODO (bonus): Add error handling for a user attempting
    # to divide by zero.
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get("PATH_INFO", None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    except ValueError:
        status = "422 Unprocessable Entity"
        body = "<h1>Resource found but inputs not valid</h1>"
        print(traceback.format_exc())

    finally:
        headers.append(("Content-length", str(len(body))))
        start_response(status, headers)
        return [body.encode("utf8")]


if __name__ == "__main__":
    from wsgiref.simple_server import make_server

    srv = make_server("localhost", 8080, application)
    srv.serve_forever()
