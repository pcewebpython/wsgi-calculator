import re
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


def add(*args):
    """ Returns a STRING with the sum of the arguments """
    # TODO: Fill sum with the correct value, based on the
    # args provided.
    try:
        res = str(int(args[0]) + int(args[1]))
        return '{} + {} = {}'.format(args[0], args[1], res)
    except ValueError:
        raise ValueError

def substract(*args):
    """ Returns a STRING with the subtract of the arguments """
    try:
        res = str(int(args[0]) - int(args[1]))
        return '{} - {} = {}'.format(args[0], args[1], res)
    except ValueError:
        raise ValueError

def multiply(*args):
    """ Returns a STRING with the multiply of the arguments """
    try:
        res = str(int(args[0]) * int(args[1]))
        return '{} * {} = {}'.format(args[0], args[1], res)
    except ValueError:
        raise ValueError

def divide(*args):
    """ Returns a STRING with the divide of the arguments """
    try:
        res = str(int(args[0]) / int(args[1]))
        return '{} / {} = {}'.format(args[0], args[1], res)
    except ValueError:
        if args[1] == 0:
            raise ZeroDivisionError
        raise ValueError

def instructions():
    """ Returns a STRING about how to use the calculator """
    ins = """
            <h1> Here is how to use the calculator:</h1>
            <li> Input URL http://localhoat:8080/add/2/3 for 2 + 3</li>
            <li> Input URL http://localhoat:8080/multiply/2/3 for 2 * 3</li>
            <li> Input URL http://localhoat:8080/subtract/2/3 for 2 - 3</li>
            <li> Input URL http://localhoat:8080/divide/2/3 for 2 / 3</li>
    """
    return ins

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    # TODO: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
    functions = {
        '': instructions,
        'add': add,
        'subtract': substract,
        'multiply': multiply,
        'divide': divide
    }
    path = path.strip('/').split('/')
    func_name = path[0]
    func_args = path[1:]

    try:
        func = functions[func_name]
    except KeyError:
        raise NameError
    finally:
        return func, func_args

def application(environ, start_response):
    # TODO: Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.
    #
    # TODO (bonus): Add error handling for a user attempting
    # to divide by zero.
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get("PATH_INFO", None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        #if len(args) == 1 or len(args) > 2:
        #    raise ValueError
        body = func(*args)
        status = '200 OK'
    except ValueError:
        status = '500 Internal Server Error'
        body = '<h1>Unable to finish the calculation. Please provide two numbers.</h1>'
    except NameError:
        status = '404 Not Found'
        body = '<h1>404 Operation Method Not Found</h1>'
    except ZeroDivisionError:
        status = '500 Internal Server Error'
        body = '<h1>Zero Division Error!</h1>'
    except Exception:
        status = '500 Internal Server Error'
        body = '<h1>Internal Server Error </h1>'
        print(traceback.format_exc())
    finally:
        headers.append(('Content-len', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    # TODO: Insert the same boilerplate wsgiref simple
    # server creation that you used in the book database.
    from wsgiref.simple_server import make_server
    srv = make_server('127.0.0.1', 8080, application)
    #srv = make_server('localhost', 8080, application)
    srv.serve_forever()
