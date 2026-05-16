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
- Store data in json file
- Load data from json file
- Filtering script
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










# How to Send Data to Backend

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

Clears all stored moderators.