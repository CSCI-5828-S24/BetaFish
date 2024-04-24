import mysql.connector
from mysql.connector import errorcode



DB_NAME = "denvercrime"

# create table
table = "CREATE TABLE `crime` (OBJECTID int NOT NULL UNIQUE, INCIDENT_ID double, OFFENSE_ID varchar(20), OFFENSE_CODE varchar(4), OFFENSE_CODE_EXTENSION int, OFFENSE_TYPE_ID varchar(30), OFFENSE_CATEGORY_ID varchar(30), FIRST_OCCURRENCE_DATE long, LAST_OCCURRENCE_DATE long, REPORTED_DATE long, INCIDENT_ADDRESS varchar(100), GEO_X double, GEO_Y double, GEO_LON double, GEO_LAT double, DISTRICT_ID varchar(3), PRECINCT_ID varchar(4), NEIGHBORHOOD_ID varchar(100), IS_CRIME int, IS_TRAFFIC int, VICTIM_COUNT double, PRIMARY KEY (`OBJECTID`));"


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="pass",
  database="denvercrime"
)

cursor = mydb.cursor()

try:
    print("Creating table {}: ".format("crime"), end='')
    cursor.execute(table)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
        print("already exists.")
    else:
        print(err.msg)
else:
    print("OK")


# fill data

import json

filename = "data/query2.json"

f = open(filename)
 
data = json.load(f)

f.close()

entries = data['features']

cols = list(entries[0]["attributes"].keys())
# print(cols)

values = []

for row in entries:
    rowdata = list(row["attributes"].values())

    value = "("

    for i in range(len(rowdata)-1):
        value = value + '"' + str(rowdata[i]) + '", '

    value = value + '"' + str(rowdata[-1]) + '")'

    values.append(value)


pop = "INSERT INTO crime VALUES "

for i in range(len(values)-1):
    pop = pop + values[i] + ", "

pop = pop + values[-1] 

# print(pop)

try:
    print("Initializing crime data")
    cursor.execute(pop)
except mysql.connector.Error as err:
    print(err.msg)
else:
    print("OK")

mydb.commit()

cursor.close()

mydb.close()