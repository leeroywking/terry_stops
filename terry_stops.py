import json
import math
import sys
from typing import Tuple
assert sys.version_info >= (3, 8)

with open('./terry_stops.json') as f:
  data = json.load(f)

columns = data["meta"]["view"]["columns"]
column_titles = []
for item in columns:
    column_titles.append(item["name"])
# print(column_titles)

def build_results(col1:int, col2:int, col3: int) -> dict:
    """
    Builds a dictionary which forms the basis of future answers
    """
    outcomes_by_officer_race_and_suspect_race = {}
    for report in data["data"]:
        officer_race = report[col1]
        suspect_race = report[col2]
        outcome = report[col3]
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
    return outcomes_by_officer_race_and_suspect_race

def get_races() -> Tuple[set,set]:
    """
    Returns a pair of sets of officer_races and suspect_races
    """
    officer_races = set()
    suspect_races = set()
    for entry in data["data"]:
        officer_races.add(entry[17])
        suspect_races.add(entry[18])
    return officer_races, suspect_races

def print_results(officer_race: str, suspect_race: str):
    """
    This calls build_results() and then prints the results
    """
    outcomes_by_officer_race_and_suspect_race = build_results(17,18,12)
    print(f"Outcomes for {suspect_race} suspects with {officer_race} officer")
    for outcome in outcomes_by_officer_race_and_suspect_race[officer_race][suspect_race]:
        parent = outcomes_by_officer_race_and_suspect_race[officer_race][suspect_race]
        print(outcome, math.floor(parent[outcome] /parent["Total"] * 10000)/100,"%")
    print("n= ", outcomes_by_officer_race_and_suspect_race[officer_race][suspect_race]["Total"])
    print("")

while True:
    officer_races, suspect_races = get_races()
    officer_race = input("Officer race:")
    while officer_race not in officer_races:
        print(f"please select an option from the following list")
        print(officer_races)
        officer_race = input("Officer race: ")
    suspect_race = input("Suspect race:")
    while suspect_race not in suspect_races:
        print(f"please select an option from the following list")
        print(suspect_races)
        suspect_race = input("Suspect race: ")
    print("")
    print_results(officer_race, suspect_race)
    exit(0)
