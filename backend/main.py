from datetime import datetime
from fastapi import FastAPI
from enum import Enum
from dataclasses import dataclass
from zoneinfo import ZoneInfo, available_timezones

app = FastAPI()

# ----------------------------------------------------------------
# DATA DEFINITIONS
# ----------------------------------------------------------------

class Rank(Enum):
    RECRUIT = "Recruit"
    KNIGHT = "Knight"
    VANGUARD_KNIGHT = "Vanguard Knight"
    COMMANDER = "Commander"
    PRIME_COMMANDER = "Prime Commander"
    GENERAL = "General"
    SUPREME_GENERAL = "Supreme General"


@dataclass
class AvailabilityRange:
    start_hour: int
    end_hour: int

    def __post_init__(self):
        if self.start_hour < 0 or self.start_hour > 24:
            raise ValueError("start_hour must be between 0 and 24")

        if self.end_hour < 0 or self.end_hour > 24:
            raise ValueError("end_hour must be between 0 and 24")


@dataclass
class Moderator:
    name: str
    rank: Rank
    timezone: ZoneInfo
    availability: list[AvailabilityRange]
    utc_offset: int
    filtered: bool

@dataclass
class GraphHour:
    hour: int
    active_mods: list[str]
    mod_count: int


# ----------------------------------------------------------------
# DATA TO MANIPULATE
# ----------------------------------------------------------------

moderators: list[Moderator] = []
final_graph: list[GraphHour] = [
    GraphHour(
        hour=i,
        active_mods=[],
        mod_count=0
    )
    for i in range(24)
]


# ----------------------------------------------------------------
# (OUTPUT) DATA TO FRONTEND FUNCTIONS (GET ENDPOINTS)
# ----------------------------------------------------------------

@app.get("/")
def root():
    return {"message": "Backend online"}

@app.get("/timezones")
def get_timezones():
    return sorted(available_timezones())

@app.get("/moderators")
def get_moderators():
    return moderators

@app.get("/graph_data")
def get_graph_data():
    return final_graph

# ----------------------------------------------------------------
# (INPUT) DATA FROM FRONTEND FUNCTIONS (POST ENDPOINTS)
# ----------------------------------------------------------------

@app.post("/moderators")
def create_moderator(data: dict):

    availability = [
        AvailabilityRange(
            start_hour=slot["start_hour"],
            end_hour=slot["end_hour"]
        )
        for slot in data["availability"]
    ]

    moderator = add_moderator(
        name=data["name"],
        rank=Rank[data["rank"]],
        timezone_name=data["timezone"],
        availability=availability
    )

    calculate_graph_data()

    return {
        "message": "Moderator added",
        "moderator": {
            "name": moderator.name,
            "rank": moderator.rank.value,
            "timezone": moderator.timezone.key,
            "availability": [
                {
                    "start_hour": slot.start_hour,
                    "end_hour": slot.end_hour
                }
                for slot in moderator.availability
            ],
            "utc_offset": moderator.utc_offset,
            "filtered": moderator.filtered
        }
    }

@app.post("/reset")
def reset_data():

    moderators.clear()

    for graph_hour in final_graph:
        graph_hour.active_mods.clear()
        graph_hour.mod_count = 0

    return {
        "message": "All data reset"
    }

# ----------------------------------------------------------------
# INTERNAL FUNCTIONS
# ----------------------------------------------------------------

def add_moderator(
    name: str,
    rank: Rank,
    timezone_name: str,
    availability: list[AvailabilityRange]
) -> Moderator:

    if timezone_name not in available_timezones():
        raise ValueError(f"Invalid timezone: {timezone_name}")

    moderator = Moderator(
        name=name,
        rank=rank,
        timezone=ZoneInfo(timezone_name),
        availability=availability,
        utc_offset=get_utc_offset_hours(timezone_name),
        filtered=False
    )

    moderators.append(moderator)
    return moderator


def get_all_moderators() -> list[Moderator]:
    return moderators


def calculate_graph_data():
    
    for graph_hour in final_graph:
        graph_hour.active_mods.clear()
        graph_hour.mod_count = 0

        for moderator in moderators:

            mod_availability_range_UTC: list[AvailabilityRange] = []

            for availability_range in moderator.availability:
                utc_start = (availability_range.start_hour - moderator.utc_offset) % 24
                utc_end = (availability_range.end_hour - moderator.utc_offset) % 24

                mod_availability_range_UTC.append(
                    AvailabilityRange(
                        start_hour=utc_start,
                        end_hour=utc_end
                    )
                )

            if is_hour_in_availability_ranges(mod_availability_range_UTC,graph_hour.hour):
                graph_hour.active_mods.append(moderator.name)
                graph_hour.mod_count += 1




def is_hour_in_availability_ranges(av_range_list:list[AvailabilityRange], hour:int):
    for availability_range in av_range_list:
        start:int = availability_range.start_hour
        end:int = availability_range.end_hour

        if start < end:
            if start <= hour < end:
                return True
            
        elif start > end:
            if hour >= start or hour < end:
                return True
        
        else:
            return True
        
    return False



def get_utc_offset_hours(timezone_name: str) -> int:

    timezone = ZoneInfo(timezone_name)

    now = datetime.now(timezone)

    utc_offset = now.utcoffset()

    return int(utc_offset.total_seconds() / 3600)


# ----------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------

def main():
    add_moderator(
        name="Dray",
        rank=Rank.KNIGHT,
        timezone_name="Europe/Rome",
        availability=[
            AvailabilityRange(8, 10),
            AvailabilityRange(11, 15)
        ]
    )
    add_moderator(
        name="Thorfinn",
        rank=Rank.VANGUARD_KNIGHT,
        timezone_name="America/New_York",
        availability=[
            AvailabilityRange(8, 10),
            AvailabilityRange(11, 15)
        ]
    )

    print(get_all_moderators())


if __name__ == "__main__":
    main()
