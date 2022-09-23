# encoding: utf-8:
import json
import time

import aiohttp
import requests
import valorant
from khl import Bot, Message
from khl.card import Card, CardMessage, Element, Module, Types

# 用读取来的 config 初始化 bot，字段对应即可
with open('./config/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

bot = Bot(token=config['token'])


##########################################################################################
##########################################################################################

# 没啥用的中二病指令
async def kda123(msg: Message):
    await msg.reply('本狸就是女王！\n[https://s1.ax1x.com/2022/07/03/jGFl0U.jpg](https://s1.ax1x.com/2022/07/03/jGFl0U.jpg)')


# 查询皮肤！只支持English皮肤名
async def skin123(msg: Message, name: str):
    try:
        # 读取valorant api的key
        with open('./config/valorant.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        client = valorant.Client(config['token'], locale=None)
        skins = client.get_skins()
        #name = input("Search a Valorant Skin Collection: ")
        results = skins.find_all(name=lambda x: name.lower() in x.lower())
        cm = CardMessage()
        c1 = Card(Module.Header('查询到你想看的皮肤了！'), Module.Context('还想查其他皮肤吗...'))
        c1.append(Module.Divider())
        for skin in results:
            c1.append(Module.Section(f"\t{skin.name.ljust(21)} ({skin.localizedNames['zh-TW']})"))
            #print(f"\t{skin.name.ljust(21)} ({skin.localizedNames['zh-CN']})")
        cm.append(c1)
        await msg.reply(cm)
    except Exception as result:
        await msg.reply("未知错误 %s" % result)


# 获取排行榜上的玩家，默认获取前15位胜场超过10的玩家
async def lead123(msg: Message, sz: int, num: int):
    try:
        with open('./config/valorant.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        client = valorant.Client(config['token'], locale=None, region='ap', route='asia')
        lb = client.get_leaderboard(size=sz)
        players = lb.players.get_all(numberOfWins=num)  # 筛选出胜场超过num的
        cm = CardMessage()
        c1 = Card(Module.Header('查询到你想看的排行榜了！'), Module.Context('什么？你也上榜了嘛...'))
        c1.append(Module.Divider())
        for p in lb.players:
            c1.append(Module.Section(f"#{p.leaderboardRank} - {p.gameName} ({p.numberOfWins} wins)"))
            #print(f"#{p.leaderboardRank} - {p.gameName} ({p.numberOfWins} wins)")
        cm.append(c1)
        await msg.reply(cm)
    except Exception as result:
        await msg.reply("未知错误 %s" % result)


####################################保存用户的游戏ID操作#######################################

# 预加载文件
with open("./log/game_idsave.json", 'r', encoding='utf-8') as frgm:
    GameIdDict = json.load(frgm)


#保存用户id
async def saveid123(msg: Message, game_id: str):
    global GameIdDict
    flag = 0
    # 如果用户id已有，则进行修改
    if msg.author_id in GameIdDict.keys():
        GameIdDict[msg.author_id] = game_id
        await msg.reply(f'本狸已经修改好你的游戏id啦!')
        flag = 1  #修改完毕后，将flag置为1

    #没有该用户信息，进行追加操作
    if flag == 0:
        GameIdDict[msg.author_id] = game_id
        await msg.reply(f"本狸已经记下你的游戏id喽~")
    # 修改/新增都需要写入文件
    with open("./log/game_idsave.json", 'w', encoding='utf-8') as fw2:
        json.dump(GameIdDict, fw2, indent=2, sort_keys=True, ensure_ascii=False)


# 让阿狸记住游戏id的help指令
async def saveid_1(msg: Message):
    await msg.reply(
        "基本方式看图就行啦！如果你的id之中有空格，需要用**英文的单引号**括起来哦！就像这样: `/saveid '你的id'`\n[https://s1.ax1x.com/2022/06/27/jV2qqe.png](https://s1.ax1x.com/2022/06/27/jV2qqe.png)\n注：阿狸升级以后已经不需要用单引号括起来了"
    )


# 显示已有id的个数
async def saveid_2(msg: Message):
    countD = len(GameIdDict)
    await msg.reply(f"目前狸狸已经记下了`{countD}`个小伙伴的id喽~")


# 实现读取用户游戏ID并返回
async def myid123(msg: Message):
    if msg.author_id in GameIdDict.keys():
        flag = 1  #找到了对应用户的id
        await msg.reply(f'游戏id: ' + GameIdDict[msg.author_id])
    else:
        countD = len(GameIdDict)
        await msg.reply(f"狸狸不知道你的游戏id呢，用`/saveid`告诉我吧！\n```\n/saveid 你的游戏id```\n目前狸狸已经记下了`{countD}`个小伙伴的id喽！")


##########################################################################################

# 预加载文件
with open("./log/ValErrCode.json", 'r', encoding='utf-8') as frgm:
    ValErrDict = json.load(frgm)

# 查询游戏错误码
async def val123(msg: Message, num: str = "-1"):
    if num == "-1":
        await msg.reply('目前支持查询的错误信息有：\n```\n0-1,4-5,7-21,29,31,33,38,43-46,49-70,81,84,128,152,1067,9001,9002,9003\n```\n注：van和val错误码都可用本命令查询')
    elif num in ValErrDict:
        await msg.reply(ValErrDict[num])
    else:
        await msg.reply('抱歉，本狸还不会这个呢~ 你能教教我吗？[当然!](https://f.wps.cn/w/awM5Ej4g/)')


#关于dx报错的解决方法
async def dx123(msg: Message):
    await msg.reply(
        '报错弹窗内容为`The following component(s) are required to run this program:DirectX Runtime`\n需要下载微软官方驱动安装，官网搜索[DirectX End-User Runtime Web Installer]\n你还可以下载本狸亲测可用的DX驱动 [链接](https://pan.baidu.com/s/1145Ll8vGtByMW6OKk6Zi2Q)，暗号是1067哦！\n狸狸记得之前玩其他游戏的时候，也有遇到过这个问题呢~'
    )


####################################################################################################
###################https://github.com/HeyM1ke/ValorantClientAPI#####################################
####################################################################################################

import riot_auth


# 获取拳头的token
# 此部分代码来自 https://github.com/floxay/python-riot-auth
async def authflow(user: str, passwd: str):
    CREDS = user, passwd
    auth = riot_auth.RiotAuth()
    await auth.authorize(*CREDS)
    # await auth.reauthorize()
    # print(f"Access Token Type: {auth.token_type}\n",f"Access Token: {auth.access_token}\n")
    # print(f"Entitlements Token: {auth.entitlements_token}\n",f"User ID: {auth.user_id}")
    return auth


#获取用户游戏id(从使用对象修改成使用文件中的内容)
async def fetch_user_gameID(auth):
    url = "https://pd.ap.a.pvp.net/name-service/v2/players"
    payload = json.dumps([auth['auth_user_id']])
    headers = {
        "Content-Type": "application/json",
        "X-Riot-Entitlements-JWT": auth['entitlements_token'],
        "Authorization": "Bearer " + auth['access_token']
    }
    async with aiohttp.ClientSession() as session:
        async with session.put(url, headers=headers, data=payload) as response:
            res = json.loads(await response.text())
    return res


# 获取每日商店
async def fetch_daily_shop(u):
    url = "https://pd.ap.a.pvp.net/store/v2/storefront/" + u['auth_user_id']
    headers = {
        "Content-Type": "application/json",
        "X-Riot-Entitlements-JWT": u['entitlements_token'],
        "Authorization": "Bearer " + u['access_token']
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            res = json.loads(await response.text())
    return res


# 获取vp和r点
async def fetch_valorant_point(u):
    url = "https://pd.ap.a.pvp.net/store/v1/wallet/" + u['auth_user_id']
    headers = {
        "Content-Type": "application/json",
        "X-Riot-Entitlements-JWT": u['entitlements_token'],
        "Authorization": "Bearer " + u['access_token']
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            res = json.loads(await response.text())
    return res


# 获取商品价格（所有）
async def fetch_item_price_all(u):
    url = "https://pd.ap.a.pvp.net/store/v1/offers/"
    headers = {
        "Content-Type": "application/json",
        "X-Riot-Entitlements-JWT": u['entitlements_token'],
        "Authorization": "Bearer " + u['access_token']
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            res = json.loads(await response.text())

    return res


# 获取商品价格（用uuid获取单个价格）
async def fetch_item_price_uuid(u, item_id: str):
    res = await fetch_item_price_all(u)  #获取所有价格

    for item in res['Offers']:  #遍历查找指定uuid
        if item_id == item['OfferID']:
            return item

    return "0"  #没有找到


# 获取皮肤等级（史诗/传说）
async def fetch_item_iters(iters_id: str):
    url = "https://valorant-api.com/v1/contenttiers/" + iters_id
    headers = {'Connection': 'close'}
    params = {"language": "zh-TW"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            res_iters = json.loads(await response.text())

    return res_iters


# 获取所有皮肤
async def fetch_skins_all():
    url = "https://valorant-api.com/v1/weapons/skins"
    headers = {'Connection': 'close'}
    params = {"language": "zh-TW"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            res_skin = json.loads(await response.text())

    return res_skin


# 获取所有皮肤捆绑包
async def fetch_bundles_all():
    url = "https://valorant-api.com/v1/bundles"
    headers = {'Connection': 'close'}
    params = {"language": "zh-TW"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            res_bundle = json.loads(await response.text())

    return res_bundle


# 获取获取玩家当前装备的卡面和称号
async def fetch_player_loadout(u):
    url = f"https://pd.ap.a.pvp.net/personalization/v2/players/{u['auth_user_id']}/playerloadout"
    headers = {
        "Content-Type": "application/json",
        "X-Riot-Entitlements-JWT": u['entitlements_token'],
        "Authorization": "Bearer " + u['access_token'],
        'Connection': 'close'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            res = json.loads(await response.text())

    return res


# 获取合约（任务）进度
# client version from https://valorant-api.com/v1/version
async def fetch_player_contract(u):
    #url="https://pd.ap.a.pvp.net/contract-definitions/v2/definitions/story"
    url = f"https://pd.ap.a.pvp.net/contracts/v1/contracts/" + u['auth_user_id']
    headers = {
        "Content-Type": "application/json",
        "X-Riot-Entitlements-JWT": u['entitlements_token'],
        "Authorization": "Bearer " + u['access_token'],
        "X-Riot-ClientPlatform":
        "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9",
        "X-Riot-ClientVersion": "release-05.03-shipping-8-745499"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            res = json.loads(await response.text())

    return res


# 获取玩家当前通行证情况，uuid
async def fetch_contract_uuid(id):
    url = "https://valorant-api.com/v1/contracts/" + id
    headers = {'Connection': 'close'}
    params = {"language": "zh-TW"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            res_con = json.loads(await response.text())

    return res_con


# 用名字查询捆绑包包含什么枪
async def fetch_bundle_weapen_byname(name):
    # 所有皮肤
    with open("./log/ValSkin.json", 'r', encoding='utf-8') as frsk:
        ValSkinList = json.load(frsk)

    WeapenList = list()
    for skin in ValSkinList['data']:
        if name in skin['displayName']:
            # 为了方便查询价格，在这里直接把skin的lv0-uuid也给插入进去
            data = {'displayName': skin['displayName'], 'lv_uuid': skin['levels'][0]['uuid']}
            WeapenList.append(data)

    return WeapenList


# 获取玩家卡面，uuid
async def fetch_playercard_uuid(id):
    url = "https://valorant-api.com/v1/playercards/" + id
    headers = {'Connection': 'close'}
    params = {"language": "zh-TW"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            res_card = json.loads(await response.text())

    return res_card


# 获取玩家称号，uuid
async def fetch_title_uuid(id):
    url = "https://valorant-api.com/v1/playertitles/" + id
    headers = {'Connection': 'close'}
    params = {"language": "zh-TW"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            res_title = json.loads(await response.text())

    return res_title


# 获取喷漆，uuid
async def fetch_spary_uuid(id):
    url = "https://valorant-api.com/v1/sprays/" + id
    headers = {'Connection': 'close'}
    params = {"language": "zh-TW"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            res_sp = json.loads(await response.text())

    return res_sp


# 获取吊坠，uuid
async def fetch_buddies_uuid(id):
    url = "https://valorant-api.com/v1/buddies/levels/" + id
    headers = {'Connection': 'close'}
    params = {"language": "zh-TW"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            res_sp = json.loads(await response.text())

    return res_sp


# 获取皮肤，通过lv0的uuid
async def fetch_skinlevel_uuid(id):
    url = f"https://valorant-api.com/v1/weapons/skinlevels/" + id
    headers = {'Connection': 'close'}
    params = {"language": "zh-TW"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            res_skin = json.loads(await response.text())
    return res_skin



##############################################################################################

# 获取不同奖励的信息
async def get_reward(reward):
    reward_type = reward['reward']['type']
    print("get_reward() ", reward_type)
    if reward_type == 'PlayerCard':  #玩家卡面
        return await fetch_playercard_uuid(reward['reward']['uuid'])
    elif reward_type == 'Currency':  #代币
        # 拳头通行证返回值里面没有数量，我谢谢宁
        return {
            'data': {
                "assetPath": "ShooterGame/Content/Currencies/Currency_UpgradeToken_DataAsset",
                "displayIcon":
                "https://media.valorant-api.com/currencies/e59aa87c-4cbf-517a-5983-6e81511be9b7/displayicon.png",
                "displayName": "輻能點數",
                "displayNameSingular": "輻能點數",
                "largeIcon":
                "https://media.valorant-api.com/currencies/e59aa87c-4cbf-517a-5983-6e81511be9b7/largeicon.png",
                "uuid": "e59aa87c-4cbf-517a-5983-6e81511be9b7"
            }
        }
    elif reward_type == 'EquippableSkinLevel':  #皮肤
        return fetch_skinlevel_uuid(reward['reward']['uuid'])
    elif reward_type == 'Spray':  #喷漆
        return await fetch_spary_uuid(reward['reward']['uuid'])
    elif reward_type == 'EquippableCharmLevel':  #吊坠
        return await fetch_buddies_uuid(reward['reward']['uuid'])
    elif reward_type == 'Title':  #玩家头衔
        return await fetch_title_uuid(reward['reward']['uuid'])

    return None


# 创建一个玩家任务和通信证的卡片消息
async def create_cm_contract(msg: Message):
    # 预加载用户token(其实已经没用了)
    with open("./log/UserAuth.json", 'r', encoding='utf-8') as frau:
        UserTokenDict = json.load(frau)
        
    userdict = UserTokenDict[msg.author_id]
    # 获取玩家当前任务和通行证情况
    player_mision = await fetch_player_contract(userdict)
    print(player_mision)
    interval_con = len(player_mision['Contracts'])
    battle_pass = player_mision['Contracts'][interval_con - 1]
    print(battle_pass, '\n')
    contract = await fetch_contract_uuid(battle_pass["ContractDefinitionID"])
    print(contract, '\n')
    cur_chapter = battle_pass['ProgressionLevelReached'] // 5  #计算出当前的章节
    remain_lv = battle_pass['ProgressionLevelReached'] % 5  #计算出在当前章节的位置
    print(cur_chapter, ' - ', remain_lv)
    if remain_lv:  #说明还有余度
        cur_chapter += 1  #加1
    else:  #为0的情况，需要修正为5。比如30级是第六章节的最后一个
        remain_lv = 5

    reward_list = contract['data']['content']['chapters'][cur_chapter - 1]  #当前等级所属章节
    print(reward_list, '\n')
    reward = reward_list['levels'][remain_lv - 1]  #当前所处的等级和奖励
    print(reward)
    reward_next = ""  #下一个等级的奖励
    if remain_lv < 5:
        reward_next = reward_list['levels'][remain_lv]  #下一级
    elif remain_lv >= 5 and cur_chapter < 11:  #避免越界
        reward_next = contract['data']['content']['chapters'][cur_chapter]['levels'][0]  #下一章节的第一个
    print(reward_next, '\n')

    c1 = Card(Module.Header(f"通行证 - {contract['data']['displayName']}"), Module.Divider())
    reward_res = await get_reward(reward)
    reward_nx_res = await get_reward(reward_next)
    print(reward_res, '\n', reward_nx_res, '\n')

    cur = f"当前等级：{battle_pass['ProgressionLevelReached']}\n"
    cur += f"当前奖励：{reward_res['data']['displayName']}\n"
    cur += f"奖励类型：{reward['reward']['type']}\n"
    cur += f"经验XP：{reward['xp']-battle_pass['ProgressionTowardsNextLevel']}/{reward['xp']}\n"
    c1.append(Module.Section(cur))
    if 'displayIcon' in reward_res['data']:  #有图片才插入
        c1.append(Module.Container(Element.Image(src=reward_res['data']['displayIcon'])))  #将图片插入进去
    next = f"下一奖励：{reward_nx_res['data']['displayName']}  - 类型:{reward_next['reward']['type']}\n"
    c1.append(Module.Context(Element.Text(next, Types.Text.KMD)))
    return c1
