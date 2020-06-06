import json
import math
import sys
assert sys.version_info >= (3, 8)

with open('./terry_stops.json') as f:
  data = json.load(f)

columns = data["meta"]["view"]["columns"]
column_titles = []
for item in columns:
    column_titles.append(item["name"])
# print(column_titles)

terry_stops_by_officer_race = {}
total_terry_stops = 0
terry_stops_by_race = {"Total":0}

for report in data["data"]:
    officer_race = report[17]
    suspect_race = report[18]
    try:
        terry_stops_by_officer_race[officer_race][suspect_race] += 1
    except:
        try:
            terry_stops_by_officer_race[officer_race][suspect_race] = 1
        except:
            terry_stops_by_officer_race[officer_race] = {}
            terry_stops_by_officer_race[officer_race][suspect_race] = 1
    try:
        terry_stops_by_officer_race[officer_race]["Total"] += 1
    except:
        terry_stops_by_officer_race[officer_race]["Total"] = 1
    total_terry_stops += 1

for report in data["data"]:
    suspect_race = report[18]
    try:
        terry_stops_by_race[suspect_race] += 1
    except:
        terry_stops_by_race[suspect_race] = 1
    terry_stops_by_race["Total"] += 1


# This will print a break down of white officers terry stop totals which track fairly well against the total

# print("Break down of White officer Terry Stops")
# white_officer_stops = terry_stops_by_officer_race["White"]
# for race in white_officer_stops:
#     percentage_terry = math.floor(white_officer_stops[race] / white_officer_stops["Total"] * 10000)/ 100
#     percentage_total_terry = math.floor(terry_stops_by_race[race] / terry_stops_by_race["Total"] * 10000)/ 100
#     print(race, str(percentage_terry) + "%" , "//", str(percentage_total_terry) + "%")
# print("Total White Officer Terry Stops", white_officer_stops["Total"])

# stop_outcomes = {}
# # print(data["data"][1][12])

# for report in data["data"]:
#     try:
#         stop_outcomes[report[12]] +=1
#     except:
#         stop_outcomes[report[12]] = 1

# for stop_type in stop_outcomes:
#     print(stop_type, stop_outcomes[stop_type])

outcomes_by_officer_race_and_suspect_race = {}
for report in data["data"]:
    officer_race = report[17]
    suspect_race = report[18]
    outcome = report[12]
    out = outcomes_by_officer_race_and_suspect_race
    try:
        out[officer_race]
    except:
        out[officer_race] = {}
    try:
        out[officer_race][suspect_race]
    except:
        out[officer_race][suspect_race] = {"Total":0}
    try:
        out[officer_race][suspect_race][outcome]
    except:
        out[officer_race][suspect_race][outcome] = 1

    out[officer_race][suspect_race][outcome] += 1
    out[officer_race][suspect_race]["Total"] +=1
# print(outcomes_by_officer_race_and_suspect_race["White"]["Black or African American"])
# print(outcomes_by_officer_race_and_suspect_race["White"]["White"])
print("outcomes for Black suspects  with White officer")
for outcome in outcomes_by_officer_race_and_suspect_race["White"]["Black or African American"]:
    parent = outcomes_by_officer_race_and_suspect_race["White"]["Black or African American"]
    print(outcome, math.floor(parent[outcome] /parent["Total"] * 10000)/100,"%")
print("n= ", outcomes_by_officer_race_and_suspect_race["White"]["Black or African American"]["Total"])

print("")

print("outcomes for White suspects  with White officer")
for outcome in outcomes_by_officer_race_and_suspect_race["White"]["White"]:
    parent = outcomes_by_officer_race_and_suspect_race["White"]["White"]
    print(outcome, math.floor(parent[outcome] /parent["Total"] * 10000)/100,"%")
print("n= ", outcomes_by_officer_race_and_suspect_race["White"]["White"]["Total"])
