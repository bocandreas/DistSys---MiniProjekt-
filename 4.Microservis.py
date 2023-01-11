"""
4. microservis sastoji od rute (/gatherData) sprema se Python kod u listu.
Ako ima više od 10 elemenata unutar liste asinkrono se kreiraju svi file-ovi
iz liste.
• Hints : aiofiles, asyncio
"""

import aiosqlite
import aiohttp
import asyncio
import json
from aiohttp import web
import aiofiles

routes = web.RouteTableDef()

async def create_files(data_list, file_name_format):
    for i, element in enumerate(data_list):
        username = element["username"]
        current_file_name = file_name_format.format(i, element)
        async with aiofiles.open(current_file_name, 'w') as f:
            await f.write(str(element))
            print(f"Created file {current_file_name}")

data_list = []
file_name_format = 'item{}.txt'

@routes.post("/gatherData")
async def gatherData(request):
    try:
        data = await request.json()
        #print(data)
        data_list.extend(data.values())
        print(data_list)
    except Exception as e:
        return web.json_response({"serviceNumber":4,"messages":str(e)}, status=200)

#Asinkrono kreiranje file iz liste
@routes.get("/gatherData")
async def gatherData(request):
    try:
        if len(data_list)>10:
            #("U listi imamo vise od 10 elemenata")
            await create_files(data_list, file_name_format)
    except Exception as e:
        return web.json_response({"serviceNumber":4,"messages":str(e)}, status=200)


app = web.Application()
app.router.add_routes(routes)
web.run_app(app,host="127.0.0.1", port=8084)