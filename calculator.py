from wsgiref.simple_server import make_server
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

def index():
    """ Returns a STRING with the sum of the arguments """
    example_list = [
        '/add/400/23/10',
        '/subtract/23',
        '/multiply/21/43',
        '/divide/2000/50'
    ]

    body = [
        '<h1>WSGI CALCULATOR</h1>',
        '<p>Here\'s how to use this tool:</p>',
        '<p>You will use the path in the url browser to calculate values. Your path will have a format of: </p>',
        '<p>/{function}/{arg1}/{arg2}/{arg3}/...</p>',
        '<p>The calculator will then use the function and apply it to the list of ',
        'arguments in the path. Please see below for examples on how to formulate urls. ',
        'Each link will provide the result from the calculation. </p>'
        '<h3>Examples:</h3>',
        '<ul>',
    ]

    item_template = '<li><a href="{}">http://localhost:8080{}</a></li>'
    for path in example_list:
        body.append(item_template.format(path, path))
    body.append('</ul>')
    return '\n'.join(body)


def add(*args):
    """ Returns a STRING with the sum of the arguments """

    summation = 0
    for number in args:
        summation += int(number)

    return str(summation)


def subtract(*args):
    """ Returns a STRING with the result of the arguments """

    base_num = int(args[0])
    for index in range(1, len(args)):
        base_num -= int(args[index])

    return str(base_num)


def multiply(*args):
    """ Returns a STRING with the product of the arguments """

    product = int(args[0])
    for number in range(1, len(args)):
        product *= int(args[number])

    return str(product)


def divide(*args):
    """ Returns a STRING with the quotient of the arguments """

    quotient = int(args[0])
    for number in range(1, len(args)):
        quotient /= int(args[number])

    return str(quotient)


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    # Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
    funcs = {
        '/': index,
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide
    }
    if path == '/':
        func_name = path
    else:
        path = path.strip('/').split('/')
        func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args


def application(environ, start_response):
    # Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.
    #
    # TODO (bonus): Add error handling for a user attempting
    # to divide by zero.
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
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
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
