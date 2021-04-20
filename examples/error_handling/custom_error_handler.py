from flask import Flask
from flask_restx import Resource, Api

app = Flask(__name__)
api = Api(app)


# you have to define your own Exception as flask_restx doesn't provide them.
class NoResultFound(Exception):
    pass

class RootException(Exception):
    pass

class CustomException(Exception):
    pass

class AnotherException(Exception):
    pass

class FakeException(Exception):
    pass

class NoResultFound(Exception):
    def __init__(self, name_item_not_found):
        self.item_not_found = name_item_not_found

# now define your own errorhandler function with custom handling
@api.errorhandler(RootException)
def handle_root_exception(error):
    '''Return a custom message and 400 status code'''
    return {'message': 'What you want'}, 400       

@api.errorhandler(CustomException)
def handle_custom_exception(error):
    '''Return a custom message and 400 status code'''
    return {'message': 'What you want'}, 400

@api.errorhandler(AnotherException)
def handle_another_exception(error):
    '''Return a custom message and 500 status code'''
    return {'message': error.specific}

@api.errorhandler(FakeException)
def handle_fake_exception_with_header(error):
    '''Return a custom message and 400 status code'''
    return {'message': error.message}, 400, {'My-Header': 'Value'}

@api.errorhandler(NoResultFound)
def handle_no_result_exception(error):
    '''Return a custom not found error message and 404 status code'''
    return {'message': "your request was not found: '%s'" % error.item_not_found }, 404        
    

# now your routes
@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        ### somthing wrong
        raise RootException

@api.route('/does_it_exist/<string:file_name>')
class HelloWorld(Resource):
    def get(self, file_name):
        if file_name != 'yes':                
            raise NoResultFound(file_name)
        else:
            return { 'file_found': file_name }

if __name__ == '__main__':
    app.run(debug=True)

