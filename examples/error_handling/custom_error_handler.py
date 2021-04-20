from flask import Flask
from flask_restx import Resource, Api

app = Flask(__name__)
api = Api(app)

# this will disable flask_restx default error message
# See: https://flask-restx.readthedocs.io/en/latest/errors.html?highlight=ERROR_INCLUDE_MESSAGE#the-api-errorhandler-decorator
app.config['ERROR_INCLUDE_MESSAGE'] = False

# could also be useful
#app.config['ERROR_404_HELP'] = False
#app.config['ERROR_INCLUDE_MESSAGE'] = False
#app.config['RESTX_ERROR_404_HELP'] = False


# you have to define your own Exception as flask_restx doesn't provide them.
class RootException(Exception):
    pass

class NoResultFound(Exception):
    def __init__(self, name_item_not_found):
        self.item_not_found = name_item_not_found

# now define your own errorhandler function with custom handling
@api.errorhandler(RootException)
def handle_root_exception(error):
    '''Return a custom message and 400 status code'''
    return {'message': 'What you want'}, 400

@api.errorhandler(NoResultFound)
def handle_no_result_exception(error):
    '''Return a custom not found error message and 404 status code'''
    return {'message': "your request was not found: '%s'" % error.item_not_found }, 404

# for global 404 error handling, use app decorator:
@app.errorhandler(404)
def handle_wrong_api_URL(e):
    return {'message': "your request was not found: '%s'" % e }, 404

# now your routes
@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        ### something wrong
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

