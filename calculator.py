import traceback


def home():
    page = '''
    <h1>Welcome to gerardop's WSGI Calculator App<h1>
    <h2>Addition</h2>
    <p>To add two integers, visit the page http://localhost:8080/add/integer1/integer2, replacing integer1 and integer2 with the integers you wish to add.</p>
    <p>Example: <a href="http://localhost:8080/add/26/21">http://localhost:8080/add/27/20</a></p>
    <h2>Subtraction</h2>
    <p>To subtract two integers, visit the page http://localhost:8080/subtract/integer1/integer2, replacing integer1 and integer2 with the integers you wish to subtract.</p>
    <p>Example: <a href="http://localhost:8080/subtract/100/53">http://localhost:8080/subtract/100/53</a></p>
    <h2>Multiplication</h2>
    <p>To multiply two integers, visit the page http://localhost:8080/multiply/integer1/integer2, replacing integer1 and integer2 with the integers you wish to multiply.</p>
    <p>Example: <a href="http://localhost:8080/multiply/11/15">http://localhost:8080/multiply/11/15</a></p>
    <h2>Division</h2>
    <p>To divide two integers, visit the page http://localhost:8080/divide/integer1/integer2, replacing integer1 and integer2 with the integers you wish to divide.</p>
    <p>Example: <a href="http://localhost:8080/divide/235/5">http://localhost:8080/divide/235/5</a></p>
    '''
    return page


def add(*args):
    """ Returns a STRING with the sum of the arguments """
    sum = str(int(args[0]) + int(args[1]))
    return sum


def subtract(*args):
    """ Returns a STRING with the difference of the arguments """
    difference = str(int(args[0]) - int(args[1]))
    return difference


def multiply(*args):
    """ Returns a STRING with the product of the arguments """
    product = str(int(args[0]) * int(args[1]))
    return product


def divide(*args):
    """ Returns a STRING with the quotient of the arguments """
    quotient = str(int(args[0]) / int(args[1]))
    return quotient


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """
    funcs = {
        '': home,
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
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = '200 OK'
    except NameError:
        status = '404 Not Found'
        body = '<h1>Not Found</h1>'
    except ZeroDivisionError:
        status = '400 Bad Request'
        body = '''<h1>Bad Request</h1>
        <p>Can't divide by 0</p>
        '''
    except Exception:
        status = '500 Internal Server Error'
        body = '<h1>Internal Server Error</h1>'
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
