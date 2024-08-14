from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from fastapi import Query, HTTPException


def timezone_query(timezone: str = Query()) -> ZoneInfo:
    try:
        zone_info = ZoneInfo(timezone)
        return zone_info
    except ZoneInfoNotFoundError:
        raise HTTPException(status_code=400, detail=f"{timezone} is unknown timezone")
