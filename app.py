from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from json import dumps, loads
from flask_jsonpify import jsonify
import requests


app = Flask(__name__)
api = Api(app)

SECRET_KEY = '1942e6cc2c1e7f6cfcd37551'

CORS(app)

@app.route("/")
def hello():
    return jsonify(Courses.get("529413"))

class Courses(Resource):
    def get(objectId):

        #Main stuff
        #Vi har en reservationlimit på 200, sa vi kan inte kolla för manga kurser eller för stort tidsintervall
        #ett alternativ kan ju vara att bygga schemat en kurs i taget...

        #URL to get schedule for courses based on objectId
        #   https://cloud.timeedit.net/liu/web/schema/ri.html?sid=3&p=190101-190631&objects= XXXXXXXXX, XXXXXXXXX
        #https://cloud.timeedit.net/liu/web/schema/ri.json?sid=3&p=190101-190631&objects= 529413,529626 .txt#formatlinks


        page_url = "https://cloud.timeedit.net/liu/web/schema/ri.json?sid=3&p=190101-190631&objects=" + objectId + ".txt#formatlinks"
        result = requests.get(page_url).text
        data = loads(result)
        return data['reservations'], int(data['info']['reservationcount'])




        #
        api.add_resource(Courses, '/courses') # Route_1
        #api.add_resource(Employees_Name, '/employees/<employee_id>') # Route_3


if __name__=='__main__':

    app.run(debug=True)
