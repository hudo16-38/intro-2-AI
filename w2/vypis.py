import json

data = json.load(open("ba_mhd_db.json", 'r'))

file = open("data.txt", "w")

for stop, sur in data["bus_stops"].items():
    x, y = sur
    print(f"{1};{stop};{round(x, 2)};{round(y, 2)}", file=file)

for stop, sus in data["neighbors"].items():
    print(2, stop, *sus, sep=";", file=file)

file.close()


