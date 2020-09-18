import re
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

dict_instrs = {
    'instrs': {
        'add_description': 'Add two numbers',
        'add_example': 'http://localhost:8080//add/10/5',
        'subtract_description': 'Subtract two numbers',
        'subtract_example': 'http://localhost:8080//subtract/10/5',
        'multiply_description': 'Multiply two numbers',
        'multiply_example': 'http://localhost:8080/multiply//10/5',
        'divide_description': 'Divide two numbers',
        'divide_example': 'http://localhost:8080/divide//10/5',
    },
    'help1': {
    },
    'help2': {
    },
    'help3': {
    },
}

# DONE: Include usage instructions home page

def calculator_usage_instructions(*args):
    page = """
<h1>"Calculator Usage Instructions:"</h1>
<table>
    <tr><th>Usage: Operator//arg1//arg2</th><td>"site: http://localhost:8080"</td></tr>
    <tr><th>{add_description}</th><td>{add_example}</td></tr>
    <tr><th>{subtract_description}</th><td>{subtract_example}</td></tr>
    <tr><th>{multiply_description}</th><td>{multiply_example}</td></tr>
    <tr><th>{divide_description}</th><td>{divide_example}</td></tr>
</table>
"""
    instrs = dict_instrs['instrs']
    return page.format(**instrs)

# DONE: Include other functions for handling more arithmetic operations.
    
def add(*args):
    """ Returns a STRING with the sum of the arguments """

    # DONE: Fill sum with the correct value, based on the
    # args provided.

    oper_a = args[0]
    oper_b = args[1]
    
    sum = str(int(oper_a) + int(oper_b))

    body = sum
    
    return sum

def multiply(*args):
    """ Returns a STRING with the product of the arguments """

    # DONE: Fill product with the correct value, based on the
    # args provided.

    multiplicand = args[0]
    multiplier = args[1]
    
    product = str(int(multiplicand) * int(multiplier))

    body = product
    
    return product

def subtract(*args):
    """ Returns a STRING with the difference of the arguments """

    # DONE: Fill difference with the correct value, based on the
    # args provided.

    minuend = args[0]
    subtrahend = args[1]
    
    difference = str(int(minuend) - int(subtrahend))

    body = difference
    
    return difference

    
def divide(*args):
    """ Returns a STRING with the difference of the arguments """

    # DONE: Fill quotient with the correct value, based on the
    # args provided.

    dividend = args[0]
    divisor = args[1]
    
    quotient = str(int(dividend) / int(divisor))

    body = quotient
    
    return quotient

    
def resolve_path(path):

    funcs = {
        '': calculator_usage_instructions,
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide,
        
    }

    path = path.strip('/').split('/')

    func_name = path[0]
    args = path[1:]

    # DONE: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
    
    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args

def application(environ, start_response):
    # DONE: Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.

    pass
    
    body = ""
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
    # DONE: Insert the same boilerplate wsgiref simple
    # server creation that you used in the book database.
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
