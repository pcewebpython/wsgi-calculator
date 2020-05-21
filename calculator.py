import traceback
import numpy as np
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
    """Instructions for the calc"""
    body = """
    <h1>WSGI Calculator</h1>
    <p>There are 4 methods:</p>
    <ul>
        <li>add</li>
        <li>subtract</li>
        <li>multiply</li>
        <li>divide</li>
    </ul>
    <p>To use calculator enter operants in address bar</p>
    <p>eg. /add/1/2</p>

    
    """    
    return body

def add(*args):
    """Returns a STRING with the sum of the arguments"""
    sumation = np.sum([int(i) for i in args])  
    
    return str(sumation)


def subtract(*args):
    """Returns a STRING with the difference of the arguments"""
    # np.diff starts with the last number first i guess...
    # orig = [1,2,3] 3-2-1 = 0
    # reversed = [1,2,3] 1-2-3 = -4
    diff = int(np.diff([int(i) for i in reversed(args)]))
    
    return str(diff)

def multiply(*args):
    """Returns a STRING with the product of the arguments"""
    product = np.prod([int(i) for i in args]) 
    
    return str(product)

def divide(*args):
    """Returns a STRING with the quotient of the arguments"""
    args = [int(i) for i in args]
    quotient = args[0]
    for num in args[1:]:
        if num == 0:
            raise ZeroDivisionError
        quotient = quotient / num

    return str(quotient)

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    func_dict = {
        "": index,
        "add": add,
        "subtract": subtract,
        "multiply": multiply,
        "divide": divide
    }

    path = path.strip("/").split("/")
    func = path[0]
    args = path[1:]
    try:
        func = func_dict[func]
    except KeyError:
        raise NameError

    return func, args

def application(environ, start_response):
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        print(path)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    
    except ZeroDivisionError:
        status = "404 Bad Request"
        body = "<h1>Cannot Divide by Zero</h1>"
                            
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
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
