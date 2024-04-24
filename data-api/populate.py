import json

filename = "data/query2.json"

f = open(filename)
 
data = json.load(f)

f.close()
 
# for i in data['fields']:
#     print(i['name'])

entries = data['features']

cols = list(entries[0]["attributes"].keys())
# print(cols)

values = []

for row in entries:
    rowdata = list(row["attributes"].values())

    value = "("

    for i in range(len(rowdata)-1):
        value = value + str(rowdata[i]) + ", "

    value = value + str(rowdata[-1]) + ")"

    values.append(value)


pop = "INSERT INTO crime VALUES "

for i in range(len(values)-1):
    pop = pop + values[i] + ", "

pop = pop + values[-1] + ";"

print(pop)
