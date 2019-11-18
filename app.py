# this app.py represents web server that listens to client and send back response to client.
# after this server is running, one way to test how this server works is: type "curl -X POST http://127.0.0.1:5000/ -i" and it will show response from this server.
# This file is one file that leads to everything else.
# import Flask
from flask import Flask, render_template, request
from flask.json import jsonify
import boto3
from boto3.dynamodb.conditions import Key, Attr
from functools import reduce
import Load
import Clear

# create an instance of Flask class.
# placeholder for the current module. In this case, application.py
app = Flask(__name__)

# create a route. route is slash.
# normally, you'll return a template called index.html. not just string like 'INDEX'.
# we can use a function called render_template, but that has to be imported from flask as well.
@app.route('/')
def index():
    # return 'INDEX'
    return render_template('index.html')


@app.route('/load', methods=['POST'])
def loadData():
    print("load received")
    Load.copyFromOtherS3ToMyS3andLoadToDB()
    response = app.response_class(status=200)

    return response


@app.route('/clear', methods=['DELETE'])
def clearData():
    print("clear received")

    Clear.deleteS3File()

    result = Clear.delete_DB_Table()
    if result == "failed":
        response = app.response_class(status=400)
    else:
        response = app.response_class(status=200)
    print(response)
    return response

# first get data from danamodb using lastname,firstname.
@app.route('/queryData', methods=['GET'])
def queryData():

    print("query received")
    first_name = request.args['arg1']
    last_name = request.args['arg2']

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('yunTable')

    if first_name or last_name:
        key_fn = ''
        key_ln = ''
        if first_name:
            key_fn = Attr('first_name').eq(first_name)
        else:
            key_fn = Attr('first_name').exists()
        if last_name:
            key_ln = Attr('last_name').eq(last_name)
        else:
            key_ln = Attr('last_name').exists()
        response = table.scan(
            FilterExpression=key_fn & key_ln
        )

    if not 'Items' in response:
        return jsonify([])
    items = response['Items']
    print(items)

    return jsonify(items)
    # return "param " + arg1 + arg2 I can return text like "param " + arg1 + arg2 or I also can return Json. if I return Json here, index.html js will have to use JSON.parse


# at the very bottom, test to see if that value that __name__ value is equal to __main. because that means it's the script that's going to be executed.
# if condition is met, then just run the application. so this code here will actually start the application.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)


# when you type python3 application.py in terminal, you will see it started running on port 5000. (= web server is running)
# so if you go to web browser and type "localhost:5000" in address bar, Initially, you will get Not Found page. The reason is because
# we haven't created a route for our home, our index, so let's add @app.route('/')
