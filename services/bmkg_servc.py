import aiohttp
import time as tm

TTL = 120
_cached = None
_fetched_at = 0.0

URL = "https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json"

async def get_latest_quake():
    global _cached, _fetched_at
    if _cached is not None and tm.monotonic() - _fetched_at < TTL:
        return _cached
    print("fetching from BMKG autogempa.json")
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as resp:
            data = await resp.json()
    _cached = data
    _fetched_at = tm.monotonic()
    return data