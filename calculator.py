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

def html_wrapper(body):
    result = f"""
<html>
<head><title>Calculator</title></head>
<body>
{body}
</body>
</html>
"""
    return result

def instructions(*args):
    """Index page"""
    page = """
<h1>Calculator</h1>

<h2>Instructions:</h2>

<ul>
    <li>To access the calculator function in your browser enter http://localhost:8080/.</li> 
    <li>Enter in the operation you wish to use after the slash "/": Add, Subtract, Multiply, or divide.</li>
    <li>After the operation enter slash "/" and the first number in the operation.</li>
    <li>Enter another slash "/" followed by the second number in the operation.</li>
    <li>Press Enter.</li>
</ul>

<h2>Examples:</h2>

<table>
    <tr>
        <th>Operation</th>
        <th>Example Link</th>
    </tr>
    <tr>
        <td>Add</td>
        <td><a href="http://localhost:8080/add/23/42">http://localhost:8080/add/23/42</a></td>
    </tr>
    <tr>
        <td>Subtract</td>
        <td><a href="http://localhost:8080/subtract/23/42">http://localhost:8080/subtract/23/42</a></td>
    </tr>
    <tr>
        <td>Multiply</td>
        <td><a href="http://localhost:8080/multiply/3/5">http://localhost:8080/multiply/3/5</a></td>
    </tr>
    <tr>
        <td>Divide</td>
        <td><a href="http://localhost:8080/divide/22/11">http://localhost:8080/divide/22/11</a></td>
    </tr>
</table>

"""
    return page


def add(*args):
    """ Returns a STRING with the sum of the arguments """

    # TODO: Fill sum with the correct value, based on the
    # args provided.
    # sum = "0"
    result = str(sum(args))
    result += '</br><a href="/">Back</a>'
    return result

# TODO: Add functions for handling more arithmetic operations.


def subtract(*args):
    """Returns a string with the result a-b"""

    result = str(args[0] - args[1])
    result += '</br><a href="/">Back</a>'

    return result

def divide(*args):
    """Return a string with the result of """
    try:
        result = str(args[0] / args[1])

    except ZeroDivisionError:
        result = "You can't divide by zero"
    result += '</br><a href="/">Back</a>'

    return result

def multiply(*args):
    """Returns the result of a*b"""
    
    result = str(args[0] * args[1])
    result += '</br><a href="/">Back</a>'

    return result


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    # TODO: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
    # func = add
    # args = ['25', '32']

    funcs = {
            "add": add, 
            "subtract": subtract,
            "multiply": multiply,
            "divide": divide, 
            "instructions" : instructions
            }
    # print(f"!{path}!")
    if "favicon.ico" in path or len(path) < 7:
        func_name = "instructions"
        left = "0"
        right = "0"
    else:
        func_name, left, right = path.split('/')[1:4]

    args = [int(left), int(right)]

    try:
      func = funcs[func_name]
    except KeyError:
      raise NameError

    return func, args

def application(environ, start_response):
    # TODO: Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.
    #
    # TODO (bonus): Add error handling for a user attempting
    # to divide by zero.
    # pass

    status = "200 OK"
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        func, args = resolve_path(path)
        body = html_wrapper(func(*args))
    except NameError:
        status = "404 Not Found"
        body = html_wrapper("<h1>Not Found</h1>")
    except Exception:
        status = "500 Internal Server Error"
        body = html_wrapper("<h1>Internal Server Error</h1>")
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    # TODO: Insert the same boilerplate wsgiref simple
    # server creation that you used in the book database.
    # pass
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()