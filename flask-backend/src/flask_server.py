from flask import Flask, request, Response
from flask_cors import CORS
import requests
import jsonpickle
import os
import sys

import logging
logging.basicConfig(level=logging.DEBUG)

from flask_mysqldb import MySQL
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
 
    mysql = MySQL(app)

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

    @app.route('/api/multiply/<int:x>/<int:y>', methods=["GET"])
    def multiply(x, y):
        status = 200
        try:
            response = {
                'data' : x * y
            }
        except Exception as error:
            response = { 
                'error' : error 
            }
            status = 500
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=status, mimetype='application/json')
    

    @app.route('/api/alldata', methods=["GET"])
    def get_all():
        status = 200
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM crime")
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
                'data' : json_data
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

