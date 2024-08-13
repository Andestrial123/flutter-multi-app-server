import uuid
from typing import List
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException

from app.controllers.mark import MarkController
from app.endpoints.schemas.mark import MarkGetSchema
from app.endpoints.v1 import router_v1
from app.utils.file import get_name
from app.utils.query import timezone_query

TAG = get_name(__file__)


@router_v1.get("/marks", tags=[TAG])
async def get_marks(
        timezone: ZoneInfo = Depends(timezone_query),
        controller: MarkController = Depends(MarkController)
) -> List[MarkGetSchema]:
    marks = await controller.get_all(tz=timezone)
    response = []

    for mark in marks:
        response.append(MarkGetSchema.model_validate(mark))

    return response


@router_v1.get("/mark/{mark_id}", tags=[TAG])
async def get_mark(
        mark_id: uuid.UUID,
        timezone: ZoneInfo = Depends(timezone_query),
        controller: MarkController = Depends(MarkController)
) -> MarkGetSchema:
    mark = await controller.get_by_id(mark_id, tz=timezone)

    if not mark:
        raise HTTPException(status_code=404, detail="Mark not found")

    return MarkGetSchema.model_validate(mark)
