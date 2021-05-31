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
"""

op_output = 'Your Answer is: '

def operations():
  """ Returns a STRING with instructions """
  body = [
    '<title>WSGI Calculator</title>',
    '<h1>Operations</h1>',
    '<p1>Select an operation. Then append the web address with /(any number you want)/(any number you want)</p1>',
    '<ul>']

  ops = ['Add','Subtract','Multiply','Divide']

  item_template = '<li><a href="/{0}">{1}</a></li>'

  for item in ops:
    body.append(item_template.format(item.lower(),item))
  body.append('</ul>')

  return '\n'.join(body)

def add(*args):
    """ Returns a STRING with the sum of the arguments """

    sum = 0

    for item in args:
      sum += int(item)

    return op_output + str(sum)

def subtract(*args):
    """Return a STRING with the difference of the arguments"""
    in_list = [int(x) for x in args]

    try:
      diff = in_list.pop(0)
    except IndexError:
      diff = 0

    for item in in_list:
      diff -= item

    return op_output + str(diff)

def multiply(*args):
   """Return a STRING with the product of the arguments"""
   in_list = [int(x) for x in args]
   try:
      prod = in_list.pop(0)
   except IndexError:
     prod = 0

   for item in in_list:
     prod *= item

   return op_output + str(prod)

def divide(*args):
   """Return a STRING with quotent of the arguments""" 
   in_list = [int(x) for x in args]

   try:
      quot = in_list.pop(0)
   except IndexError:
      quot = 0

   if 0 in in_list:
     raise ValueError

   for item in in_list:
     quot /= item

   return op_output +  str(quot)

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    # TODO: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.

    funcs = {
        '' : operations,
        'add' : add,
        'subtract': subtract,
        'multiply': multiply,
        'divide' : divide,
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
        status = "404 Not Found"
        body = "<h1> Not Found </h1>"
    except ValueError:
        status = "400 Bad Request"
        body = "<h1>Bad Request</h1>"
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
