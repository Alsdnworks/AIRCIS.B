search = input("검색하려는 정보를 입력하세요 ARR/DEP : ")

from discord.ext.commands.errors import MaxConcurrencyReached
import requests


Year, Month, Date = input('write time what you want to lookup(ex:2021 09 01): ').split()

if search == "ARR":
    URL =''
    URL += f'http://ubikais.fois.go.kr/sysUbikais/biz/fpl/selectArr.fois?downloadYn=1&srchDate={Year}-{Month}-{Date}&srchDatesh={Year}{Month}{Date}&srchAl=&srchFln=&srchDep=&srchArr=RKSI&dummy=175827665&cmd=get-records&limit=100&offset=0'
    response = requests.get(URL.format())
    rep = response.json()

    result = ''

    print("status : ", rep["status"],"\n")
    for i in rep["records"]:
        result += "\n편명 : " + str(i["fpId"])
        result += "\n등록번호 : " + str(("Not Assigned" if i["acId"] == None else i["acId"]))
        result += "\n기종 : " + str(i["acType"])
        result += "\n출발공항 : " + str(i["apIcao"])
        result += "\n출발시각 : " + str(i["staDate"]) + " " + str(i["sta"])
        result += "\n도착공항 : " + str(i["apArr"])
        result += "\n도착시간 : " + str(i["schDate"]) + " " + str(("None" if i["eta"] == None else i["eta"]))
        result += "\n램프/램프인 : " + str(("Not Assigned" if i["standArr"] == None else i["standArr"])) + " / " + str(("None" if i["blockOnTime"] == None else i["blockOnTime"]))
        result += "\n현재상태 : " +  str(("None" if i["arrStatus"] == None else i["arrStatus"]))
        result += "\namsRecPk / flightPk : " + str(i["amsRecPk"]) + " / " + str(i["flightPk"])
        result += "\n\n[FPL]\n\n"
    print (result)        
