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


"Updated README, Major improvements including handling full time format (12:35 can be accepted as a valid start time of availability for example)"









# How to Send Data to Backend

## API Endpoints

### Add Moderator

`POST /moderators`

Body example:

```json
{
  "name": "Dray",
  "rank": "COMMANDER",
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
  {
    "start_minute": 750,
    "end_minute": 780,
    "active_mods": ["Dray"],
    "mod_count": 1
  }
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