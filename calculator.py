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
def instructions():
  """ Returns and instructional page at root """
  page = """
  <h1>How to use this page</h1>
  <h2> Instructions </h2>
  For the following cases, replace the numbers 3 & 4 with the numbers you wish to use in the search box.<br>
  The first number is acted on by the second.  e.g. divide/3/4 would be 3 divided by 4.
    <ol>
      <li> For addition use: <a href="add/3/4">add/3/4</a></li>
      <li> For subtraction use: <a href="subtract/3/4">subtract/3/4</a></li>
      <li> For multiplication use: <a href="multiply/3/4">multiply/3/4</a></li>
      <li> For division use: <a href="divide/3/4">divide/3/4</a></li>
    </ol>   
  """
  return page


  # return str([])
def add(*args):
    """ Returns a STRING with the sum of the arguments """

    # TODO: Fill sum with the correct value, based on the
    # args provided.
    sum_val = str(sum(map(int, args)))
    return sum_val

def subtract(*args):
  """ Returns a STRING with the difference of the arguments """
  return str(int(args[0]) - int(args[1]))
  

def multiply(*args):
  """ Returns a STRING with the product of the arguments """
  return str(int(args[0])*int(args[1]))

def divide(*args):
  """ Returns a STRING with the quotient of the arguments """
  return str(int(args[0]) / int(args[1]))

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

    return func, args

def application(environ, start_response):
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
    except ZeroDivisionError:
      status = "400 Bad Request"
      body = "<h1>Divide by zero not allowed</h1>"
    finally:
      headers.append(('Content-length', str(len(body))))
      start_response(status, headers)
      return [body.encode('utf8')]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
