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
