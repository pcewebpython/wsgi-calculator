#Victor Medina
#Assignemnt 4
def empty():
    page = """
<h1>Calculator</h1>
This calculator is able to run the following operands:
<ul>
    <li>add</li>
        <ul>
            <li>Example: Navigate to http://localhost:8080/add/5/10 to view the result of 5 + 10</li>
        </ul>
    <li>subtract</li>
        <ul>
            <li>Example: Navigate to http://localhost:8080/subtract/12/10 to view the result of 12 - 10</li>
        </ul>
    <li>multiply</li>
        <ul>
            <li>Example: Navigate to http://localhost:8080/multiply/35/16 to view the result of 35 x 16</li>
        </ul>
    <li>divide</li>
        <ul>
            <li>Example: Navigate to http://localhost:8080/divide/20/4 to view the result of 20 / 4</li>
        </ul>
</ul>
"""
    return page

def add(*args):
    """ Returns a STRING with the sum of the arguments """


    sum = 0
    for arg in args:
        sum += int(arg)
    return str(sum)
    

def subtract(*args):
    """ Returns a STRING with the difference of the arguments """

    diff = 0
    first = True
    for arg in args:
        if first:
            diff = int(arg)
            first = False
        else:
            diff = diff - int(arg)
    return str(diff)
    

def multiply(*args):
    """ Returns a STRING with the product of the arguments """

    prod = 1
    for arg in args:
        prod *= int(arg)
    return str(prod)
    
    
def divide(*args):
    """ Returns a STRING with the quotient of the arguments """

    quot = 1
    first = True
    for arg in args:
        if first:
            quot = int(arg)
            first = False
        else:
            quot /= int(arg)
    return str(quot)



def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    funcs = {
        '': empty,
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

    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()