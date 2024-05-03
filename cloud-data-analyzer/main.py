from functools import cmp_to_key
import functions_framework
import os
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
import mysql.connector
from dotenv import load_dotenv

@functions_framework.http
def analyze(request):
    load_dotenv()
    status = True
    mydb = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            port=os.getenv("MYSQL_PORT", "3306"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DB")
        )
    cursor = mydb.cursor()
    
    cursor.execute(f'CREATE DATABASE IF NOT EXISTS {os.getenv("MYSQL_DB")}')
    cursor.execute(f'USE {os.getenv("MYSQL_DB")}')
    cursor.execute('SHOW TABLES')
    tables = cursor.fetchall()

    if (len(tables) == 0 or 'crime_totals' not in tables[0]):
        table_creation_script = "CREATE TABLE IF NOT EXISTS `crime_totals` (OFFENSE_CATEGORY_ID VARCHAR(30) NOT NULL, COUNT INT NOT NULL, PRIMARY KEY (`OFFENSE_CATEGORY_ID`));"
        cursor.execute(table_creation_script)
    
    cursor.execute("DELETE FROM crime_totals")
    cursor.execute('SELECT COUNT(*) FROM crime_totals')
    count = cursor.fetchall()
    if (count[0][0] == 0):
        # TODO: decide the minimum number of rows we want in the table. Minimized due to space in Cloud SQL server
        try:
            cursor = mydb.cursor()
            cursor.execute("SELECT * FROM crime")
            raw_data = cursor.fetchall()
            row_headers = [x[0] for x in cursor.description]
            json_data = []

            for r in raw_data:
                json_data.append(dict(zip(row_headers, r)))
            
            totals = {}
            for item in json_data:
                crime_category = item["OFFENSE_CATEGORY_ID"]
                if (crime_category not in totals): totals[crime_category] = 1
                else: totals[crime_category] += 1
        except Exception as error:
            status = False
        values = []
        
        for row in totals.items():
            rowdata = row

            value = "("

            for i in range(len(rowdata)-1):
                if rowdata[i] and (isinstance(rowdata[i],int) or isinstance(rowdata[i], float)):
                    value = value + str(rowdata[i]).strip() + ", "
                else:
                    value = value + "'" + str(rowdata[i]).strip() + "', "

            value = value  + str(rowdata[-1]) + ')'

            values.append(value)

        init_query = "INSERT INTO crime_totals VALUES "

        for i in range(len(values)-1):
            init_query = init_query + values[i] + ", "

        init_query = init_query + values[-1]
        cursor.execute(init_query)
        
    # crime frequency
    cursor.execute('SHOW TABLES')
    tables = cursor.fetchall()

    if (len(tables) == 0 or 'crime_freq' not in tables[0]):
        table_creation_script = "CREATE TABLE IF NOT EXISTS `crime_freq` (DAY INT NOT NULL, COUNT INT NOT NULL, PRIMARY KEY (`DAY`));"
        cursor.execute(table_creation_script)
    
    cursor.execute("DELETE FROM crime_freq")
    cursor.execute('SELECT COUNT(*) FROM crime_freq')
    count = cursor.fetchall()
    if (count[0][0] == 0):
        json_data = []
        try:
            timeToFilter = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) - relativedelta(days=29)
            reportedDateFilter = int(time.mktime(timeToFilter.timetuple()) * 1000)
            cursor.execute(f"select floor((REPORTED_DATE - {reportedDateFilter}) / 86400000) as day, count(*) as crimes_reported from crime group by 1")
            raw_data = cursor.fetchall()
            row_headers = [x[0] for x in cursor.description]
            json_data = []

            for r in raw_data:
                if(int(r[0]) < 0):
                    continue
                json_data.append({
                    'day': int(r[0]),
                    'crimes': r[1]
                })
            
            added_json_data = []
            for i in range(0,30):
                found = False
                for r in json_data:
                    if i == r['day']:
                        found = True
                        break
                if not found:
                    added_json_data.append({
                        'day': i,
                        'crimes': 0
                    })
            json_data = json_data + added_json_data
            json_data = sorted(json_data, key=cmp_to_key(lambda x1, x2: x1['day'] - x2['day']))
        except Exception as error:
            status = False
        values = []
    
        for row in json_data:
            rowdata = tuple(row.values())

            value = "("

            for i in range(len(rowdata)-1):
                if rowdata[i] and (isinstance(rowdata[i],int) or isinstance(rowdata[i], float)):
                    value = value + str(rowdata[i]).strip() + ", "
                else:
                    value = value + "'" + str(rowdata[i]).strip() + "', "

            value = value  + str(rowdata[-1]) + ')'

            values.append(value)

        init_query = "INSERT INTO crime_freq VALUES "

        for i in range(len(values)-1):
            init_query = init_query + values[i] + ", "

        init_query = init_query + values[-1]
        cursor.execute(init_query)

    mydb.commit()
    return "success" if status else "failed"
    
