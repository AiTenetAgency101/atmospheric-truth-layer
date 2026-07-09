"""Backend API tests for Atmospheric Truth Layer."""
import os
import time
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://atmo-truth-v1.preview.emergentagent.com").rstrip("/")
API = f"{BASE_URL}/api"


def test_root_hello():
    r = requests.get(f"{API}/", timeout=15)
    assert r.status_code == 200
    assert "message" in r.json()


def _get_cert():
    r = requests.get(f"{API}/minting-certificate", timeout=15)
    assert r.status_code == 200
    return r.json()


def test_cert_version_and_timestamp():
    data = _get_cert()
    assert data["version"] == "v1.0.0-minted"
    assert data["minted_timestamp"] == "2026-04-23T07:53:50.5144990+10:00"


def test_cert_has_all_four_engines():
    engines = _get_cert()["engines"]
    for k in ["engine_365_days", "ultimate_engine", "tenet_agency_101", "witness_ledger"]:
        assert k in engines


def test_cert_has_four_verified_witnesses():
    witnesses = _get_cert()["witnesses"]
    assert len(witnesses) == 4
    codes = {w["code"] for w in witnesses}
    assert codes == {"BOM", "HIMAWARI-8", "GOES-16", "METEOSAT"}


def test_cert_series_a_funding_ask():
    assert _get_cert()["series_a"]["funding_ask_usd"] == 2500000


def test_cert_tagline_present():
    data = _get_cert()
    assert "tagline" in data and "sky" in data["tagline"].lower()


def test_system_state_increments():
    r1 = requests.get(f"{API}/system-state", timeout=15)
    assert r1.status_code == 200
    d1 = r1.json()
    assert "server_time" in d1
    assert d1["consensus"] == "3/3"
    time.sleep(2)
    r2 = requests.get(f"{API}/system-state", timeout=15)
    d2 = r2.json()
    # tenet_ticks increments ~54.7/s so must rise in 2s
    assert d2["tenet_ticks"] > d1["tenet_ticks"]
    assert d2["witnessed_tiles"] >= d1["witnessed_tiles"]


def test_status_post_and_get():
    payload = {"client_name": "TEST_atl_pytest"}
    r = requests.post(f"{API}/status", json=payload, timeout=15)
    assert r.status_code == 200
    body = r.json()
    assert body["client_name"] == "TEST_atl_pytest"
    assert "id" in body
    r2 = requests.get(f"{API}/status", timeout=15)
    assert r2.status_code == 200
    assert any(s.get("client_name") == "TEST_atl_pytest" for s in r2.json())
