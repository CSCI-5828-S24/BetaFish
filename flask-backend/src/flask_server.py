from functools import cmp_to_key
from flask import Flask, request, Response, g
from flask_cors import CORS
import jsonpickle
import os, time
import prometheus_client
from prometheus_client.metrics import Histogram, Counter

import logging
logging.basicConfig(level=logging.DEBUG)

import mysql.connector
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__, static_folder="../../react-frontend/build", static_url_path='/')
CORS(app, origins=["*"])

def create_app(graph:dict={}):
    _INF = float("inf")
    app = Flask(__name__, static_folder="../../react-frontend/build", static_url_path='/')

    app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST")
    app.config['MYSQL_USER'] = os.getenv("MYSQL_USER")
    app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD")
    app.config['MYSQL_DB'] = os.getenv("MYSQL_DB")

    if 'count' not in graph.keys():
        graph['count'] = Counter('total_req', 'total requests on all paths')
    if 'analytics_latency' not in graph.keys():
        graph['analytics_latency'] = Histogram('analytics_latency', 'Latency for anaytics API', buckets=(100, 200, 300, _INF))
    if 'data_latency' not in graph.keys():
        graph['data_latency'] = Histogram('data_latency', 'Latency for data API', buckets=(100, 200, 300, _INF))
    
    def getDB():
        if 'db' not in g or not g.db.is_connected():
            g.db = mysql.connector.connect(
                host=os.getenv("MYSQL_HOST"),
                user=os.getenv("MYSQL_USER"),
                port=os.getenv("MYSQL_PORT", "3306"),
                password=os.getenv("MYSQL_PASSWORD"),
                database=os.getenv("MYSQL_DB")
            )
        return g.db;
    # mysql = MySQL(app)
    

    """
    Hosting web pages from Flask itself
    """
    @app.route('/')
    def index():
        graph['count'].inc()
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
                'error' : error,
                'data': False
            }
            status = 500
        response_pickled = jsonpickle.encode(response)
        graph['count'].inc()
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
    
    @app.route('/api/crime_freq', methods=["GET"])
    def get_crime_freq():
        start = time.time_ns()
        graph['count'].inc()
        status = 200
        try:
            mydb = getDB()
            cursor = mydb.cursor()
            queryToExecute = f"SELECT * FROM crime_freq"
            # print(queryToExecute)
            cursor.execute(queryToExecute)
            raw_data = cursor.fetchall()
            row_headers = [x[0] for x in cursor.description]
            json_data = []

            for r in raw_data:
                json_data.append(dict(zip(row_headers, r)))
            
            json_data = sorted(json_data, key=cmp_to_key(lambda x1, x2: x1['DAY'] - x2['DAY']))
            response = {
                'data' : json_data
            }
            
        except Exception as error:
            response = { 
                'error' : error,
                'data': []
            }
            status = 500
        response_pickled = jsonpickle.encode(response)
        graph['analytics_latency'].observe((time.time_ns() - start) // 1000000)
        return Response(response=response_pickled, status=status, mimetype='application/json')
    
    @app.route('/api/crime_totals', methods=["GET"])
    def get_crime_totals():
        start = time.time_ns()
        graph['count'].inc()
        status = 200
        try:
            mydb = getDB()
            cursor = mydb.cursor()
            queryToExecute = "SELECT * FROM crime_totals"
            #print(queryToExecute)
            cursor.execute(queryToExecute)
            raw_data = cursor.fetchall()
            row_headers = [x[0] for x in cursor.description]
            json_data = []

            for r in raw_data:
                json_data.append(dict(zip(row_headers, r)))
            
            json_data = sorted(json_data, key=cmp_to_key(lambda x1, x2: x2['COUNT'] - x1['COUNT']))
            response = {
                'data' : json_data
            }
        except Exception as error:
            response = { 
                'error' : error,
                'data' : []
            }
            status = 500
        response_pickled = jsonpickle.encode(response)
        graph['analytics_latency'].observe((time.time_ns() - start) // 1000000)
        return Response(response=response_pickled, status=status, mimetype='application/json')

    @app.route('/api/alldata', methods=["GET"])
    def get_all():
        status = 200
        start = time.time_ns()
        graph['count'].inc()
        try:
            mydb = getDB()
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
            cursor = mydb.cursor()
            queryToExecute = f"SELECT * FROM crime WHERE REPORTED_DATE < {endTime} AND REPORTED_DATE > {startTime} ORDER BY (POWER(GEO_LAT-{lat}, 2)+POWER(GEO_LON-{long}, 2)) LIMIT {pagesize} OFFSET {(pageno-1)*pagesize}"
            # print(queryToExecute)
            cursor.execute(queryToExecute)
            raw_data = cursor.fetchall()
            row_headers = [x[0] for x in cursor.description]
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
                'error' : error,
                'data': [],
                'pageno': 0,
                'pagesize': 0
            }
            status = 500
        response_pickled = jsonpickle.encode(response)
        graph['data_latency'].observe((time.time_ns() - start) // 1000000)
        return Response(response=response_pickled, status=status, mimetype='application/json')

    @app.route('/metrics', methods=["GET"])
    def get_metrics():
        res = []
        for k,v in graph.items():
            res.append(prometheus_client.generate_latest(v))
        return Response(res, mimetype='text/plain')
    
    return app


def main():
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)

if __name__ == "__main__":
    main()

