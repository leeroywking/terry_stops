## SPD terry stop CLI explorer
This tool is a simple way to see the output of some fairly static queries against seattle police terry stops. Currently the data is organizes such that it will output as follows


```bash
lee@lee:~/projects/police_data$ python terry_stops.py 
Officer race: White
Suspect race: White

Outcomes for White suspects with White officer
Total 100.0 %
Field Contact 40.34 %
Offense Report 33.68 %
Arrest 23.74 %
Referred for Prosecution 1.94 %
Citation / Infraction 0.27 %
n=  16362

Run an additional Query?y
```

## Requirements
  - Python 3.8
  - This repo

## Usage
  - Should be fairly intuitive from the above example
  - bad entries will get a response of available fields

## Updating with current data
  - Visit https://data.seattle.gov/Public-Safety/Terry-Stops/28ny-9ts8/data
  - export data in JSON format
  - replace `terry_stops.json` data with new data