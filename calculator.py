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

def add(*args):
    """ Returns a STRING with the addition result of the arguments """
    return str(int(args[0]) + int(args[1]))

def sub(*args):
    """ Returns a STRING with the subtraction result of the arguments """
    return str(int(args[0]) - int(args[1]))

def mult(*args):
    """ Returns a STRING with the multiplication result of the arguments """
    return str(int(args[0]) * int(args[1]))

def div(*args):
    """ Returns a STRING with the division result of the arguments """
    return str(int(args[0]) / int(args[1]))

def guide(*args):
    """ Returns a STRING with the instructions for producing a result for the arguments """
    body = "<h1>This is an online calculator</h1>"\
           "To get your result, enter the address in the browser in the following format:\n"\
           "operation/number1/number2 (i.e. add/2/4)"
    return body

def resolve_path(path):
    """
    Returns two values: a callable and an iterable of
    arguments.
    """
    funcs = {
      "":guide,
      "add":add,
      "sum":add,
      "sub":sub,
      "subtract":sub,
      "mult":mult,
      "multiply":mult,
      "div":div,
      "divide":div,
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
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except ZeroDivisionError:
        status = "500 Inernal Server Error"
        body = "<h1>Division by Zero Error</h1>"
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
