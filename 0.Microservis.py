"""
0. Fake E-ucenje API microservis (M0). Sastoji se od DB i jedne rute koja
vraća github linkove na zadaće. Prilikom pokretanja servisa, provjerava
se postoje li podaci u DB. Ukoliko ne postoje, pokreće se funkcija koja
popunjava DB s testnim podacima (10000). Kad microservis zaprimi
zahtjev za dohvaćanje linkova, uzima maksimalno 100 redataka podataka
iz DB-a.
• Hints
– Fake Dataset (224MB compressed, 1GB uncompressed)
"""

import aiosqlite
import aiohttp
from aiohttp import web
import asyncio
import json

routes = web.RouteTableDef()

#Provjerava da li je baza prazna
@routes.get("")
async def check_data(request):
    res=[]
    async with aiosqlite.connect("1.Projekt/Projekt1.db") as db:
        async with db.execute("SELECT * FROM Projekt1") as cur:
            async for row in cur:
                res.append(row)
            await db.commit()
            #Provjerava imamo li podataka u bazi
            #ako baza nije prazna
            if len(res) > 0:
                print("U bazi ima podataka")
            #ako je baza prazna
            else:
                print("U bazi nemamo podataka")
                fill_db = await post_data(request)
    return web.json_response({"status":"OK", "data":res}, status=200)


#Funkcija koja popunjava bazu podatcima
async def post_data(request):
    lista = []
    with open ("1.Projekt/file-000000000040.json", "r") as f:
        for jsonObj in f:
            fileDict = json.loads(jsonObj)
            lista.append(fileDict)
    prvih10k = lista[:10000]
    async with aiosqlite.connect("1.Projekt/Projekt1.db") as db:
        for item in prvih10k:
            username = (item["repo_name"].split("/")[0])
            #print(username)
            ghlink = "https://github.com/" + item["repo_name"]
            #print(ghlink)
            filename = (item["path"].split("/")[-1])
            #print(filename)
            await db.execute("INSERT INTO Projekt1 (username,ghlink,filename) VALUES (?,?,?)", (username,ghlink,filename))
            await db.commit()

#Poziv koji uzima samo 100 redova iz tablice
@routes.get("/gh_link")
async def get_data(request):
    try:
        async with aiosqlite.connect("1.Projekt/Projekt1.db") as db:
                #Uzimanje samo 100 elementa i slanje drugom servisu
                async with db.execute("SELECT * FROM Projekt1 LIMIT 100") as cur: 
                    data = await cur.fetchall()
                    
                    return web.json_response(data)
    except Exception as e:
        return web.json_response({"serviceNumber":0,"messages":str(e)}, status=200)


#Funkcija koja briše podatake iz tablice
@routes.get("/delete")
async def delete(request):
    res=[]
    async with aiosqlite.connect("1.Projekt/Projekt1.db") as db:
        await db.execute("DELETE FROM Projekt1")
        await db.commit()
        print("Obrisali smo podatke iz baze")
    return web.json_response({"status":"OK", "data":res}, status=200)


app = web.Application()
app.router.add_routes(routes)
web.run_app(app, host="127.0.0.1", port=8080)