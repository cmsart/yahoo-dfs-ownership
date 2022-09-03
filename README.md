# yahoo-dfs-ownership
A simple python script to fetch ownership data for past Yahoo Daily Fantasy contests

## Setup
You will need Python installed on your machine, as well as the the following Python packages:
- numpy
- requests

To run the script, navigate to the `src` directory and run `python main.py`

## Inputs
The script will prompt you to enter a contest id and input file name.

### Contest Id
To find the contest id, go to any of your past contest entries on Yahoo and fetch the id from the contest URL.

<img width="450" alt="contest_id" src="https://user-images.githubusercontent.com/8540255/188278459-5ffa702b-1527-400f-897a-1ae137dc0aad.png">

### Input File
You will also need to manually download the players list for the contest from the Yahoo website and place it in the `resources` directory of the project. When prompted to enter the file name, be sure to include the .csv extension (eg. `inputfile.csv`).

Open up the info modal for the contest:

<img width="547" alt="info" src="https://user-images.githubusercontent.com/8540255/188278527-6266c19b-514d-4f66-a7bf-626c5ca3682f.png">

Then download the player list csv:

<img width="841" alt="export" src="https://user-images.githubusercontent.com/8540255/188278556-47801f06-aab7-4b78-85f5-e02349e062e3.png">

## Output
The script will automatically write the file to the `out` directory of the project.

Since it would take to long to parse every entry for large contests, some players with miniscule ownership percentages won't be found. If a player is not found (or truly wasn't included in any lineups), their ownership will appear as `0.1` in the output file.
