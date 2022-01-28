#取用功能
import os
import sys
import shutil
import string
import random
import time
import pathlib
import discord
from os import listdir
from os.path import isfile, isdir, join
from datetime import datetime
import logging
#discord
client = discord.Client()

@client.event
#登入設置
async def on_ready():
    print('login with',client.user)
    game = discord.Game('Redirecting Files')
    #discord.Status.<狀態>，可以是online,offline,idle,dnd,invisible
    await client.change_presence(status=discord.Status.online, activity=game)

#指令區
@client.event
async def on_message(message):
    #設定檔
    path = 'config.txt'
    with open(path) as f:
        e = f.readline()
        e = f.readline()
        prefix1 = f.readline()
        tmp1 = prefix1.split(" ",2)[1:]
        prefix = tmp1[:1] + ['']*(1 - len(tmp1))
        prefix = prefix[0]
        prefix = prefix.replace("\n", "")
        print(prefix)
        tmprefix = prefix

        domain1 = f.readline()
        tmp1 = domain1.split(" ",2)[1:]
        domain = tmp1[:1] + ['']*(1 - len(tmp1))
        domain = domain[0]
        domain = domain.replace("\n", "")
        print(domain)

        token1 = f.readline()
        tmp1 = token1.split(" ",2)[1:]
        token = tmp1[:1] + ['']*(1 - len(tmp1))
        token = token[0]
        token = token.replace("\n", " ")
        print(token)

    print(tmprefix)
    #排除自我訊息
    if message.author == client.user:
        return
    #指令功能從此開始
    #help
    if message.content.startswith(tmprefix + 'help'):
        #logging.info('[' + time.ctime + '] ' + message.author.name)
        await message.channel.send('<@' + str(message.author.id) + '>\n你不會?我教你\n> 一般指令:\n`' + prefix + 'url <URL> <名稱，隨機不填即可>` - 縮網址\n`' + prefix + 'curl <URL> <標題> <詳細敘述> <圖片網址> <名稱，隨機不填即可>` - 自訂縮網址，各項目一定要填，不然會錯位\n> 管理員:\n`' + prefix + 'del <短網址名稱>` - 刪除網址\n`' + prefix + 'list` - 網址列表\n\n_nelson url shorten v1.0_')
    #一般縮網址
    if message.content.startswith(tmprefix + 'url'):
        #切三刀訊息
        tmp1 = message.content.split(" ",3)[1:]
        tmp = tmp1[:2] + ['']*(2 - len(tmp1))
        print(tmp)
        #如果分割後串列長度只有4
        if len(tmp[0]) == 0:
            await message.channel.send(":warning:正確用法:`+url <URL> <名稱，隨機不填即可>`")
            return
        else:
            web = tmp[0]
            name = tmp[1]
            if "http" in web:
                print('url http pass')
                if 'http://' + domain in web:
                    await message.channel.send(':warning:不要重新導向至本網址!')
                    print('url nsgx fail')
                    return
                else:
                    if "://" in web:
                        print('url http/https:// pass')
                        if len(name) == 0:
                            letters = string.ascii_letters + string.digits
                            name2 = ( ''.join(random.choice(letters) for i in range(3)) )
                            print('random name')
                            print('name set to ' + name2)
                            if os.path.isdir('/var/www/html/' + name2):
                                await message.channel.send(':warning:URL已存在，請再試一次')
                                return
                            else:
                                os.mkdir('/var/www/html/' + name2)
                                with open('/var/www/html/' + name2 + '/index.html', 'w') as fp:
                                    fp.write('<head><meta charset="utf-8"><title>重新導向中 | Redirecting...</title><meta http-equiv="refresh" content="0; url=' + web + ' "/>' + '</head>\n<h1><b>重新導向中 | Redirecting...<a href=' + web + '>CLICK ME</a> if you aren\'t redirected.\n</h1><h2>Powered by nelson')
                                    pass
                                await message.channel.send('http://' + domain + '/' + name2)
                        else:
                            name2 = name
                            print('name set to ' + name2)
                            if os.path.isdir('/var/www/html/' + name2):
                                await message.channel.send(':warning:URL已存在，請再試一次')
                                return
                            else:
                                os.mkdir('/var/www/html/' + name2)
                                with open('/var/www/html/' + name2 + '/index.html', 'w') as fp:
                                    fp.write('<head><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=' + web + ' "/>' + '</head>\n<h1><b>重新導向中 | Redirecting...<a href=' + web + '>CLICK ME</a> if you aren\'t redirected.\n</h1><h2>Powered by nelson')
                                    pass
                                await message.channel.send('http://' + domain + '/' + name2)
                    else:
                        print('url fail https://')
                        await message.channel.send(':warning:無效的URL')
            else:
                await message.channel.send(":warning:您的URL必須包含http/https。")
                print('url fail')
                return
    #自訂縮網址
    if message.content.startswith(tmprefix + 'curl'):
        #切5刀訊息
        tmp1 = message.content.split(" ",6)[1:]
        tmp = tmp1[:5] + ['']*(5 - len(tmp1))
        print(tmp)
        #如果分割後串列長度只有4
        if len(tmp[0]) == 0:
            await message.channel.send(":warning:正確用法:`+curl <URL> <標題> <詳細敘述> <圖片> <名稱，隨機不填即可>`")
            return
        else:
            web = tmp[0]
            title = tmp[1]
            detail = tmp[2]
            img = tmp[3]
            name = tmp[4]
            if "http" in web:
                print('url http pass')
                if "://" in web:
                    print('url http/https:// pass')
                    if 'http://' + domain in web:
                        await message.channel.send(':warning:不要重新導向至本網址!')
                        print('url nsgx fail')
                        return
                    else:
                        if len(name) == 0:
                            letters = string.ascii_letters + string.digits
                            name2 = ( ''.join(random.choice(letters) for i in range(3)) )
                            print('random name')
                            print('name set to ' + name2)
                            if os.path.isdir('/var/www/html/' + name2):
                                await message.channel.send(':warning:URL已存在，請再試一次')
                                return
                            else:
                                os.mkdir('/var/www/html/' + name2)
                                with open('/var/www/html/' + name2 + '/index.html', 'w') as fp:
                                    fp.write('<meta http-equiv="refresh" content="0; url=' + web + ' "/>' + '\n<h1><b>重新導向中 | Redirecting...<a href=' + web + '>CLICK ME</a> if you aren\'t redirected.\n</h1><h2>Powered by nelson\n<head><meta charset="utf-8"><title>重新導向中 | Redirecting</title><meta property="og:type" content="website" /><meta property="og:title" content="' + title + '" /><meta property="og:description" content="' + detail + '" /><meta property="og:image" content="' + img + '" /></head>')
                                    pass
                                await message.channel.send('http://' + domain + '/' + name2)
                        else:
                            name2 = name
                            print('name set to ' + name2)
                            if os.path.isdir('/var/www/html/' + name2):
                                await message.channel.send(':warning:URL已存在，請再試一次')
                                return
                            else:
                                os.mkdir('/var/www/html/' + name2)
                                with open('/var/www/html/' + name2 + '/index.html', 'w') as fp:
                                    fp.write('<meta http-equiv="refresh" content="0; url=' + web + ' "/>' + '\n<h1><b>重新導向中 | Redirecting...<a href=' + web + '>CLICK ME</a> if you aren\'t redirected.\n</h1><h2>Powered by nelson\n<head><title>重新導向中 | Redirecting</title><meta charset="utf-8"><meta property="og:type" content="website" /><meta property="og:title" content="' + title + '" /><meta property="og:description" content="' + detail + '" /><meta property="og:image" content="' + img + '" /></head>')
                                    pass
                                await message.channel.send('http://' + domain + '/' + name2)
                else:
                    print('url fail https://')
                    await message.channel.send(':warning:無效的URL')
            else:
                await message.channel.send(":warning:您的URL必須包含http/https。")
                print('url fail')
                return
    #刪除[ADMIN]
    if message.content.startswith(tmprefix + 'del'):
        #驗證
        if context.message.author.mention == message.author.guild_permissions.administrator:
            print('pass')
            tmpd1 = message.content.split(" ",2)[1:]
            tmpd = tmpd1[:1] + ['']*(1 - len(tmpd1))
            print(tmpd)
            #如果分割後串列0長度只有1
            if len(tmpd[0]) == 0:
                await message.channel.send(":warning:正確用法:`+del <名稱>`")
                return
            else:
                if os.path.isdir('/var/www/html/' + tmpd[0]):
                    try:
                        shutil.rmtree('/var/www/html/' + tmpd[0])
                    except OSError as e:
                        print("Error: %s - %s." % (e.filename, e.strerror))
                    await message.channel.send(":white_check_mark:完成刪除")
                else:
                    await message.channel.send(':warning:沒有此短網址')
        else:
            await message.channel.send(':warning:你沒權限!')
            return
    #列表[ADMIN]
    if message.content.startswith(tmprefix + 'list'):
        if context.message.author.mention == message.author.guild_permissions.administrator:
            links = listdir('/var/www/html')
            await message.channel.send('所有網址列表:' + str(links))
        else:
            await message.channel.send(':warning:你沒權限!')
            return

#token here
#設定檔
path = 'config.txt'
with open(path) as f:
    e = f.readline()
    e = f.readline()
    e = f.readline()
    e = f.readline()
    token1 = f.readline()
    tmp1 = token1.split(" ",2)[1:]
    token = tmp1[:1] + ['']*(1 - len(tmp1))
    token = token[0]
    token = token.replace("\\n\n", "")
    print(token)
client.run(token)