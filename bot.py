from bs4 import BeautifulSoup
from datetime import datetime,timezone,timedelta
import requests
import discord
import asyncio
#setting
channel=0
code=0
token=""
###

bot=discord.Bot()

@bot.event
async def on_ready():
    print(bot.user)

    mc=bot.get_channel(channel)
    msg=await mc.send("資料取得中")
    old=""
    while True:

        html_doc=requests.get(f"https://www.t-cat.com.tw/Inquire/TraceDetail.aspx?BillID={code}").text
        soup = BeautifulSoup(html_doc,'html.parser')
        st=[]
        for i in soup.find(id='resultTable').find_all("td"):
            st.append(i.text.replace("\n",""))
        number=st[4]
        st=st[5:]
        l=0
        text=''
        for i in st:
            if l%3==0:
                text+="===\n"
            text+=f"{i}\n"
            l+=1

        dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
        dt2 = dt1.astimezone(timezone(timedelta(hours=8)))
        now = dt2.strftime("%Y-%m-%d %H:%M:%S")


        embed=discord.Embed(title=f"貨物狀態({number})",description=text)
        embed.set_footer(text=now)
        await msg.edit(content=None,embed=embed)

        if old!=text and old!="":
            await mc.send(f"<!{bot.owner_id}> 資料貌似更新了")
        old=text
        await asyncio.sleep(30)

bot.run(token)