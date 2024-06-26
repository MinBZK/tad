from fastapi import APIRouter
from fastapi.responses import JSONResponse

from tad.core.config import VERSION

router = APIRouter()


@router.get("/version", response_class=JSONResponse)
async def version():
    return {"version": VERSION}
