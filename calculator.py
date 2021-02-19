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

def index(*args):
    """ Returns a howto for the calculator application"""
    howto = """
      <h1>How To Use WSGI Calculator</h1>
      <h2>Examples</h2>
      To add integers: <a href="/add/23/42">http://localhost:8080/add/23/42</a><br>
      To subtract integers: <a href="/subtract/23/42">http://localhost:8080/subtract/23/42</a><br>
      To multiply: <a href="/multiply/3/5">http://localhost:8080/multiply/3/5</a><br>
      To divide: <a href="/divide/22/11">http://localhost:8080/divide/22/11</a><br>
      """
    return howto

def add(*args):
    """ Returns a STRING with the sum of the arguments """
    args = [int(i) for i in args]
    return str(sum(args))

def subtract(*args):
    """ Returns a STRING with the subtraction of the arguments """
    diff = int(args[0]) - int(args[1])
    return str(diff)

def multiply(*args):
    """ Returns a STRING with the product of the arguments """
    product = int(args[0]) * int(args[1])
    return str(product)

def divide(*args):
    """ Returns a STRING with the division of the arguments """
    quotient = int(args[0]) / int(args[1])
    return str(int(quotient))


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """
    funcs = {
      '': index,
      'add':add,
      'subtract':subtract,
      'multiply':multiply,
      'divide':divide,
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
      body = "404 Not Found"
    except ZeroDivisionError:
      status = "400 Bad Request"
      body = "400 Bad Request: Division by Zero"
    except Exception:
      status = "500 Internal Server Error"
      body = "500 Internal Server Error"
      print(traceback.format_exc())
    finally:
      headers.append(('Content-length', str(len(body))))
      start_response(status, headers)
    return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
