from fastapi import APIRouter, Query

from app.services.report_service import (
    get_report_preview
)
from fastapi.responses import FileResponse

from app.services.report_service import (
    export_csv,
    export_excel
)
router = APIRouter()


# ==========================================
# REPORT PREVIEW
# ==========================================

@router.get("/preview")
def report_preview(

    platform: str | None = Query(
        default=None
    ),

    sentiment: str | None = Query(
        default=None
    ),

    brand: str | None = Query(
        default=None
    ),

    keyword: str | None = Query(
        default=None
    )

):

    return get_report_preview(

        platform=platform,

        sentiment=sentiment,

        brand=brand,

        keyword=keyword

    )

@router.get("/download-csv")
def download_csv(

    platform: str | None = None,
    sentiment: str | None = None,
    brand: str | None = None,
    keyword: str | None = None

):

    file_path = export_csv(

        platform,
        sentiment,
        brand,
        keyword

    )

    return FileResponse(
        file_path,
        filename="social_media_report.csv"
    )


@router.get("/download-excel")
def download_excel(

    platform: str | None = None,
    sentiment: str | None = None,
    brand: str | None = None,
    keyword: str | None = None

):

    file_path = export_excel(

        platform,
        sentiment,
        brand,
        keyword

    )

    return FileResponse(
        file_path,
        filename="social_media_report.xlsx"
    )