from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.services.mandi_services import (
    MandiDataUnavailableError,
    fetch_karnataka_mandi_rates,
)
                                                                                                            
router = APIRouter(prefix="/api/v1/mandi-rates", tags=["Mandi Rates"])                                  
                                                                                                            
@router.get("")
async def get_mandi_rates(
    district: Optional[str] = Query(None, max_length=50, description="e.g. Mandya, Kolar, Bangalore"),
    commodity: Optional[str] = Query(None, max_length=50, description="e.g. Tomato, Onion"),
    refresh: bool = Query(False, description="Force cache refresh from data.gov.in"),
):                                                                                                      
        try:
            rates = await fetch_karnataka_mandi_rates(
                district=district,
                commodity=commodity,
                force_refresh=refresh,
            )
        except MandiDataUnavailableError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

        return {                                                                                            
            "success": True,                                                                                
            "count": len(rates),                                                                            
            "source": "AGMARKNET (data.gov.in)",                                                            
            "data": rates                                                                                   
        } 