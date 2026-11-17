from typing import Optional
from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse

from app.services import crop_services

router = APIRouter(prefix="/api/v1/crops", tags=["Crops"])


@router.get("/master")
async def get_master_crops(
    category: Optional[str] = Query(None, max_length=50, description="Filter by category")
):
    """
    Returns the static master list of Karnataka crops with bilingual labels.
    Supports optional category filtering (e.g. Vegetables, Fruits, Grains).
    """
    crops = crop_services.get_master_crops(category=category)
    return {
        "success": True,
        "total": len(crops),
        "crops": crops,
    }


@router.get("/search")
async def search_crop(
    q: str = Query(..., min_length=1, max_length=100, description="Search query in Kannada, Hindi, English, or Kanglish"),
    district: Optional[str] = Query(None, max_length=50, description="Preferred district benchmark (e.g. Mandya)"),
):
    """
    Translates user search query across Kannada script, Hindi script, English, or Kanglish
    into standardized crop profiles with live/district APMC benchmark prices.
    """
    matched_crop = crop_services.search_crop(query=q, district=district)
    if not matched_crop:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "query": q,
                "matched_crop": None,
                "message": f"No matching Karnataka crop found for '{q}'",
            },
        )

    return {
        "success": True,
        "query": q,
        "matched_crop": matched_crop,
    }
