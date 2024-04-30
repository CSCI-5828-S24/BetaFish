import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()


from test_data import data


def populate_db():
    mydb = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            port=os.getenv("MYSQL_PORT"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DB")
        )
    cursor = mydb.cursor()
    print("database connected!")
    
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
        
        values = []
        
        for row in data:
            rowdata = list(row["attributes"].values())

            value = "("

            for i in range(len(rowdata)-1):
                if rowdata[i] and (isinstance(rowdata[i],int) or isinstance(rowdata[i], float)):
                    value = value + str(rowdata[i]).strip() + ", "
                else:
                    value = value + "'" + str(rowdata[i]).strip() + "', "

            value = value  + str(rowdata[-1]) + ')'

            values.append(value)

        init_query = "INSERT INTO crime VALUES "

        for i in range(len(values)-1):
            init_query = init_query + values[i] + ", "

        init_query = init_query + values[-1]
        print(init_query)
        cursor.execute(init_query)

        mydb.commit()
        

if __name__ == "__main__":
    populate_db()