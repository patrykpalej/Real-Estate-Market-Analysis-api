from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
import pandas as pd

from models import ApartmentModel


router = APIRouter()


def get_model():
    from main import apartments_model
    return apartments_model


def get_scraper():
    from main import apartments_scraper
    return apartments_scraper


@router.post("/apartments/from-json", tags=["apartments"])
async def estimate_price_from_json(body: ApartmentModel):
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


@router.get("/apartments/from-otodom-offer", tags=["apartments"])
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
        "market": offer.market,
        "apartment_area": offer.apartment_area,
        "n_rooms": offer.n_rooms,
        "build_year": offer.build_year,
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
