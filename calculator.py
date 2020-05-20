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

def home():
	""" Returns a home page with information for using the calculator """
	home_str = """
	Here's how to use this page:<br><br>
	Enter the type of operation, then enter in n1 and n2 separating each
	item with a backlash.<br>
	Please use the example below.<br><br>
	
	Examples:<br>
	Addition: http://localhost:8080/add/n1/n2 <br>
	Subtraction: http://localhost:8080/subtract/n1/n2 <br>
	Multiplication: http://localhost:8080/multiply/n1/n2 <br>
	Division: http://localhost:8080/divide/n1/n2 <br><br>
	"""
	return home_str

def add(*args):
    """ Returns a STRING with the sum of the arguments """
    sum = int(args[0]) + int(args[1])
    sum_str = f"The sum is {sum}."
    return sum_str

def subtract(*args):
    """ Returns a STRING with the difference of the arguments """
    dif = int(args[0]) - int(args[1])
    dif_str = f"The difference is {dif}."
    return dif_str

def multiply(*args):
    """ Returns a STRING with the product of the arguments """
    pro = int(args[0]) * int(args[1])
    pro_str = f"The product is {pro}."
    return pro_str

def divide(*args):
    """ Returns a STRING with the quotient of the arguments """
    quo = int(args[0]) / int(args[1])
    quo_str = f"The product is {quo}."
    return quo_str

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """
    funcs = {"": home, "add": add, "subtract": subtract, "multiply": multiply, "divide": divide}    
    path = path.strip('/').split('/')
    func_name = path[0]
    args = path[1:]

    try:
    	func = funcs[func_name]
    except KeyError:
    	raise NameError
    return func, args

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
