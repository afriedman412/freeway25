from .config import BASE_URL
from .routes import router
from .utilities import get_today
from . import generate_app
import os
import requests


live_app = generate_app()
live_app.include_router(router)


@live_app.get("/")
def read_root():
    return {"cornrows": "blind giants"}


@live_app.get("/form_test")
def test_pp_endpoint():
    headers = {}
    params = {}
    params['offset'] = 0

    url = os.path.join(BASE_URL, "independent_expenditures/{}/{}/{}.json")
    date = get_today()
    url = url.format(*date.split("-"))
    headers['X-API-Key'] = os.environ['PRO_PUBLICA_API_KEY']

    r = requests.get(
        url=url,
        timeout=30,
        headers=headers,
        params=params
    )

    if r.status_code == 200:
        output_ = r.json()
        return output_
    else:
        return "error code: {}".format(r.status_code)
