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


def add(*args):
    """ Returns a STRING with the sum of the arguments """

    # TODO: Fill sum with the correct value, based on the
    # args provided.
    sum = "0"

    return sum

# TODO: Add functions for handling more arithmetic operations.

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    # TODO: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
    funcs = {'':index, 'add':add, 'multiply':multiply, 'subtract':subtract, 'divide':divide}
    path = path.strip('/').split('/')
    operation = path[0]
    # args  = [path[1], path[2]]
    args = path[1:]
    try:
        func = funcs[operation]
    except KeyError:
        raise NameError
    return func, args

def index():
    body = """
    <h3>Calculator, how to use</h3>
    <p>http://localhost:8080/multiply/3/5 =&gt; 15<br />
    http://localhost:8080/add/23/42 =&gt; 65<br />
    http://localhost:8080/subtract/23/42 =&gt; -19<br />
    http://localhost:8080/divide/22/11 =&gt; 2</p>
    """
    return body

def add(*args):
    result = sum(map(int,args))
    body = '<h1>{} added to {} = {}</h1>'.format(args[0],args[1],result)
    return body


def multiply(*args):
    result = int(args[0]) * int(args[1])
    body = '<h1>{} Multiply by {} = {}</h1>'.format(args[0],args[1],result)
    return body


def subtract(*args):
    result = int(args[0]) - int(args[1])
    body = '<h1>{} subtract by {} = {}</h1>'.format(args[0],args[1],result)
    return body

def divide(*args):
    result = int(args[0]) / int(args[1])
    body = '<h1>{} divide by {} = {}</h1>'.format(args[0],args[1],result)
    return body


def application(environ, start_response):
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
        status = '404 Not Found'
        body = "<h1>Not Found</h1>"
    except ZeroDivisionError:
        status = '406 Not Acceptable'
        body = "Can divide {} by {} - ZeroDivisionError".format(args[0],args[1])
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())


    finally:
        headers.append(('Content-type', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()