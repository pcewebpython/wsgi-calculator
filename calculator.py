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
  """ Returns a home page with info on using the calculator """
  home_str = """
    Thank you for using my WSGI Calculator.<br>
    You can use this calculator by visiting one of the following pages:<br><br>

    Addition: http://localhost:8080/add/x1/x2<br>
    Subtraction: http://localhost:8080/subtract/x1/x2<br>
    Multiplication: http://localhost:8080/multiply/x1/x2<br>
    Division: http://localhost:8080/divide/x1/x2<br><br>

    where x1 and x2 are the input arguments that you would like to
    perform addition, subtraction, multiplication, or division
    operations on.
  """
  return home_str


def add(*args):
    """ Returns a STRING with the sum of the arguments """

    sum = str(int(args[0]) + int(args[1]))
    sum_str = f"The sum of the arguments provided is: {sum}"

    return sum_str

def subtract(*args):
    """ Returns a STRING with the difference of the arguments """

    difference = str(int(args[0]) - int(args[1]))
    diff_str = f"The difference of the arguments provided is: {difference}"

    return diff_str

def multiply(*args):
    """ Returns a STRING with the product of the arguments """

    product = str(int(args[0]) * int(args[1]))
    prod_str = f"The product of the arguments provided is: {product}"

    return prod_str

def divide(*args):
    """ Returns a STRING with the quotient of the arguments """
    try:
      quotient = str(int(args[0]) / int(args[1]))
    except ZeroDivisionError:
      raise Exception
    quo_str = f"The quotient of the arguments provided is: {quotient}"

    return quo_str

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
      'divide': divide
    }
    path = path.strip('/').split('/')
    func_name = path[0]
    args = path[1:]

    try:
      func = funcs[func_name]
    except KeyError:
      raise NameError

    return func, args

def application(environ, start_response):
    status = "200 OK"
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
