from .config import DT_FORMAT
import pytz
from datetime import datetime as dt
import requests


def get_today() -> str:
    tz = pytz.timezone('America/New_York')
    today = dt.now().astimezone(tz)
    today = today.strftime(DT_FORMAT)
    return today


def verify_r(r: requests.Response) -> int:
    """
    Convenience function to verify the queries worked.
    """
    assert r.status_code == 200, f"bad status code: {r.status_code}"
    assert r.json(), "bad response json"
    assert r.json()['results'], "no results loaded"
    return len(r.json()['results'])


def load_data():
    """
    Gets donor, committee and candidate info from YAML file.

    Probably better ways/places to store this, but this is fine for now.
    """
    with open("data.yaml") as f:
        data = yaml.safe_load(f)
    return data
