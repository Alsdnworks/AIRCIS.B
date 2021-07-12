import discord
import os
from discord.ext import commands
from selenium import webdriver 
import time
client = commands.Bot(command_prefix='*')

@client.command()
async def 점검(chk):
    await chk.send('aircisv0.0.5-Debug정상작동중')

@client.command()
async def 조회(look):   #' *조회'    
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("disable-gpu")
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")#heroku 외부변수
    browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=options)#heroku 외부변수
    url = 'https://aircis.kr/jspView.do?jsp=kor/schedule/airDailySchLi'
    browser.get(url)
    #time.sleep(3) 이거 네트워크 상테 불량할때 켜주세요
    data = browser.find_element_by_css_selector("#gridMasterLayer > table").text
    print(data)
    await look.send(data)
    browser.quit()
client.run(os.environ.get('TOKEN'))