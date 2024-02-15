import io
import pickle
from google.cloud import storage


def load_model(property_type):
    blob_names_dict = {"houses": "gcp_randomforest_hou_240210_MAPE: 0.218.pickle",
                       "apartments": "gcp_randomforest_apa_240210_MAPE: 0.116.pickle",
                       "lands": "gcp_randomforest_lan_240210_MAPE: 0.284.pickle"}

    client = storage.Client()

    bucket = client.bucket("rea-models")
    blob = bucket.blob(blob_names_dict[property_type])
    byte_stream = io.BytesIO()
    blob.download_to_file(byte_stream)
    byte_stream.seek(0)
    return pickle.load(byte_stream)


def load_scraper(property_type):
    scraper_names_dict = {"houses": "bin/otodom_house_scraper.pickle",
                          "apartments": "bin/otodom_apartment_scraper.pickle",
                          "lands": "bin/otodom_land_scraper.pickle"}

    with open(scraper_names_dict[property_type], "rb") as f:
        scraper = pickle.load(f)
    return scraper
