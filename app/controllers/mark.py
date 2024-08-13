import uuid
from datetime import datetime, timezone
from typing import List, Optional
from zoneinfo import ZoneInfo

from sqlalchemy.orm import joinedload
from sqlmodel import select

from app.controllers.base import BaseController
from app.models.enums import WorkType, Day
from app.models.mark import Mark, MarkWorkingHours


class MarkController(BaseController):

    async def get_all(self, tz: ZoneInfo) -> List[dict]:
        query = select(Mark) \
            .options(joinedload(Mark.working_hours))
        result = await self._session.execute(query)
        marks = result.unique().scalars().all()

        result = []

        for mark in marks:
            result.append(self.__get_working_hours(mark=mark, tz=tz))

        return result

    async def get_by_id(self, mark_id: uuid.UUID, tz: ZoneInfo) -> Optional[dict]:
        query = select(Mark) \
            .where(Mark.id == mark_id) \
            .options(joinedload(Mark.working_hours))
        result = await self._session.execute(query)
        mark: Mark = result.unique().scalars().first()

        if not mark:
            return None

        return self.__get_working_hours(mark=mark, tz=tz)

    def __get_working_hours(self, mark: Mark, tz: ZoneInfo) -> dict:
        is_open_default, bakery_hours = self.__is_open(tz, mark.working_hours, WorkType.default)
        is_open_delivery, delivery_hours = self.__is_open(tz, mark.working_hours, WorkType.delivery)
        result = {
            **mark.__dict__,
            "bakery_hours": {
                "is_open": is_open_default,
                **bakery_hours.__dict__,
            },
            "delivery_hours": {
                "is_open": is_open_delivery,
                **delivery_hours.__dict__,
            }

        }

        return result

    @staticmethod
    def __is_open(tz: ZoneInfo,
                  working_hours: List[MarkWorkingHours],
                  work_type: WorkType) -> (bool, MarkWorkingHours):
        now = datetime.now(tz)
        current_day = Day(now.strftime("%A").lower())

        current_working_hour = None

        for working_hour in working_hours:
            if working_hour.work_type == work_type and working_hour.day == current_day:
                current_working_hour = working_hour
                break

        if current_working_hour is None:
            raise ValueError(f"Working hours for current day now found, now: {now}, current_day: {current_day}")

        now_utc = datetime.now(timezone.utc)
        open_at = now_utc.replace(hour=current_working_hour.open_at.hour,
                                  minute=current_working_hour.open_at.minute,
                                  second=0,
                                  microsecond=0).astimezone(tz)
        close_at = now_utc.replace(hour=current_working_hour.close_at.hour,
                                   minute=current_working_hour.close_at.minute,
                                   second=0,
                                   microsecond=0).astimezone(tz)
        is_open = open_at <= now <= close_at

        current_working_hour.open_at = open_at.time()
        current_working_hour.close_at = close_at.time()

        return is_open, current_working_hour
