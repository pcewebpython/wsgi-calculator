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
import re
import traceback
import pdb

def how_to_index():
    index = """
    <html>
    <head><basic Calculator</title></head>
    <h1>Calculator</h1>
    <h2>multiply</h2>
   <p> <a href="http://localhost:8080/multiply/3/5">http://localhost:8080/multiply/3/5</a>   => 15 </p>
   <h2>Addition</h2>
   <p> <a href="http://localhost:8080/add/23/42">http://localhost:8080/add/23/42</a>      => 65 </p>
   <h2>subtract</h2>
   <p> <a href="http://localhost:8080/subtract/23/42">http://localhost:8080/subtract/23/42</a> => -19 </p>
   <h2>divide</h2>
   <p> <a href="http://localhost:8080/divide/22/11">http://localhost:8080/divide/22/11</a>  => 2 </p>
   <h2>main</h2>
   <p> <a href="http://localhost:8080">http://localhost:8080</a> => Here's how to use this page.. </p>
    </html>
    """
    return index



def add(*args):
    """ Returns a STRING with the sum of the arguments """

    # TODO: Fill sum with the correct value, based on the
    # args provided.
    page = """<html>
    <head>
        <title>Addition</title>
    </head>
        <body>
       <table>
    <tr><th>Addition of {} and {} is = </th><td>{}</td></tr>
    </table>
<a href="/">Back to the list</a>
    </body>
</html>"""
 

    nums = []
    for arg in args:
        nums.append(arg)
    sum_nums = int(nums[0])+int(nums[1])
    #pdb.set_trace()
    return page.format(*args,str(sum_nums))


def multiply(*args):
    """ Returns a STRING with the sum of the arguments """

    # TODO: Fill sum with the correct value, based on the
    # args provided.
    page = """<html>
    <head>
        <title>Multiplication</title>
    </head>
        <body>
       <table>
    <tr><th>Multiplication of {} and {} is = </th><td>{}</td></tr>
    </table>
<a href="/">Back to the list</a>
    </body>
</html>"""
    nums = []
    for arg in args:
        nums.append(arg)
    mul_nums = int(nums[0])*int(nums[1])
    #pdb.set_trace()
    return page.format(*args, str(mul_nums))


def subtract(*args):
    """ Returns a STRING with the sum of the arguments """

    # TODO: Fill sum with the correct value, based on the
    # args provided.
    page = """<html>
    <head>
        <title>Subtraction</title>
    </head>
        <body>
       <table>
    <tr><th>Subtraction of {} and {} is = </th><td>{}</td></tr>
    </table>
<a href="/">Back to the list</a>
    </body>
</html>"""
    nums = []
    for arg in args:
        nums.append(arg)
    subtra_nums = int(nums[0])-int(nums[1])
    #pdb.set_trace()
    return page.format(*args, str(subtra_nums))


def divide(*args):
    """ Returns a STRING with the sum of the arguments """

    # TODO: Fill sum with the correct value, based on the
    # args provided.
    page = """<html>
    <head>
        <title>Division</title>
    </head>
        <body>
       <table>
    <tr><th>Division of {} and {} is = </th><td>{}</td></tr>
    </table>
<a href="/">Back to the list</a>
    </body>
</html>"""
    nums = []
    for arg in args:
        nums.append(arg)
    div_nums = int(nums[0])/int(nums[1])
    #pdb.set_trace()
    return page.format(*args, str(div_nums))

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
        '': how_to_index,
        'add': add,
        'multiply': multiply,
        'subtract': subtract,
        'divide': divide,
    }

    path = path.strip('/').split('/')
    func_name = path[0]
    args = path[1:]
    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError
    # if len(args) != 2:
    #     raise NotImplementedError("Exactly two arguments are allowed")


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
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not found"
        body = "<h1>Not found</h1>"
    except Exception:
        status = "500 Internal server Error"
        body = "<h1>Internal server Error</h1>"
        print(traceback.format_exc())
    # except NotImplementedError():
    #     status = "501 Not implemented"
    #     body = "<h1>Not implemented</h1>"
    #     print(traceback.format_exc())
    finally:
        headers.append(('content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    # TODO: Insert the same boilerplate wsgiref simple
    # server creation that you used in the book database.
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
