import discord
import os
from discord.ext import commands
from selenium import webdriver 
import time
client = commands.Bot(command_prefix='*')

@client.command()
async def 버젼(chk):
###########################################################################
#릴리즈시
    await chk.send('aircisv0.0.11-Debug: HIROKU.US 서버정상작동중')

#디버깅시
    #await chk.send('aircisv0.0.11-Debug 개발자 디버깅중입니다.')


@client.command()
async def 조회(look):   #' *조회'
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("disable-gpu")

#히로쿠서버사용(릴리즈,웹디버깅)
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=options)

#노트북서버사용(디버그)
    #browser = webdriver.Chrome('chromedriver.exe',options=options)
    url = 'https://aircis.kr/jspView.do?jsp=kor/schedule/airDailySchLi'
    browser.get(url)
    for i in (range(1, 6)):
        await look.send('페이지'+str(i))
        time.sleep(1)
        #browser.find_element_by_css_selector('#gridPagingLayer > ul > a:nth-child(1)').click()css셀렉터 안씀
        browser.find_element_by_xpath('//*[@id="gridPagingLayer"]/ul/a['+str(i)+']').click()
        data = browser.find_element_by_css_selector("#gridMasterLayer > table").text
        await look.send(data)
    browser.quit()

@client.command()
async def 검색(sch):
    #값을 받고 그걸로 
    await sch.send('구현중')
################################################################################    
client.run(os.environ.get('TOKEN'))