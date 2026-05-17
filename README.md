# Timezone Calculator

Web app for managing moderator availability across multiple timezones.

## Features

- Moderator availability submission
- Timezone conversion
- Availability graph
- Filtering

# To-do list

### To do:

#### Frontend:
- 
#### Backend:




### In progress:

#### Frontend:
- 
#### Backend:
- 




### Done:

#### Frontend:
- 
#### Backend:
- Store data in runtime objects
- Send graph data with POST endpoint
- RESET POST request to reset all data
- Handle Timezone conversion
- Modular Time Slot handling when generating graph
- Filtering script
- Store data in json file
- Load data from json file
- Enable changes to single mods
- Remove mod by name








# Setting up the backend

## Windows

If you are using Windows, the easiest way is to run:

```cmd
setup_backend.bat
```

This will automatically:

- check if Python is installed
- create the virtual environment
- activate it
- install the required Python packages from `requirements.txt`

If Python is not installed, the script will show an error message.  
Install Python from the official website and make sure to enable:

```text
Add Python to PATH
```

Then run `setup_backend.bat` again.

---

## macOS / Linux / Manual setup

From the root project folder on Linux/Mac OS, open a terminal and run:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

On some systems, you may need to use:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

On Windows:
```bash
python3 -m venv venv
source venv/Source/activate
pip install -r requirements.txt
```

---

# How to Send Data to Backend

## Launch the backend

## Windows

If you are using Windows, simply run:

```cmd
run_backend.bat
```

This will activate the virtual environment and start the FastAPI backend.

---

## macOS / Linux / Manual launch

From the root project folder, run:

```bash
source venv/bin/activate
uvicorn backend.main:app --reload
```

On Windows, if you prefer doing it manually instead of using the `.bat` file:

```cmd
venv\Scripts\activate
uvicorn backend.main:app --reload
```

When the backend starts, data from the JSON file that stores every moderator and the autosave option will be automatically loaded. See the save/load section below for more details.


---

## API Endpoints

### Add or Update Moderator

`POST /moderators/add`

Adds a new moderator.  
If a moderator with the same name already exists, the backend updates that moderator instead.

Body example:

```json
{
  "name": "Dray",
  "rank": "KNIGHT",
  "timezone": "Europe/Rome",
  "offduty": false,
  "availability": [
    {
      "start": "14:30",
      "end": "17:00"
    }
  ]
}
```

Response example when adding a new moderator:

```json
{
  "message": "Moderator added",
  "moderator": {
    "name": "Dray",
    "rank": "Commander",
    "timezone": "Europe/Rome",
    "availability": [
      {
        "start_minute": 870,
        "end_minute": 1020
      }
    ],
    "utc_offset": 2,
    "filtered": false,
    "offduty": false
  }
}
```

Response example when updating an existing moderator:

```json
{
  "message": "Applied changes to already existing moderator",
  "moderator": {
    "name": "Dray",
    "rank": "Commander",
    "timezone": "Europe/Rome",
    "availability": [
      {
        "start_minute": 870,
        "end_minute": 1020
      }
    ],
    "utc_offset": 2,
    "filtered": false,
    "offduty": false
  }
}
```

**`offduty` is optional. If it is not provided, it defaults to `false`.**

---

### Remove Moderator

`POST /moderators/remove`

Removes a moderator by name.

Body example:

```json
{
  "name": "Dray"
}
```

Response example when the moderator exists:

```json
{
  "message": "Moderator removed",
  "removed_moderator": "Dray"
}
```

Response example when the moderator does not exist:

```json
{
  "message": "Moderator not found",
  "removed_moderator": null
}
```

---

### Get Graph Data

`GET /graph_data?slot_size=30`

Returns the processed availability graph data.

The backend takes all stored moderators, converts their local availability ranges to UTC, applies the current filters, and groups the result into time slots.

The `slot_size` query parameter defines the duration of each graph slot in minutes.

Example:

```text
http://127.0.0.1:8000/graph_data?slot_size=30
```

With `slot_size=30`, the backend returns **48 slots**, each representing 30 minutes of the day:

```text
00:00-00:30
00:30-01:00
01:00-01:30
...
23:30-24:00
```

Response example:

```json
[
  {
    "start_minute": 0,
    "end_minute": 30,
    "active_mods": ["Dray"],
    "mod_count": 1
  },
  {
    "start_minute": 30,
    "end_minute": 60,
    "active_mods": ["Dray"],
    "mod_count": 1
  },
  ...
  {
    "start_minute": 150,
    "end_minute": 180,
    "active_mods": ["Dray", "Thorfinn"],
    "mod_count": 2
  },
  ...
  {
    "start_minute": 750,
    "end_minute": 780,
    "active_mods": ["Thorfinn"],
    "mod_count": 1
  }
  ...
]
```

Response fields:

- `start_minute`: start of the slot, expressed as minutes after midnight UTC.
- `end_minute`: end of the slot, expressed as minutes after midnight UTC.
- `active_mods`: list of moderators available during that slot.
- `mod_count`: number of active moderators in that slot.

Example conversion:

```text
750 minutes = 12:30 UTC
780 minutes = 13:00 UTC
```

So this slot:

```json
{
  "start_minute": 750,
  "end_minute": 780,
  "active_mods": ["Dray"],
  "mod_count": 1
}
```

represents:

```text
12:30-13:00 UTC
```

---

### Get Timezones

`GET /timezones`

Returns all valid timezone names.

---

### Reset Data

`POST /reset`

Clears all stored moderators LOCALLY.
If you want to clear all stored data then proceed to do RESET AND THEN SAVE to erase all data permanently.
WATCH OUT: If Autosave is enabled (not by default), reset means all data will be deleted permanently.

---

### ~~Filter Moderators~~ **DEPRECTATED**

`POST /filters`

Body example:

```json
{
  "filtered_mods": [
    "Dray",
    "Thorfinn"
  ]
}
```

All moderators whose names are inside `filtered_mods` will be excluded from graph generation.
This method is **DEPRECATED** as it has been replaced by the new filtering options (see below).

---

### Filter by Moderator

`POST /filters/mod`

Shows only the moderators whose names are included in `visible_mods`.

Body example:

```json
{
  "visible_mods": ["Dray", "Thorfinn"]
}
```

Response example:

```json
{
  "message": "Moderator filter updated",
  "visible_mods": ["Dray", "Thorfinn"]
}
```

---

### Filter by Rank

`POST /filters/rank`

Shows only the moderators whose rank family is included in `visible_ranks`.

Valid rank families:

```text
RECRUIT
KNIGHT
COMMANDER
GENERAL
```

Rank families include upgraded ranks:

```text
KNIGHT    -> KNIGHT, VANGUARD_KNIGHT
COMMANDER -> COMMANDER, PRIME_COMMANDER
GENERAL   -> GENERAL, SUPREME_GENERAL
```

Body example:

```json
{
  "visible_ranks": ["KNIGHT", "COMMANDER"]
}
```

Response example:

```json
{
  "message": "Rank filter updated",
  "visible_ranks": ["KNIGHT", "COMMANDER"]
}
```

---

### Clear Filters

`POST /filters/clear`

Removes all active filters and shows every moderator again.

Response example:

```json
{
  "message": "Filters cleared"
}
```



### Save Data

`POST /save`

Saves current runtime data into the JSON file.

Response example:

```json
{
  "message": "Data saved successfully"
}
```

---

### Load Data

`POST /load`

Loads data from the JSON file into runtime memory. Data will be also automatically loaded when starting backend.

Response example:

```json
{
  "message": "Data loaded successfully",
  "moderators_count": 3
}
```

---

### Enable / Disable Autosave

`POST /autosave?enabled=true`

Enables autosave (off by default). This option will be saved and loaded every session since it's stored in the json file, like moderators list.

```text
http://127.0.0.1:8000/autosave?enabled=true
```

To disable it:

```text
http://127.0.0.1:8000/autosave?enabled=false
```

Response example:

```json
{
  "autosave": true
}
```

---

### Get Autosave Status

`GET /autosave`

Returns whether autosave is currently enabled or disabled.

Response example:

```json
{
  "autosave": true
}
```

---

### Autosave Behavior

If autosave is enabled, data will be automatically saved when the backend server shuts down.

Manual saving is still possible with:

`POST /save`