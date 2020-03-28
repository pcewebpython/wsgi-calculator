import traceback

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

def tagged(tag, content, end="\n", **kwargs):
    # Turn kwargs into a collection of usable HTML element attributes.
    # Or leave the attributes empty if nothing is present.
    attrs = " ".join([f"{key}={value}" for key, value in kwargs.items()])
    attrs = f" {attrs}" if len(attrs) > 0 else ""

    return f"<{tag}{attrs}>{content}</{tag}>{end}"


def add(*args):
    """ Returns a STRING with the sum of the arguments """
    total = sum([int(i) for i in args])
    return tagged("h1", f"Your total is: {total}")


def subtract(*args):
    start = int(args[0])
    to_sub = args[1:]

    for number in to_sub:
        start -= int(number)

    return tagged("h1", f"Your total is: {start}")


def multiply(*args):
    start = int(args[0])
    to_mult = args[1:]

    for number in to_mult:
        start *= int(number)

    return tagged("h1", f"Your total is: {start}")


def divide(*args):
    start = int(args[0])
    to_divide = args[1:]

    for number in to_divide:
        start /= int(number)

    return tagged("h1", f"Your total is: {start}")


def index(*args):
    title = tagged("h1", "WSGI Calculator")
    detail = tagged("p", str("This website will help you calculate numbers.  "
                             "Simply navigate to the operation you want to "
                             "perform and the numbers you want to calculate "
                             "against.  Try one of the examples below."))
    example_text = tagged("h3", "Examples:")
    table = []
    examples = {"add": f"{args[0]}/add/4/5",
                "subtract": f"{args[0]}/subtract/-7/10",
                "multiply": f"{args[0]}/multiply/2/7",
                "divide": f"{args[0]}/divide/20/5"}

    for key, value in examples.items():
        anchor = tagged("a", value, end="", href=value)
        row = tagged("th", key, end="") + tagged("td", anchor, end="")
        table.append(tagged("tr", row))
    
    table = tagged("table", "".join(table))
    return "".join([title, detail, example_text, table])


def resolve_path(path, environ_host):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    # TODO: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
    functions = {"add": add,
                 "subtract": subtract,
                 "multiply": multiply,
                 "divide": divide}

    if path == "/":
        func = index
        args = [environ_host]
    else:
        path = path.strip('/').split('/')
        name = path[0]
        args = path[1:]

        func = functions.get(name)

        if not func:
            raise NameError

    return func, args


def application(environ, start_response):
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get("PATH_INFO", None)
        if not path:
            raise NameError
        function, args = resolve_path(path, environ["HTTP_HOST"])
        body = function(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = tagged("h1", "Not Found")
    except ZeroDivisionError:
        status = "400 Bad Request"
        body = tagged("h1", "Cannot Divide By Zero")
    except Exception:
        status = "500 Internal Server Error"
        body = tagged("h1", "Internal Server Error")
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode("utf8")]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
