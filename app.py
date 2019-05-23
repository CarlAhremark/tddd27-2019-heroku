from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from json import dumps, loads
from flask_jsonpify import jsonify
import requests
import json


app = Flask(__name__)
api = Api(app)

SECRET_KEY = '1942e6cc2c1e7f6cfcd37551'

CORS(app)

@app.route("/")
def hello():
    return jsonify(Courses.get(objectId="529413"))

@app.route("/courselist", methods=['POST'])
def retrieve_courselist():
    courseList = request.form()
    print(courseList)
    return courseList



class Courses(Resource):
    def create_json(raw_data): #Osäker på formateringen om vi ska få den till json, kanske ska vara ' eller "

        count = raw_data['info']['reservationcount']
        json_string = {}


        #print(raw_data['reservations'][0]['startdate'])
        for i in range(count):
            json_string[i] = {}
            title = raw_data['reservations'][i]['columns'][0] + ' <br /> '\
                + raw_data['reservations'][i]['columns'][1] + ' <br /> ' \
                + raw_data['reservations'][i]['columns'][2] + ' <br /> ' \
                + raw_data['reservations'][i]['columns'][3]
            title = title.replace(',', '')

            json_string[i]['start'] =  [\
            raw_data['reservations'][i]['startdate'][0:4]  ,\
            str(int(raw_data['reservations'][i]['startdate'][5:7]) - 1)  ,\
            raw_data['reservations'][i]['startdate'][8:10]  , \
            raw_data['reservations'][i]['starttime'][0:2]  , \
            raw_data['reservations'][i]['starttime'][3:5]]

            json_string[i]['end'] = [\
            raw_data['reservations'][i]['enddate'][0:4]  ,\
            str(int(raw_data['reservations'][i]['enddate'][5:7]) - 1)  ,\
            raw_data['reservations'][i]['enddate'][8:10]  , \
            raw_data['reservations'][i]['endtime'][0:2]  , \
            raw_data['reservations'][i]['endtime'][3:5]]

            json_string[i]['title'] = title

            json_string[i]['color'] = 'color.blue'





        return json_string

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

        #test = Courses.create_json(data)

        return Courses.create_json(data)





        #
        api.add_resource(Courses, '/courses') # Route_1
        #api.add_resource(Employees_Name, '/employees/<employee_id>') # Route_3


if __name__=='__main__':

    app.run(debug=True)
