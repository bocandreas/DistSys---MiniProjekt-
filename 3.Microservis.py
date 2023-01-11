"""
3. WT microservis uzima dictionary. Uzima samo redove gdje username
počinje na d. Prosljeđuje kod 4. microservisu.
"""


import aiosqlite
import aiohttp
import asyncio
import json
from aiohttp import web

routes = web.RouteTableDef()

@routes.post("")
async def receive_and_filter_data(request):
    try:
        data = await request.json()
        print(data)
        #print("/n")
        filtered_data = {}
        for k,v in data["data"].items():
            if v["username"].startswith("d"):
                filtered_data[k] = v
        print(filtered_data)
        #Slanje podataka 4. mikroservisu
        async with aiohttp.ClientSession() as session:
            async with session.post("http://127.0.0.1:8084/gatherData", json=filtered_data) as resp:
                if resp.status == 200:
                    print("Podaci uspješno poslani 4. mikroservisu!")
                else:
                    print("Došlo je do greške pri slanju podataka.")
                    return web.json_response({"Podaci koje smo poslali su":filtered_data}, status=200)

    except Exception as e:
        return web.json_response({"serviceNumber":3,"messages":str(e)}, status=200)


app = web.Application()
app.router.add_routes(routes)
web.run_app(app,host="127.0.0.1", port=8083)