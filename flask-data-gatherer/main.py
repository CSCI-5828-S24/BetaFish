import functions_framework
import requests
import os
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

import logging
logging.basicConfig(level=logging.DEBUG)

import mysql.connector
from dotenv import load_dotenv

@functions_framework.http
def collect(request):
    load_dotenv()

    mydb = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD")
    )
    # mysql = MySQL(app)

    cursor = mydb.cursor()
    cursor.execute(f'CREATE DATABASE IF NOT EXISTS {os.getenv("MYSQL_DB")}')
    cursor.execute(f'USE {os.getenv("MYSQL_DB")}')
    cursor.execute('SHOW TABLES')
    tables = cursor.fetchall()

    if (len(tables) == 0 or 'crime' not in tables[0]):
        table_creation_script = "CREATE TABLE IF NOT EXISTS `crime` (OBJECTID int NOT NULL UNIQUE, INCIDENT_ID double, OFFENSE_ID varchar(20), OFFENSE_CODE varchar(4), OFFENSE_CODE_EXTENSION int, OFFENSE_TYPE_ID varchar(30), OFFENSE_CATEGORY_ID varchar(30), FIRST_OCCURRENCE_DATE long, LAST_OCCURRENCE_DATE long, REPORTED_DATE BIGINT NOT NULL, INCIDENT_ADDRESS varchar(100), GEO_X double, GEO_Y double, GEO_LON double, GEO_LAT double, DISTRICT_ID varchar(3), PRECINCT_ID varchar(4), NEIGHBORHOOD_ID varchar(100), IS_CRIME int, IS_TRAFFIC int, VICTIM_COUNT double, PRIMARY KEY (`OBJECTID`));"
        cursor.execute(table_creation_script)

    cursor.execute("DELETE FROM crime")
    cursor.execute('SELECT COUNT(*) FROM crime')
    count = cursor.fetchall()
    if (count[0][0] == 0):
        # TODO: decide the minimum number of rows we want in the table. Minimized due to space in Cloud SQL server
        init_num = 10000

        newest = f"https://services1.arcgis.com/zdB7qR0BtYrg0Xpl/ArcGIS/rest/services/ODC_CRIME_OFFENSES_P/FeatureServer/324/query?where=OBJECTID%3E%3D0&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=standard&distance=0.0&units=esriSRUnit_Meter&relationParam=&returnGeodetic=false&outFields=OBJECTID%2C+INCIDENT_ID%2C+OFFENSE_ID%2C+OFFENSE_CODE%2C+OFFENSE_CODE_EXTENSION%2C+OFFENSE_TYPE_ID%2C+OFFENSE_CATEGORY_ID%2C+FIRST_OCCURRENCE_DATE%2C+LAST_OCCURRENCE_DATE%2C+REPORTED_DATE%2C+INCIDENT_ADDRESS%2C+GEO_X%2C+GEO_Y%2C+GEO_LON%2C+GEO_LAT%2C+DISTRICT_ID%2C+PRECINCT_ID%2C+NEIGHBORHOOD_ID%2C+IS_CRIME%2C+IS_TRAFFIC%2C+VICTIM_COUNT&returnGeometry=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&defaultSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=REPORTED_DATE+desc&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount={init_num}&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=standard&f=pjson&token="

        r = requests.post(newest)
        data = r.json()
        
        values = []
        entries = data['features']
        timeToFilter = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) - relativedelta(days=30)
        reportedDateFilter = int(time.mktime(timeToFilter.timetuple()) * 1000)
        print(reportedDateFilter)
        for row in entries:
            if(row["attributes"]["REPORTED_DATE"] is None):
                continue
            if(row["attributes"]["REPORTED_DATE"] < reportedDateFilter):
                continue
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

        cursor.execute(init_query)

        mydb.commit()
    
    return "done!!"


