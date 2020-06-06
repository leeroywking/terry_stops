import json
import math
import sys
from typing import Tuple

assert sys.version_info >= (3, 8)

# data obtained from
# https://www.seattle.gov/police/information-and-data/terry-stops
# and
# https://data.seattle.gov/Public-Safety/Terry-Stops/28ny-9ts8/data

with open("./terry_stops.json") as f:
    data = json.load(f)

columns = data["meta"]["view"]["columns"]
column_titles = []
for item in columns:
    column_titles.append(item["name"])
# print(column_titles)


def check_or_create_field(
    out: dict, officer_race: str, suspect_race: str, outcome: str
) -> None:
    try:
        out[officer_race]
    except KeyError:
        out[officer_race] = {}
    try:
        out[officer_race][suspect_race]
    except KeyError:
        out[officer_race][suspect_race] = {"Total": 0}
    try:
        out[officer_race][suspect_race][outcome]
    except KeyError:
        out[officer_race][suspect_race][outcome] = 0


def build_outcomes(col1: int, col2: int, col3: int) -> dict:
    """
    Builds a dictionary which forms the basis of future answers
    """
    outcomes_by_officer_race_and_suspect_race = {}
    for report in data["data"]:
        officer_race, suspect_race, outcome = report[col1], report[col2], report[col3]
        out = outcomes_by_officer_race_and_suspect_race
        check_or_create_field(out, officer_race, suspect_race, outcome)
        out[officer_race][suspect_race][outcome] += 1
        out[officer_race][suspect_race]["Total"] += 1
    return outcomes_by_officer_race_and_suspect_race


def get_races() -> Tuple[set, set]:
    """
    Returns a pair of sets of officer_races and suspect_races
    """
    officer_races = set()
    suspect_races = set()
    for entry in data["data"]:
        officer_races.add(entry[17])
        suspect_races.add(entry[18])
    return officer_races, suspect_races


def print_results(officer_race: str, suspect_race: str) -> None:
    """
    This calls build_results() and then prints the results
    """
    outcomes_by_officer_race_and_suspect_race = build_outcomes(17, 18, 12)
    print(f"Outcomes for {suspect_race} suspects with {officer_race} officer")
    for outcome in outcomes_by_officer_race_and_suspect_race[officer_race][
        suspect_race
    ]:
        parent = outcomes_by_officer_race_and_suspect_race[officer_race][suspect_race]
        print(outcome, math.floor(parent[outcome] / parent["Total"] * 10000) / 100, "%")
    print(
        "n= ",
        outcomes_by_officer_race_and_suspect_race[officer_race][suspect_race]["Total"],
    )
    print("")


def valid_entry(prompt: str, possible_entries: set) -> str:
    entry = input(prompt)
    while entry not in possible_entries:
        print(f"please enter an option from the following list")
        print(possible_entries)
        entry = input(prompt)
    return entry


def run_again():
    continue_yn = input("Run an additional Query?").lower()
    if continue_yn in ["y", "yes"]:
        main()
    elif continue_yn in ["n", "no"]:
        exit_prog()


def main() -> None:
    officer_races, suspect_races = get_races()
    officer_race = valid_entry("Officer race: ", officer_races)
    suspect_race = valid_entry("Suspect race: ", suspect_races)
    print("")
    print_results(officer_race, suspect_race)
    run_again()


def exit_prog():
    print(
        """
        Thank you for using this program written by Lee-Roy King
        https://github.com/leeroywking
        """
    )
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit_prog()
