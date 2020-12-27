"""a simple math application"""
import traceback


def add(*args):
    """ Returns a STRING with the sum of the arguments """

    my_sum = 0
    for my_arg in args:
        my_sum += int(my_arg)
    page = f"""
            <h1>Addition</h1>
            <div>{my_sum}</div>
            <div><a href="/">Back to index</a></div>
            """
    return page


def subtract(*args):
    """subtract input numbers"""

    my_sum = int(args[0])
    sliced_tuple = args[1:]
    print(sliced_tuple)
    for my_arg in sliced_tuple:
        print(my_sum)
        my_sum = my_sum - int(my_arg)
    page = f"""
            <h1>Subtraction</h1>
            <div>{my_sum}</div>
            <div><a href="/">Back to index</a></div>
            """
    return page


def multiply(*args):
    """multiply input numbers"""

    my_sum = int(args[0])
    sliced_tuple = args[1:]
    print(sliced_tuple)
    for my_arg in sliced_tuple:
        print(my_sum)
        my_sum = my_sum * int(my_arg)
    page = f"""
                <h1>Multiplication</h1>
                <div>{my_sum}</div>
                <div><a href="/">Back to index</a></div>
                """
    return page


def divide(*args):
    """divide input numbers"""

    try:
        my_sum = int(args[0])
        sliced_tuple = args[1:]
        print(sliced_tuple)
        for my_arg in sliced_tuple:
            print(my_sum)
            my_sum = my_sum / int(my_arg)
        page = f"""
                    <h1>Division</h1>
                    <div>{my_sum}</div>
                    <div><a href="/">Back to index</a></div>
                    """
    except ZeroDivisionError:
        page = """
        <h1>500 Internal Server Error</h1>
        <h2>Divide by zero error</h2>
        <div><a href="/">Back to index</a></div>
        """
        print(traceback.format_exc())
        return page
    return page


def resolve_path(path):
    """ returns two values: a callable and an iterable of arguments. """

    funcs = {'': index, 'add': add, 'subtract': subtract, 'multiply': multiply, 'divide': divide,}
    path = path.strip('/').split('/')
    func_name = path[0]
    args = path[1:]
    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError
    return func, args


def index():
    """create an entry page for the application"""

    page = """
            <h1>Calculator</h1>
            <div>Directions. This app will calculate 2 or more numbers provided in the url string. To use:
            <ol>
            <li>Type in http://localhost:8080/</li>
            <li>Type in the arithmetic operation (add, subract, multiply, divide) followed by /</li>
            <li>Type in numbers. Between each number include a /</li>
            <li>For example, http://localhost:8080/add/5/10/</li>
            </ol></div>
            <h2>Tests:</h2><ul>
            <li><a href="http://localhost:8080/add/5/10/15">Addition</a></li>
            <li><a href="http://localhost:8080/subtract/100/50/25">Subraction</a></li>
            <li><a href="http://localhost:8080/multiply/5/10/15">Multiplication</a></li>
            <li><a href="http://localhost:8080/divide/100/50">Division</a></li>
            """
    return page


def application(environ, start_response):
    """invoke start_response(status, headers) and
    start the body of the response in BYTE encoding"""

    headers = [("Content-type", "text/html")]
    body = ''
    status = ''
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
