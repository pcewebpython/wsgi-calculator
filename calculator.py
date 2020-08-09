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
    body = """
        <h1>Calculator Instructions</h1>
        <h3>Enter http://localhost:8080/ <br/>
            Then the operation followed by /<br/>
            Then the two numbers separated by /</h3>
        <ul>
            <li>To add enter a URL like this: 
            <a href="/add/4/8">http://localhost:8080/add/4/8</a></li>
            <li>To subtract enter a URL like this: 
            <a href="/subtract/10/5">http://localhost:8080/subtract/10/5</a></li>
            <li>To multiply enter a URL like this: 
            <a href="/multiply/3/6">http://localhost:8080/multiply/3/6</a></li>
            <li>To divide enter a URL like this: 
            <a href="/divide/20/10">http://localhost:8080/divide/20/10</a></li>
            
    """
    return body


def add(*args):
    """ Returns a STRING with the sum of the arguments """
    try:
        answer = int(args[0])+int(args[1])
        body = f"""
        <h3>The sum of {args[0]} and {args[1]} is: {answer}</h3>
        <a href="/">Return to instructions</a>
        """
    except (ValueError, TypeError):
        body = f"""
        <h3>Unable to add {args[0]} and {args[1]}</h3>
        <a href="/">Return to instructions</a>
        """

    return body


def subtract(*args):
    """ Returns a STRING with the difference of the arguments """
    try:
        answer = int(args[0])-int(args[1])
        body = f"""
        <h3>The difference between {args[0]} and {args[1]} is: {answer}</h3>
        <a href="/">Return to instructions</a>
        """
    except (ValueError, TypeError):
        body = f"""
        <h3>Unable to subtract {args[1]} from {args[0]}</h3>
        <a href="/">Return to instructions</a>
        """

    return body


def multiply(*args):
    """ Returns a STRING with the product of the arguments """
    try:
        answer = int(args[0])*int(args[1])
        body = f"""
        <h3>The product of {args[0]} and {args[1]} is: {answer}</h3>
        <a href="/">Return to instructions</a>
        """
    except (ValueError, TypeError):
        body = f"""
        <h3>Unable to multiply {args[0]} and {args[1]}</h3>
        <a href="/">Return to instructions</a>
        """

    return body


def divide(*args):
    """ Returns a STRING with the dividend of the arguments """
    try:
        answer = int(args[0])/int(args[1])
        body = f"""
        <h3>The dividend of {args[0]} and {args[1]} is: {answer}</h3>
        <a href="/">Return to instructions</a>
        """
    except (ValueError, TypeError):
        body = f"""
        <h3>Unable to divide {args[0]} by {args[1]}</h3>
        <a href="/">Return to instructions</a>
        """
    except ZeroDivisionError:
        body = f"""
        <h3>Unable to divide by 0</h3>
        <a href="/">Return to instructions</a>
        """

    return body

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    funcs = {
        '/': instructions,
        '': instructions,  # if nothing additional in path then show instructions
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide,
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
    status = ""
    body = ""
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
