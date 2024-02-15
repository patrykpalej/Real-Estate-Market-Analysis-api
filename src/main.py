import os
import concurrent.futures
from fastapi import FastAPI

from routers import houses, apartments, lands
from utl import load_model, load_scraper


app = FastAPI(
    title="Real Estate Price Estimation API",
    description="This API can be used to estimate prices of apartments, houses and lands in Poland",
    version="0.1.0"
)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "secrets/cloud-storage-sa-key.json"

apartments_model = None
houses_model = None
lands_model = None

apartments_scraper = None
houses_scraper = None
lands_scraper = None


@app.on_event("startup")
async def load_all_models():
    global apartments_model, houses_model, lands_model
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for property_type in ["apartments", "houses", "lands"]:
                futures.append(executor.submit(load_model, property_type))

            concurrent.futures.wait(futures)
            apartments_model, houses_model, lands_model = [f.result() for f in futures]

    except Exception as e:
        raise Exception(f"Loading models failed: {e}")


@app.on_event("startup")
async def load_all_scrapers():
    global apartments_scraper, houses_scraper, lands_scraper
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for property_type in ["apartments", "houses", "lands"]:
                futures.append(executor.submit(load_scraper, property_type))

            concurrent.futures.wait(futures)
            apartments_scraper, houses_scraper, lands_scraper = [f.result() for f in futures]

    except Exception as e:
        raise Exception(f"Loading models failed: {e}")


app.include_router(houses.router)
app.include_router(apartments.router)
app.include_router(lands.router)
