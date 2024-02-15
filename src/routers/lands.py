from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
import pandas as pd

from models import LandModel


router = APIRouter()


def get_model():
    from main import lands_model
    return lands_model


def get_scraper():
    from main import lands_scraper
    return lands_scraper


@router.post("/lands/from-json", tags=["lands"])
async def estimate_price_from_json(body: LandModel):
    data = body.model_dump()
    model = get_model()

    df = pd.DataFrame(data, index=[0])
    df["utc_created_at"] = pd.to_datetime(df["utc_created_at"])

    try:
        price = model.predict(df)[0]
    except Exception as e:
        message = {"message": f"An error occured during the model prediction: {e}"}
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=message)

    message = {"result": price}
    return JSONResponse(status_code=status.HTTP_200_OK, content=message)


@router.get("/lands/from-otodom-offer", tags=["lands"])
def estimate_price_from_otodom_offer(url: str):
    scraper = get_scraper()
    try:
        offer = scraper.scrape_offer_from_url(url)
    except Exception as e:
        message = {"message": f"An error occured during the offer scraping: {e}"}
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=message)

    offer_json = {
        "advert_type": offer.advert_type,
        "utc_created_at": offer.utc_created_at,
        "province": offer.province,
        "subregion": offer.subregion,
        "location": offer.location,
        "land_area": offer.land_area,
    }
    offer_df = pd.DataFrame(offer_json, index=[0])
    model = get_model()

    try:
        price = model.predict(offer_df)[0]
    except Exception as e:
        message = {"message": f"An error occured during the model prediction: {e}"}
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=message)

    message = {"result": price}
    return JSONResponse(status_code=status.HTTP_200_OK, content=message)

