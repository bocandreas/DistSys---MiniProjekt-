"""
1. Microservis asinkrono poziva e-učenje API (M1), te prosljeđuje podatke
kao dictionary Worker tokenizer (WT) microservisu.

"""

import aiohttp
import asyncio
from aiohttp import web
import json

routes = web.RouteTableDef()

@routes.get("")
async def receive_data(request):
    try:
        #Dohvaćanje podataka sa 8080 mikroservisa
        async with aiohttp.ClientSession() as session:
            for _ in range(100):
                async with session.get("http://127.0.0.1:8080/gh_link") as response:
                    data = await response.json()
                #print(data)
                #Kreiranje dictionarya
                podaci = {}
                for row in data:
                    podatci = {}
                    podatci["username"] = row[1]
                    podatci["ghlink"] = row[2]
                    podatci["filename"] = row[3]
                    podaci[row[0]] = podatci
                result = {"data":podaci}
                print(result)
        #Slanje podataka na mikroservise 8082 i 8083
        async with aiohttp.ClientSession() as session:
            # Slanje podataka na 8082
            resp1 = session.post("http://127.0.0.1:8082/", json=result)
            # Slanje podataka na 8083
            resp2 = session.post("http://127.0.0.1:8083/", json=result)
            await asyncio.gather(resp1, resp2)

    except Exception as e:
        return web.json_response({"serviceNumber":1,"messages":str(e)}, status=200)
       
app = web.Application()
app.router.add_routes(routes)
web.run_app(app, host="127.0.0.1", port=8081)