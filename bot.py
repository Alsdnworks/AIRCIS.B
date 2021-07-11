import discord
import os
from discord.ext import commands
from selenium import webdriver 
import time
client = commands.Bot(command_prefix='*')
@client.command()
async def 조회(look):    
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    browser = webdriver.Chrome('chromedriver.exe',options=options)
    url = 'https://aircis.kr/jspView.do?jsp=kor/schedule/airDailySchLi'
    browser.get(url)
    #time.sleep(3) 이거 네트워크 상테 불량할때 켜주세요
    data = browser.find_element_by_css_selector("#gridMasterLayer > table").text
    print(data)
    await look.send(data)
    browser.quit()



    
client.run('os.environ['token'])