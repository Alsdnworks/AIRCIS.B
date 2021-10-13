import discord
import os
import sys
import json
from discord.ext import commands
import time

global result

#UBIKAIS 관리자 서버관리 프로그램###################################################
client = commands.Bot(command_prefix='*')
@client.event
async def on_ready():
    print("유비카이스 봇 로그인이 완료되었습니다.")
    print("유비카이스 봇:" + client.user.name)
    print("디스코드봇 ID:" + str(client.user.id))
    print("디스코드봇 버전:" + str(discord.__version__))
    print('------')
    await client.change_presence(status=discord.Status.online, activity=discord.Game("PlaneSpotting"))
@client.command()
async def 버전(ver):
    await ver.send('UBIKAIS BOT/ver 1.7.3 해당버전은 베타버전으로 개발중입니다. 헬로월드(world is going hell)')
@client.command()
async def 작동확인(chk):
    await chk.send('UBIKAIS BOT/ver 1.7.3은 비정상작동중입니다.')   
@client.command()
async def 스케줄(sch):
    await sch.send()
    await sch.send('gg')
@client.command()
async def 출력(pln):
    await pln.channel.send(calc(str(pln.message.content)[4:]))
    
    #await pln.send(calc(pln.content))



#################################################################################################

def calc(Ubikais):
    import requests
    import re
    import sys
    tuple_string=("ALK","ANA","ABW","AAL","AFR","AFL","AHK","AIH","AZG","AAR","ACA","ABL","ASV","BAV","BOX","CAL","CKK","CKS","CES","CPA","CYZ","CSZ","CTJ","CQH","CXA","CLX","DLH","DAL","EVA","ETD","ETH","FIN","FDX","GIA","GEC","GTI","HAL","HGG","HYT","HVN","ICV","JJA","JNA","KAL","KLM","KZR","LHA","LOT","MAS","MGL","MMA","NCR","PAC","QTR","QFA","SIA","SOO","SHU","TWB","THA","THY","TZP","UAE","UAL","UPS","UZB","VJC","WGN")

    print(Ubikais.split('-'))

    search=(Ubikais.split('-')[0])

    Airport=(Ubikais.split('-')[1])

    Date=(Ubikais.split('-')[2])

    ######################################### 어라이벌 디파쳐 ###################
    if "ARR" in search:
        URL =''
        URL += 'http://ubikais.fois.go.kr/sysUbikais/biz/fpl/selectArr.fois?downloadYn=1&srchDate='
        URL += str(Date)
        URL += '&srchDatesh='
        URL += str(Date)
        URL += '&srchAl=&srchFln=&srchDep=&srchArr='
        URL += str(Airport)
        URL += '&dummy=175827665&cmd=get-records&limit=10000&offset=0'
        response = requests.get(URL.format())
        rep = response.json()
        result = ''

        print("status : ", rep["status"],"\n")
        for i in rep["records"]:
            if True==str(i["fpId"]).startswith(tuple_string):
                continue
            result += "\n\nFLT : " + str(i["fpId"])
            result += "\nREG : " + str(("Not Assigned" if i["acId"] == None else i["acId"]))
            result += "\nTYP : " + str(i["acType"])
            result += "\nDATE : " + str(i["schDate"])
            result += "\nORG : " + str(i["apIcao"])
            result += "\nSTD : " + str(i["schTime"])
            result += "\nETD : " + str(i["etd"])
            result += "\nDES : " + str(i["apArr"])
            result += "\nSTA : " + str(i["sta"])
            result += "\nETA : " + str(i["eta"])
            result += "\nATA : " + str(("None" if i["ata"] == None else i["ata"]))
            result += "\nSPT/RAM : " + str(("Not Assigned" if i["standArr"] == None else i["standArr"])) + " / " + str(("None" if i["blockOnTime"] == None else i["blockOnTime"]))
            result += "\nSTS : " +  str(("None" if i["arrStatus"] == None else i["arrStatus"]))



        if "DEP" in search:
            URL =''
            URL += 'http://ubikais.fois.go.kr/sysUbikais/biz/fpl/selectDep.fois?downloadYn=1&srchDate='
            URL += str(Date)
            URL += '&srchDatesh='
            URL += str(Date)
            URL += '&srchAl=&srchFln=&srchArr=&srchDep='
            URL += str(Airport)
            URL += '&dummy=175827665&cmd=get-records&limit=10000&offset=0'
            response = requests.get(URL.format())
            rep = response.json()
            result = ''
            print("status : ", rep["status"],"\n")
            for i in rep["records"]:
                if True==str(i["fpId"]).startswith(tuple_string):
                    continue
                result += "\n\nFLT : " + str(i["fpId"])
                result += "\nREG : " + str(("Not Assigned" if i["acId"] == None else i["acId"]))
                result += "\nTYP : " + str(i["acType"])
                result += "\nDATE : " + str(i["schDate"])
                result += "\nORG : " + str(i["apIcao"])
                result += "\nSTD : " + str(i["schTime"])
                result += "\nETD : " + str(i["etd"])
                result += "\nATD : " + str(i["atd"])
                result += "\nDES : " + str(i["apArr"])
                result += "\nSTA : " + str(i["sta"])
                result += "\nETA : " + str(i["eta"])
                result += "\nATA : " + str(("None" if i["ata"] == None else i["ata"]))
                result += "\nSPT/RAM : " + str(("Not Assigned" if i["standDep"] == None else i["standDep"])) + " / " + str(("None" if i["blockOffTime"] == None else i["blockOffTime"]))
                result += "\nSTS : " +  str(("None" if i["depStatus"] == None else i["depStatus"]))
    return result            
    ##EOF

###################################################################################################################
token=''
client.run(token) 
