""" calculator.py script """

#imports
import traceback
import operator as op
from functools import reduce

# =============================================
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
# =============================================

def info():
    """ info page """
    page = """
    <h1>Information</h1>
    <hr></hr>
    <ul style="list-style-type:circle;">
        <li>Addition example:
            <a href = "http://localhost:8080/add/3/5"> 3 + 5</a>
        </li>
        <li>Subtraction example:
            <a href = "http://localhost:8080/subtract/23/42"> 23 - 42</a>
        </li>
        <li>Multiplication example: 
            <a href = "http://localhost:8080/multiply/3/5"> 3 * 5</a>
        </li>
        <li>Division example:
            <a href = "http://localhost:8080/divide/22/11"> 21 / 11</a>
        </li>
    </ul>
    <hr></hr>
    """
    return page
# ----------------------------------------------

def add(*args):
    """ Returns a STRING with the sum of the arguments """
    # TODO: Fill sum with the correct value, based on the
    # args provided.

    summation = round(sum(map(float, args)), 4)
    page = """
        <h1>Addition</h1>
        <p>The sum of listed numbers <b>{}</b> is: <b>{}</b></p>
        <a href="/">Back to info page</a>
        <p><b>NOTE:</b> <i>continue entering numbers to browser 
        line to add to current sum; eg /add/3/5/7 -> 15 </i></b>
    """
    return page.format(list(map(float, args)), summation)
# ----------------------------------------------

# TODO: Add functions for handling more arithmetic operations.
def subtract(*args):
    """ Returns a STRING with the difference of the arguments """
    # TODO: Fill sum with the correct value, based on the
    # args provided.

    difference = round(op.sub(*map(float, args)), 4)
    page = """
        <h1>Subtraction</h1>
        <p>The difference of <b>{}</b> and <b>{}</b> is: <b>{}</b></p>
        <a href="/">Back to info page</a>
        <p><b>NOTE:</b> <i>only first two numbers in browser'e line will
        be subtracted; eg /substact/23/42 -> -19, 
        entering more numbers will generate an error</i></b>
    """
    return page.format(*map(float, args), difference)
# ----------------------------------------------

def multiply(*args):
    """ Returns a STRING with the product of the arguments """
    # TODO: Fill sum with the correct value, based on the
    # args provided.

    product = round(reduce((lambda x, y: float(x) * float(y)), args), 4)
    page = """
        <h1>Multiplication</h1>
        <p>The product of numbers <b>{}</b> is: <b>{}</b></p>
        <a href="/">Back to info page</a>
        <p><b>NOTE:</b> <i>continue entering numbers to browser 
        line to multiply to current product; 
        eg /multiply/3/5/7 -> 105 </i></b>
    """
    return page.format(list(map(float, args)), product)
# ----------------------------------------------

def divide(*args):
    """ Returns a STRING with the division of the arguments """
    # TODO: Fill sum with the correct value, based on the
    # args provided.

    if float(args[1]) != 0.:
        fraction = round(op.truediv(*map(float, args)), 4)
    else:
        raise ZeroDivisionError
    page = """
        <h1>Division</h1>
        <p>The fraction of <b>{}</b> and <b>{}</b> is: <b>{}</b></p>
        <a href="/">Back to info page</a>
        <p><b>NOTE:</b> <i>only first two numbers in browser'e line will
        be divided; eg /divide/22/11 -> 1, 
        entering more numbers will generate an error</i></b>
    """
    return page.format(*map(float, args), fraction)
# ----------------------------------------------

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """
    # TODO: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
    # func = add
    # args = ['25', '32']

    path = path.strip("/").split("/")

    func_name = path[0]
    args = path[1:]

    funcs = {
        "": info,
        "add": add,
        "subtract": subtract,
        "multiply": multiply,
        "divide": divide
        }

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError
    return func, args
# ----------------------------------------------

def application(environ, start_response):
    """ app """
    # TODO: Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.
    #
    # TODO (bonus): Add error handling for a user attempting
    # to divide by zero.

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
        body = """"
            <h1>Not Found</h1>
            <a href="/">Back to info page</a>
            """
    except ZeroDivisionError:
        status = "400 Bad Request"
        body = """
            <h1>Unexpected Division by Zero</h1>
            <a href="/">Back to info page</a>
        """
    except Exception:
        status = "500 Internal Server Error"
        body = """
            <h1> Internal Server Error</h1>
            <a href="/">Back to info page</a>
        """
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
    return [body.encode('utf-8')]
# =============================================


if __name__ == '__main__':
    # TODO: Insert the same boilerplate wsgiref simple
    # server creation that you used in the book database.
    from wsgiref.simple_server import make_server
    SRV = make_server('localhost', 8080, application)
    SRV.serve_forever()
    