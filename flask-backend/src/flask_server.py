from flask import Flask, request, Response
from flask_cors import CORS
import jsonpickle
import os

import logging
logging.basicConfig(level=logging.DEBUG)

import mysql.connector
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__, static_folder="../../react-frontend/build", static_url_path='/')
CORS(app, origins=["*"])

def create_app():
    app = Flask(__name__, static_folder="../../react-frontend/build", static_url_path='/')


    app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST")
    app.config['MYSQL_USER'] = os.getenv("MYSQL_USER")
    app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD")
    app.config['MYSQL_DB'] = os.getenv("MYSQL_DB")
 
    mydb = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        port=os.getenv("MYSQL_PORT", "3306"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB")
    )
    # mysql = MySQL(app)
    

    """
    Hosting web pages from Flask itself
    """
    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    """
    Health check endpoint for getting status of api
    """
    @app.route('/api/health', methods=["GET"])
    def health():
        status = 200
        try:
            response = {
                'data' : True
            }
        except Exception as error:
            response = {
                'error' : error 
            }
            status = 500
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=status, mimetype='application/json')

    # @app.route('/api/multiply/<int:x>/<int:y>', methods=["GET"])
    # def multiply(x, y):
    #     status = 200
    #     try:
    #         response = {
    #             'data' : x * y
    #         }
    #     except Exception as error:
    #         response = { 
    #             'error' : error 
    #         }
    #         status = 500
    #     response_pickled = jsonpickle.encode(response)
    #     return Response(response=response_pickled, status=status, mimetype='application/json')
    
    # @app.route('/api/crime_freq', methods=["GET"])
    # def get_crime_freq():
    #     status = 200
    #     try:
    #         cursor = mydb.cursor()
    #         timeToFilter = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) - relativedelta(days=29)
    #         reportedDateFilter = int(time.mktime(timeToFilter.timetuple()) * 1000)
    #         cursor.execute(f"select floor((REPORTED_DATE - {reportedDateFilter}) / 86400000) as day, count(*) as crimes_reported from crime group by 1")
    #         raw_data = cursor.fetchall()
    #         row_headers = [x[0] for x in cursor.description]
    #         print(row_headers)
    #         json_data = []

    #         for r in raw_data:
    #             if(int(r[0]) < 0):
    #                 continue
    #             json_data.append({
    #                 'day': int(r[0]),
    #                 'crimes': r[1]
    #             })
            
    #         added_json_data = []
    #         for i in range(0,30):
    #             found = False
    #             for r in json_data:
    #                 if i == r['day']:
    #                     found = True
    #                     break
    #             if not found:
    #                 added_json_data.append({
    #                     'day': i,
    #                     'crimes': 0
    #                 })
    #         json_data = json_data + added_json_data
    #         json_data = sorted(json_data, key=cmp_to_key(lambda x1, x2: x1['day'] - x2['day']))
    #         response = {
    #             'data' : json_data
    #         }
            
    #         print(response)
    #     except Exception as error:
    #         response = { 
    #             'error' : error 
    #         }
    #         status = 500
    #     response_pickled = jsonpickle.encode(response)
    #     return Response(response=response_pickled, status=status, mimetype='application/json')
    
    # @app.route('/api/crime_totals', methods=["GET"])
    # def get_crime_totals():
    #     status = 200
    #     try:
    #         cursor = mydb.cursor()
    #         cursor.execute("SELECT * FROM crime")
    #         raw_data = cursor.fetchall()
    #         row_headers = [x[0] for x in cursor.description]
    #         print(row_headers)
    #         json_data = []

    #         for r in raw_data:
    #             json_data.append(dict(zip(row_headers, r)))
            
    #         totals = {}
    #         for item in json_data:
    #             crime_category = item["OFFENSE_CATEGORY_ID"]
    #             if (crime_category not in totals): totals[crime_category] = 1
    #             else: totals[crime_category] += 1

    #         response = {
    #             'data' : totals
    #         }
    #     except Exception as error:
    #         response = { 
    #             'error' : error 
    #         }
    #         status = 500
    #     response_pickled = jsonpickle.encode(response)
    #     return Response(response=response_pickled, status=status, mimetype='application/json')

    @app.route('/api/alldata', methods=["GET"])
    def get_all():
        status = 200
        try:
            pageno = int(request.args["pageno"])
            if pageno <= 0:
                pageno = 1
            pagesize = int(request.args["pagesize"])
            if pagesize <= 5:
                pagesize = 5
            lat = float(request.args["lat"])
            long = float(request.args["long"])
            startTime = int(request.args["startTime"])
            endTime = int(request.args["endTime"])
            print("reached")
            cursor = mydb.cursor()
            queryToExecute = f"SELECT * FROM crime WHERE REPORTED_DATE < {endTime} AND REPORTED_DATE > {startTime} ORDER BY (POWER(GEO_LAT-{lat}, 2)+POWER(GEO_LON-{long}, 2)) LIMIT {pagesize} OFFSET {(pageno-1)*pagesize}"
            print(queryToExecute)
            cursor.execute(queryToExecute)
            raw_data = cursor.fetchall()
            row_headers = [x[0] for x in cursor.description]
            print(row_headers)
            json_data = []

            for r in raw_data:
                json_data.append(dict(zip(row_headers, r)))


            # TODO: Make this actual data the front end can handle and not just an atrocious ongoing string
            # stringOut = ""
            # for row in raw_data:
            #     for item in row:
            #         stringOut = stringOut + str(item) + ", "
            #     stringOut = stringOut + "\n"

            response = {
                'data' : json_data,
                'pageno': pageno,
                'pagesize': pagesize
            }
        except Exception as error:
            response = { 
                'error' : error 
            }
            status = 500
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=status, mimetype='application/json')
    
    return app


def main():
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)

if __name__ == "__main__":
    main()

