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
  http://localhost:8080/               =>
    <html>Here's how to use this page...</html>
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
    final_sum = str(sum(args))
    return final_sum

# TODO: Add functions for handling more arithmetic operations.


def subtract(*args):
    difference = args[0]
    for x in args[1:]:
        difference -= x
    return str(difference)


def divide(*args):
    quotient = args[0]
    for x in args[1:]:
        quotient /= x
    return str(quotient)


def multiply(*args):
    product = 1
    for x in args:
        product *= x
    return str(product)


def instructions():
    page = """
<h1>Here's how to Use this Page!</h1>
<h2>This is a basic calculator that can add, subtract, multiply and divide</h2>
<ul><li>You are going to be using the URL to do math!</li>
<li>First input a math operation eg. add. This will look like 'http://localhost:8080/add/'</li>
<li>Next input as many numbers as you would like to do the operation upon, separated by '/'.</li>
<li>Finally press enter to get the result!</li>
<li>A valid URL would look like 'http://localhost:8080/multiply/3/5/6'</li>
</ul>
  """
    return page


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
    "divide": divide,
    "multiply": multiply,
    "subtract": subtract,
    "": instructions
    }
    path = path.strip('/').split('/')
    func_name = path[0]
    argstrings = path[1:]

    try:
        func = funcs[func_name]
        args = [int(x) for x in argstrings]
    except KeyError:
        raise NameError
    except ValueError:
        raise ValueError
    return func, args


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
        result = func(*args)
        if func.__name__ == 'instructions':
            body = result
        else:
            body = "The result of your request to {} is: {}".format(
                                                        func.__name__, result)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except ValueError:
        status = "400 Bad Request"
        body = "<h1>Unable to do math on strings</h1>"
    except ZeroDivisionError:
        status = "400 Bad Request"
        body = "<h1>Unable to divide by zero</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    # TODO: Insert the same boilerplate wsgiref simple
    # server creation that you used in the book database.
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
