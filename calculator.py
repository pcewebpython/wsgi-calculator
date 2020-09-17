import re
import traceback

TEST_BODY = """<html>
<head>
<title>Test Mike - WSGI Assignment</title>
</head>
<body>
<p>Hello world Mike</p>
</body>
</html>"""


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

# DONE: Include other functions for handling more arithmetic operations.

def add(*args):
    """ Returns a STRING with the sum of the arguments """

    # DONE: Fill sum with the correct value, based on the
    # args provided.

    print (f"ddddddddddd arg1={args[0]} arg2={args[1]}")
    oper_a = args[0]
    oper_b = args[1]
    
    sum = str(int(oper_a) + int(oper_b))

    body = sum
    
    return sum

def subtract(*args):
    """ Returns a STRING with the difference of the arguments """

    # DONE: Fill difference with the correct value, based on the
    # args provided.

    print (f"eeeeeeeeee arg1={args[0]} arg2={args[1]}")
    minuend = args[0]
    subtrahend = args[1]
    
    difference = str(int(minuend) - int(subtrahend))

    body = difference
    
    return difference

    
def divide(*args):
    """ Returns a STRING with the difference of the arguments """

    # DONE: Fill quotient with the correct value, based on the
    # args provided.

    print (f"fffffffffff arg1={args[0]} arg2={args[1]}")
    dividend = args[0]
    divisor = args[1]
    
    quotient = str(int(dividend) / int(divisor))

    body = quotient
    
    return quotient

    
def resolve_path(path):

    print ("CCCCCCCCC 111111111111")
    
    funcs = {
        '': add,
        'book': add,
        'add': add,
        'subtract': subtract,
        'divide': divide,
        
    }

    print("CCCCC 22222222222")

    path = path.strip('/').split('/')

    print("CCCCC 22222222222")

    func_name = path[0]
    args = path[1:]

    print("CCCCC 22222222222")

    # DONE: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
    
    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    print("CCCCC 33333333")
        
    return func, args

def resolve_path_TODO(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    # TODO: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
    func = add
    args = ['25', '32']

    return func, args

def application(environ, start_response):
    # Done:

    print("BBBBBB")
    
    pass
    
    body = ""
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        print(f"BBBBBB path = -{path}-")
        if path is None:
            raise NameError
        body = TEST_BODY        #***MMM temp only test
        print("BBBBBB calling resolve_path")
        func, args = resolve_path(path)
        print("BBBBBB return from resolve_path")
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
    # TODO: Insert the same boilerplate wsgiref simple
    # server creation that you used in the book database.
    pass
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
