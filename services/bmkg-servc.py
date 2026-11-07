import aiohttp

URL = "https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json"

async def get_latest_quake():
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as resp:
            data = await resp.json()
            return data