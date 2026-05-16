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
- Enable changes to single mods
- Remove mod by name




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










# How to Send Data to Backend

## Launch the backend:
```bash
uvicorn backend.main:app --reload
```

Data from the json file that stores every moderator and Autosave option will be automatically loaded. (See below)


## API Endpoints

### Add Moderator

`POST /moderators`

Body example:

```json
{
  "name": "Dray",
  "rank": "KNIGHT",
  "timezone": "Europe/Rome",
  "availability": [
    {
      "start": "14:30",
      "end": "17:00"
    }
  ]
}
```

---

### Get Graph Data

`GET /graph_data?slot_size=30`

Example:

```text
http://127.0.0.1:8000/graph_data?slot_size=30
```

Response example:

```json
[
  [
  {
    "start_minute": 0,
    "end_minute": 30,
    "active_mods": [
      "Hunter"
    ],
    "mod_count": 1
  },
  {
    "start_minute": 30,
    "end_minute": 60,
    "active_mods": [
      "Hunter"
    ],
    "mod_count": 1
  },
  ...
]
```

`slot_size` is expressed in minutes.

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

### Filter Moderators

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