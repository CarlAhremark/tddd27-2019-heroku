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
    return jsonify(Courses.get())


class Employees(Resource):
    def get(self, id="0"):
        print("id is: ",id)
        if (id =="1"):
            return {'employees':{'id':1, 'name':'Balram'}}
        elif (id == "2"):
            return  {'employees':{'id':2, 'name':'Tom'}}
        else:
            return {'employees': [{'id':1, 'name':'Balram'},{'id':2, 'name':'Tom'}]}

class Employees_Name(Resource):
    def get(self, employee_id):
        print('Employee id:' + employee_id)
        result = Employees.get(self, str(employee_id))
        print(result)

        return jsonify(result)

class Courses(Resource):
    def get():
        #Useful functions
        def create_json(raw_data): #Osäker på formateringen om vi ska få den till json, kanske ska vara ' eller " 
            test = raw_data
            count = test['info']['reservationcount']
            json_string = "["

            for i in range(3): #count instead of integer
                title = raw_data['reservations'][i]['columns'][0] + " Location " \
                    + raw_data['reservations'][i]['columns'][1] + " " \
                    + raw_data['reservations'][i]['columns'][2] + " " \
                    + raw_data['reservations'][i]['columns'][3]
                title = title.replace(',', ' ')
                if (i == 0):
                    json_string += f"{{ startdate: {test['reservations'][i]['startdate']}, "\
                        f"starttime: {test['reservations'][i]['starttime']}, "\
                        f"enddate: {test['reservations'][i]['enddate']}, "\
                        f"endtime: {test['reservations'][i]['endtime']}, "\
                        f"title: {title}, "\
                        f"color: color.yellow, "\
                        f"actions: this.actions }}"
                else:
                    json_string += f",{{ startdate: {test['reservations'][i]['startdate']}, "\
                        f"starttime: {test['reservations'][i]['starttime']}, "\
                        f"enddate: {test['reservations'][i]['enddate']}, "\
                        f"endtime: {test['reservations'][i]['endtime']}, "\
                        f"title: {title}, "\
                        f"color: color.yellow, "\
                        f"actions: this.actions }}"


            json_string += "];"
            return json_string

        #Main stuff
        #Vi har en reservationlimit på 200, så vi kan inte kolla för många kurser eller för stort tidsintervall
        #ett alternativ kan ju vara att bygga schemat en kurs i taget...
        
        obj = ["529413","515157"] #Byt den adra till 529626
        object_names = ""
        #URL to get schedule for courses based on objectId
        #   https://cloud.timeedit.net/liu/web/schema/ri.html?sid=3&p=190101-190631&objects= XXXXXXXXX, XXXXXXXXX
        #https://cloud.timeedit.net/liu/web/schema/ri.json?sid=3&p=190101-190631&objects= 529413,529626 .txt#formatlinks

        for objectid in obj:
            if object_names == "":
                object_names += objectid
            else:
                object_names += ',' + objectid
            

        page_url = "https://cloud.timeedit.net/liu/web/schema/ri.json?sid=3&p=190101-190631&objects=" + object_names + ".txt#formatlinks"

        print(page_url)
        result = requests.get(page_url).text
        test = loads(result)
        print("test containts: ", test['reservations'][0])
        print("Reservationcount: ", test['info']['reservationcount'])
        json_string = create_json(test)
        print("json_string: ",json_string)

        data = dumps(result)
        


        return  data

 


        # page_raw = urlopen(url=page_url)
        # page = BeautifulSoup(page_raw,'html.parser')
        # page_box = page.find('table', attrs={'class': 'restable'})
        # print(page_box.read())


api.add_resource(Employees, '/employees') # Route_1
api.add_resource(Employees_Name, '/employees/<employee_id>') # Route_3


if __name__ == '__main__':
   app.run(port=5006)
