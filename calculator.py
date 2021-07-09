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


def should_be_int(number):
    """ Convert the number to an integer if it is zero to the right of the decimal.
    """
    if number.is_integer():
        return int(number)
    return number


def add(*args):
    """ Returns a STRING with the sum of the arguments """
    sum = 0
    for i in range(0, len(args)):
        sum = sum + args[i]

    sum = should_be_int(sum)
    
    return str(sum)


def subtract(*args):
    """ Returns a STRING with the difference of the arguments """
    diff = args[0]
    for i in range(1, len(args)):
        diff = diff - args[i]
    
    diff = should_be_int(diff)

    return str(diff)


def multiply(*args):
    """ Returns a STRING with the product of the arguments """
    product = 1
    for i in range(0, len(args)):
        product = product * args[i]
    
    product = should_be_int(product)

    return str(product)


def divide(*args):
    """ Returns a STRING with the quotient of the arguments """
    quotient = args[0]
    for i in range(1, len(args)):
        quotient = quotient / args[i]
    
    quotient = should_be_int(quotient)

    return str(quotient)


def instructions():
  return """
<head>
<title>Instructions</title>
</head>
<body>
<h1><u>Instructions</u></h1>
<p>
This website will add, subtract, multiply, and divide an arbitrary number of values by entering a URL.<br>
To use, the first part of the URL should be http://localhost:8080 . <br>
The next part of the URL will be a forward slash ('/') followed by the math operator expressed as a word 
- i.e. '/add', '/subtract', '/multiply', or '/divide'. <br>
The values you want to apply the operator to follow the operator, each separated by a single foward slash.<br>
The operator is applied from left to right.
</p>
<p>Here are some example URL's:</p>
<p>
  http://localhost:8080/add/23/42   &rarr;   (23 + 42)<br>
  http://localhost:8080/subtract/23/42/1   &rarr;   (23 - 42 - 1)<br>
  http://localhost:8080/multiply/3/5/2   &rarr;   (3 * 5 * 2)<br>
  http://localhost:8080/divide/22/11   &rarr;   (22 / 11)<br>
</p>
http://localhost:8080/ will bring you back to these instructions.
</body>
"""

  
def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """
    funcs = {
        '': instructions,
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

    try:
        converted_args = list(map(float, args))
    except ValueError:
        raise ValueError

    # handle divide by zero error
    try:
        if func is divide:
            if converted_args.index(0) > 0:  # first argument can be 0
                raise ZeroDivisionError
    except ValueError:  # no 0 value is OK
        pass

    return func, converted_args


def application(environ, start_response):
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
    except ValueError:
        status = "400 Bad Request"
        body = "<h1>A value is not a number.</h1>"
    except ZeroDivisionError:
        status = "400 Bad Request"
        body = "<h1>Divide by zero error.</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
