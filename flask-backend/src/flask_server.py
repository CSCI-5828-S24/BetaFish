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

    def db_setup():
        cursor = mysql.connection.cursor()
        cursor.execute(f'CREATE DATABASE IF NOT EXISTS {os.getenv("MYSQL_DB")}')
        cursor.execute(f'USE {os.getenv("MYSQL_DB")}')
        cursor.execute('SHOW TABLES')
        tables = cursor.fetchall()

        if (len(tables) == 0 or 'crime' not in tables[0]):
            app.logger.info("Recreate crime table")
            table_creation_script = "CREATE TABLE IF NOT EXISTS `crime` (OBJECTID int NOT NULL UNIQUE, INCIDENT_ID double, OFFENSE_ID varchar(20), OFFENSE_CODE varchar(4), OFFENSE_CODE_EXTENSION int, OFFENSE_TYPE_ID varchar(30), OFFENSE_CATEGORY_ID varchar(30), FIRST_OCCURRENCE_DATE long, LAST_OCCURRENCE_DATE long, REPORTED_DATE long, INCIDENT_ADDRESS varchar(100), GEO_X double, GEO_Y double, GEO_LON double, GEO_LAT double, DISTRICT_ID varchar(3), PRECINCT_ID varchar(4), NEIGHBORHOOD_ID varchar(100), IS_CRIME int, IS_TRAFFIC int, VICTIM_COUNT double, PRIMARY KEY (`OBJECTID`));"
            cursor.execute(table_creation_script)

        cursor.execute('SELECT COUNT(*) FROM crime')
        count = cursor.fetchall()
        if (count[0][0] == 0):
            app.logger.info("Initialize crime data")

            app.logger.info("Pull Data from API")

            # TODO: decide the minimum number of rows we want in the table. Minimized due to space in Cloud SQL server
            init_num = 10

            newest = f"https://services1.arcgis.com/zdB7qR0BtYrg0Xpl/ArcGIS/rest/services/ODC_CRIME_OFFENSES_P/FeatureServer/324/query?where=OBJECTID%3E%3D0&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=standard&distance=0.0&units=esriSRUnit_Meter&relationParam=&returnGeodetic=false&outFields=OBJECTID%2C+INCIDENT_ID%2C+OFFENSE_ID%2C+OFFENSE_CODE%2C+OFFENSE_CODE_EXTENSION%2C+OFFENSE_TYPE_ID%2C+OFFENSE_CATEGORY_ID%2C+FIRST_OCCURRENCE_DATE%2C+LAST_OCCURRENCE_DATE%2C+REPORTED_DATE%2C+INCIDENT_ADDRESS%2C+GEO_X%2C+GEO_Y%2C+GEO_LON%2C+GEO_LAT%2C+DISTRICT_ID%2C+PRECINCT_ID%2C+NEIGHBORHOOD_ID%2C+IS_CRIME%2C+IS_TRAFFIC%2C+VICTIM_COUNT&returnGeometry=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&defaultSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=OBJECTID+desc&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount={init_num}&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=standard&f=pjson&token="

            r = requests.post(newest)
            data = r.json()

            values = []
            entries = data['features']
            for row in entries:
                rowdata = list(row["attributes"].values())

                value = "("

                for i in range(len(rowdata)-1):
                    value = value + '"' + str(rowdata[i]) + '", '

                value = value + '"' + str(rowdata[-1]) + '")'

                values.append(value)

            init_query = "INSERT INTO crime VALUES "

            for i in range(len(values)-1):
                init_query = init_query + values[i] + ", "

            init_query = init_query + values[-1]


            app.logger.info("Initialize table data")
            cursor.execute(init_query)

            mysql.connection.commit()

    """
    Hosting web pages from Flask itself
    """
    @app.route('/')
    def index():
        db_setup()
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


            # TODO: Make this actual data the front end can handle and not just an atrocious ongoing string
            stringOut = ""
            for row in raw_data:
                for item in row:
                    stringOut = stringOut + str(item) + ", "
                stringOut = stringOut + "\n"

            response = {
                'data' : stringOut
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

