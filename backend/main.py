from datetime import datetime
from fastapi import FastAPI
from enum import Enum
from dataclasses import dataclass
from zoneinfo import ZoneInfo, available_timezones

app = FastAPI()

# ----------------------------------------------------------------
# DATA DEFINITIONS
# ----------------------------------------------------------------

SLOT_SIZE = 60
MINUTES_PER_DAY = 1440

class Rank(Enum):
    RECRUIT = "Recruit"
    KNIGHT = "Knight"
    VANGUARD_KNIGHT = "Vanguard Knight"
    COMMANDER = "Commander"
    PRIME_COMMANDER = "Prime Commander"
    GENERAL = "General"
    SUPREME_GENERAL = "Supreme General"
    SAIYAN_ROYALTY = "Saiyan Royalty"


@dataclass
@dataclass
class AvailabilityRange:
    start_minute: int
    end_minute: int

    def __post_init__(self):
        if not 0 <= self.start_minute < MINUTES_PER_DAY:
            raise ValueError("start_minute must be between 0 and 1439")

        if not 0 <= self.end_minute <= MINUTES_PER_DAY:
            raise ValueError("end_minute must be between 0 and 1440")


@dataclass
class Moderator:
    name: str
    rank: Rank
    offduty: bool
    timezone: ZoneInfo
    availability: list[AvailabilityRange]
    utc_offset: int
    filtered: bool

@dataclass
class GraphSlot:
    start_minute:int
    end_minute:int
    active_mods: list[str]
    mod_count: int


# ----------------------------------------------------------------
# DATA TO MANIPULATE
# ----------------------------------------------------------------

moderators: list[Moderator] = []
final_graph: list[GraphSlot] = []


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
    return [
        {
            "name": moderator.name,
            "rank": moderator.rank.value,
            "offduty": moderator.offduty,
            "timezone": moderator.timezone.key,
            "availability": [
                {
                    "start_minute": slot.start_minute,
                    "end_minute": slot.end_minute
                }
                for slot in moderator.availability
            ],
            "utc_offset": moderator.utc_offset,
            "filtered": moderator.filtered
        }
        for moderator in moderators
    ]

@app.get("/graph_data")
def get_graph_data(slot_size: int = SLOT_SIZE):
    calculate_graph_data(slot_size)
    return final_graph

# ----------------------------------------------------------------
# (INPUT) DATA FROM FRONTEND FUNCTIONS (POST ENDPOINTS)
# ----------------------------------------------------------------

@app.post("/moderators")
def create_moderator(data: dict):

    availability = [
        AvailabilityRange(
            start_minute=time_to_minutes(slot["start"]),
            end_minute=time_to_minutes(slot["end"])
        )
        for slot in data["availability"]
    ]

    moderator = add_moderator(
        name=data["name"],
        rank=Rank[data["rank"]],
        timezone_name=data["timezone"],
        availability=availability
    )

    calculate_graph_data(SLOT_SIZE)

    return {"message": "Moderator added"}

@app.post("/reset")
def reset_data():

    moderators.clear()

    for graph_hour in final_graph:
        graph_hour.active_mods.clear()
        graph_hour.mod_count = 0

    return {
        "message": "All data reset"
    }

@app.post("/filters")
def set_filters(data: dict):

    filtered_mods = data["filtered_mods"]

    for moderator in moderators:

        if moderator.name in filtered_mods:
            moderator.filtered = True

        else:
            moderator.filtered = False

    return {
        "message": "Filters updated"
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
        offduty=False,
        timezone=ZoneInfo(timezone_name),
        availability=availability,
        utc_offset=get_utc_offset_hours(timezone_name),
        filtered=False
    )

    moderators.append(moderator)
    return moderator


def get_all_moderators() -> list[Moderator]:
    return moderators


def calculate_graph_data(slot_size: int):
    global final_graph

    final_graph = [
        GraphSlot(
            start_minute=i,
            end_minute=i + slot_size,
            active_mods=[],
            mod_count=0
        )
        for i in range(0, MINUTES_PER_DAY, slot_size)
    ]

    for graph_slot in final_graph:
        slot_start = graph_slot.start_minute

        for moderator in moderators:
            if moderator.filtered==False:
                utc_ranges: list[AvailabilityRange] = []

                for availability_range in moderator.availability:
                    utc_start = convert_local_minutes_to_utc(
                        availability_range.start_minute,
                        moderator.utc_offset
                    )

                    utc_end = convert_local_minutes_to_utc(
                        availability_range.end_minute,
                        moderator.utc_offset
                    )

                    utc_ranges.append(
                        AvailabilityRange(
                            start_minute=utc_start,
                            end_minute=utc_end
                        )
                    )

                if is_minute_in_availability_ranges(utc_ranges, slot_start):
                    graph_slot.active_mods.append(moderator.name)
                    graph_slot.mod_count += 1




def is_minute_in_availability_ranges(
    av_range_list: list[AvailabilityRange],
    minute: int
) -> bool:

    for availability_range in av_range_list:
        start = availability_range.start_minute
        end = availability_range.end_minute

        if is_minute_in_availability_range(start, end, minute):
            return True

    return False

def get_utc_offset_hours(timezone_name: str) -> int:

    timezone = ZoneInfo(timezone_name)

    now = datetime.now(timezone)

    utc_offset = now.utcoffset()

    return int(utc_offset.total_seconds() / 3600)

def time_to_minutes(time: str) -> int:
    hours, minutes = time.split(":")
    return int(hours) * 60 + int(minutes)

def convert_local_minutes_to_utc(local_minutes: int, utc_offset_hours: int) -> int:
    return (local_minutes - utc_offset_hours * 60) % 1440

def is_minute_in_availability_range(
    start: int,
    end: int,
    minute: int
) -> bool:

    if start < end:
        return start <= minute < end

    if start > end:
        return minute >= start or minute < end

    return True

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
