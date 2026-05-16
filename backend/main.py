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

        if self.start_hour >= self.end_hour:
            raise ValueError("start_hour must be lower than end_hour")


@dataclass
class Moderator:
    name: str
    rank: Rank
    timezone: ZoneInfo
    availability: list[AvailabilityRange]


# ----------------------------------------------------------------
# DATA TO MANIPULATE
# ----------------------------------------------------------------

moderators: list[Moderator] = []



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

# ----------------------------------------------------------------
# (INPUT) DATA FROM FRONTEND FUNCTIONS (POST ENDPOINTS)
# ----------------------------------------------------------------

@app.post("/moderators")
def create_moderator(data: dict):

    moderators.append(data)

    return {
        "message": "Moderator added",
        "moderator": data
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
        availability=availability
    )

    moderators.append(moderator)
    return moderator


def get_moderators() -> list[Moderator]:
    return moderators


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

    print(get_moderators())


if __name__ == "__main__":
    main()
