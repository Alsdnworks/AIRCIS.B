from lib2to3.pgen2 import token
import pandas as pd
import discord
import os
import sys
import json
from discord.ext import commands
import requests
import re
import sys
global result

#필터/필터예외처리
filter=("AMX","ANZ","AIC","ALK","ANA","ABW","AAL","AFR","AFL","AHK","AIH","AZG","AAR","ACA","ABL","ASV","BAV","BOX","CAL","CKK","CKS","CES","CPA","CCA","CNZ","CDG","CSN","CEB","CRK","CYZ","CSZ","CTJ","CQH","CXA","CLX","DLH","DAL","EVA","ETD","ETH","FIN","FDX","GIA","GEC","GTI","HAL","HGG","HYT","HVN","ICV","JJA","JNA","KAL","KLM","KZR","LHA","LAO","LOT","MAS","MGL","MMA","PAC","PAL","QTR","QFA","QDA","SIA","SEJ","SBI","SOO","SHU","TWB","TGW","THA","THY","TZP","UAE","UAL","UPS","UZB","VJC","WGN","XAX")
fpid_except_Filter=('KAL1461')
acType_except_Filter=('B764')
acId_except_Filter=('HL7784')
    
#UBIKAIS 관리자 서버관리 프로그램###################################################
client = commands.Bot(command_prefix='!')
@client.event
async def on_ready():
    print("유비카이스 봇 로그인이 완료되었습니다. 개발자로그인중")
    print("유비카이스 봇:" + client.user.name)
    print("디스코드봇 ID:" + str(client.user.id))
    print("디스코드봇 버전:" + str(discord.__version__))
    print('------')
    await client.change_presence(status=discord.Status.online, activity=discord.Game("PlaneSpotting"))
@client.command()
async def 버전(ver):
    await ver.send('UBIKAIS BOT/ver Jan18. 헬로월드(world is going hell)')
@client.command()
async def 명령어(qna):
    await qna.send('[!버전],[!작동확인][!필터] [!PLN (ARR or DEP)-(RK@@)-(YYYYMMDD)] [ex) !PLN ARR-RKSI-20211225]')
@client.command()
async def 작동확인(chk):
    await chk.send('UBIKAIS BOT/ 개발자 디버깅중이라고 써두었지만 사실 디버깅후 수정하는걸 까먹었을수도있음')  
@client.command()
async def 필터 (fil):
    await fil.send('현재 적용중인 항공사 필터 목록은 다음과 같습니다.'+str(filter))
@client.command()
async def PLN(pln):
    await pln.channel.send(calc(str(pln.message.content)[5:]))
    
#await pln.send(calc(pln.content))
#keep_alive()

#################################################################################################
def makelayout(df,sortVar):
    df.sort_values(by=[sortVar], inplace=True)                
    df_ = df.copy()
    df_.columns = [''for _ in range(len(df_.columns))]
    df_.index = ['' for _ in range(len(df))]
    return df_
##################################################################################################################
def getdata(data,getlist):
    returnDF=pd.DataFrame()
    for j in range(len(getlist)):
        param=getlist[j]
        datBuffer=[]
        for i in data["records"]:
            if(str(i["fpId"]).startswith(fpid_except_Filter)==False|str(i["acType"]).startswith(acType_except_Filter)==False|str(i["acId"]).startswith(acId_except_Filter)==False):    
                if True==str(i["fpId"]).startswith(filter):
                    continue
            datBuffer.append(str(("N/A" if i[param] == None else i[param])))
        returnDF[param]=datBuffer
    return returnDF            
##################################################################################################################
def calc(Ubikais):
    result = pd.DataFrame()
    ARRgetlist=("fpId","acType","schTime","eta","apIcao","acId","standArr")
    DEPgetlist=("fpId","acType","schTime",'fplYn','apArr','depStatus','acId')
    print(Ubikais.split('-'))
    search=(Ubikais.split('-')[0])
    Airport=(Ubikais.split('-')[1])
    Date=(Ubikais.split('-')[2])
    if ((search=='') or (Airport=='')or(Date=='')):
        return('https://user-images.githubusercontent.com/79889482/149918194-def70899-4933-40fe-8756-0528aa3de51b.jpg')
##################################################################################################################
    if "ARR" in search:
        URL = 'http://ubikais.fois.go.kr/sysUbikais/biz/fpl/selectArr.fois?downloadYn=1&srchDate='+str(Date)+'&srchDatesh='+str(Date)+'&srchAl=&srchFln=&srchDep=&srchArr='+ str(Airport)+'&dummy=175827665&cmd=get-records&limit=10000&offset=0'
        try:
            response = requests.get(URL.format())
            rep = response.json()
        except:
            #서버다운 대응
            print('server_exception_occured')    
            return('https://user-images.githubusercontent.com/79889482/149918194-def70899-4933-40fe-8756-0528aa3de51b.jpg')
        print("status : ", rep["status"],"\n")
        result=getdata(rep,ARRgetlist)
        if result.empty:
            result='There is no data to output'
            return result
        else:
            return makelayout(result,'eta')
##################################################################################################################
    elif "DEP" in search: 
        URL = 'http://ubikais.fois.go.kr/sysUbikais/biz/fpl/selectDep.fois?downloadYn=1&srchDate='+ str(Date)+ '&srchDatesh='+ str(Date)+ '&srchAl=&srchFln=&srchArr=&srchDep='+ str(Airport)+ '&dummy=175827665&cmd=get-records&limit=10000&offset=0'
        try:
            response = requests.get(URL.format())
            rep = response.json()
        except:                        
            #서버다운 대응
            print('server_exception_occured')
            return('https://user-images.githubusercontent.com/79889482/149918194-def70899-4933-40fe-8756-0528aa3de51b.jpg')    
        print("status : ", rep["status"],"\n")
        result=getdata(rep,DEPgetlist)
        if result.empty:
            result='There is no data to output'
            return result
        else:
            return makelayout(result,'fplYn')
    else: 
        return('https://user-images.githubusercontent.com/79889482/149918194-def70899-4933-40fe-8756-0528aa3de51b.jpg')    
##################################################################################################################

client.run(token)
