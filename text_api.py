import uvicorn
from fastapi import FastAPI, Request
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from MiniSpire.src import sql_function
from MiniSpire.src.cards import  card_library, library_card_name, library_card_cost, library_card_desc, library_card_type ,card_library_dict
from MiniSpire.src.config import game_config
from MiniSpire.src.entities import Targets
from MiniSpire.src.play import Play
from MiniSpire.src.constants import Turn, CardType, State
import MiniSpire.src.data as data_
from MiniSpire.src.websocket_router import router

app = FastAPI()
app.include_router(router)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("templates/start.html")

@app.post("/reset")
async def reset(request: Request):
    data = await request.json()
    user_id = data["user_id"]
    data_.player[user_id].reset()
    data_.player[user_id].cards = []
    data_.player[user_id].hand_cards = []
    data_.player[user_id].enemy.reset()
    data_.game[data_.player[user_id].room_num] = Play(data_.player[user_id], data_.player[user_id].enemy)
    data_.game[data_.player[user_id].room_num].player.energy -= 1
    data_.message_log[data_.player[user_id].room_num] =  "游戏开始!\n"
    return {"message": "重置成功"}


@app.get("/play")
async def play():
    #cards.print_cards(player.hand_cards)
    return FileResponse("templates/play.html")

@app.post("/play")
async def play(request: Request):
    data = await request.json()
    user_id = data["user_id"]
    card_id = int(data["card_id"])
    message = ""
    if user_id == data_.game[data_.player[user_id].room_num].player.id and data_.game[data_.player[user_id].room_num].turn == Turn.PLAYERTURN1:
        infor_dict = data_.game[data_.player[user_id].room_num].rounds(card_id)
    elif user_id == data_.game[data_.player[user_id].room_num].enemy.id and data_.game[data_.player[user_id].room_num].turn == Turn.PLAYERTURN2:
        infor_dict = data_.game[data_.player[user_id].room_num].rounds(card_id)
    elif user_id == data_.game[data_.player[user_id].room_num].player.id and data_.game[data_.player[user_id].room_num].turn == Turn.PLAYERTURN2:
        return {"message": "你不能在当前回合行动"}
    elif user_id == data_.game[data_.player[user_id].room_num].enemy.id and data_.game[data_.player[user_id].room_num].turn == Turn.PLAYERTURN1:
        return {"message": "你不能在当前回合行动"}
    else:
        infor_dict = data_.game[data_.player[user_id].room_num].rounds(card_id)
    data_.use_card = infor_dict["use_card"]
    next_turn = data_.game[data_.player[user_id].room_num].turn
    data_.repeat_[user_id] = 1
    if next_turn == Turn.PLAYERTURN1:
        data_.repeat_[user_id] = 0
        data_.repeat_[data_.player[user_id].enemy.id] = 0
    if next_turn == Turn.PLAYERTURN2:
        data_.repeat_[user_id] = 0
        data_.repeat_[data_.player[user_id].enemy.id] = 0
    if data_.game[data_.player[user_id].room_num].state != State.PLAYING:
        data_.repeat_[user_id] = 0
        data_.repeat_[data_.player[user_id].enemy.id] = 0
    if infor_dict["message"] != "":
        message = infor_dict["message"]
    data_.message_log[data_.player[user_id].room_num] += message + "\n"
    return {"message": f"{message}","repeat":data_.repeat_[user_id],"message_log":data_.message_log[data_.player[user_id].room_num]}


@app.get("/get_card")
async def get_card():
    return FileResponse("templates/get_card.html")

@app.post("/get_card")
async def get_card(request: Request):
    data = await request.json()
    user_id = data["user_id"]
    current_card_id = int(data["card_id"])
    count_ku = len(data_.player[user_id].cards)
    if count_ku >= game_config.BASE_CARD_NUM:
        return {"message": "牌库已满,请开始游戏","print":1}
    data_.player[user_id].get_cards(1,current_card_id,False,card_library)
    if count_ku + 1 == game_config.BASE_CARD_NUM:
        data_.player[user_id].get_hand_card()
    return {"message": "添加成功","print":0}


@app.post("/save")
async def save(request: Request):
    data = await request.json()
    user_id = data["user_id"]
    exists = sql_function.check_user_exists(user_id)
    if user_id not in data_.player:
        data_.player[user_id] = Targets()
        data_.repeat_[user_id] = 0
        data_.player[user_id].id = user_id
        data_.player[user_id].enemy = Targets()
        data_.user_num += 1
        data_.player[user_id].room_num = data_.room_num
        if data_.user_num % 2 == 1:
            data_.game[data_.room_num].player = data_.player[user_id]
            data_.player[user_id].enemy = Targets()
            data_.game[data_.room_num].enemy = data_.player[user_id].enemy
        if data_.user_num % 2 == 0:
            data_.game[data_.room_num].enemy = data_.player[user_id]
            data_.player[user_id].enemy = data_.game[data_.room_num].player
            data_.game[data_.room_num].player.enemy = data_.player[user_id]
            data_.game[data_.room_num].player.energy -= 1
            data_.room_num += 1
            print(f"用户{data_.game[data_.room_num-1].player.id}和用户{data_.game[data_.room_num-1].enemy.id}加入游戏{data_.room_num}")
        print(f"用户{user_id}加入游戏")
        data_.message_log[data_.player[user_id].room_num] = "游戏开始!\n"
    count_ku = len(data_.player[user_id].cards)
    player_card_type = []
    for i in range(count_ku):
        if data_.player[user_id].cards[i].type == CardType.ATTACK:
            player_card_type.append("攻击")
        elif data_.player[user_id].cards[i].type == CardType.DEFENSE:
            player_card_type.append("防御")
        elif data_.player[user_id].cards[i].type == CardType.FUNCTION:
            player_card_type.append("功能")
        elif data_.player[user_id].cards[i].type == CardType.LUCKEY:
            player_card_type.append("运势")
    player_hand_card_type = []
    for i in range(len(data_.player[user_id].hand_cards)):
        if data_.player[user_id].hand_cards[i].type == CardType.ATTACK:
            player_hand_card_type.append("攻击")
        elif data_.player[user_id].hand_cards[i].type == CardType.DEFENSE:
            player_hand_card_type.append("防御")
        elif data_.player[user_id].hand_cards[i].type == CardType.FUNCTION:
            player_hand_card_type.append("功能")
        elif data_.player[user_id].hand_cards[i].type == CardType.LUCKEY:
            player_hand_card_type.append("运势")

    if data_.player[user_id].enemy.health < 0:
        data_.player[user_id].enemy.health = 0

    if data_.player[user_id].health < 0:
        data_.player[user_id].health = 0

    return [{
            "message": "已读取后端数据",
            "exists":exists,
            "repeat":data_.repeat_[user_id],
            "count_ku":count_ku,
            "count_hand_cards":len(data_.player[user_id].hand_cards),
            "library_card_name":library_card_name,
            "library_card_cost":library_card_cost,
            "library_card_desc":library_card_desc,
            "library_card_type":library_card_type,
            "player_card_type":player_card_type,
            "player_hand_card_type":player_hand_card_type,
            "player_health":data_.player[user_id].health,
            "enemy_health":data_.player[user_id].enemy.health,
            "player_energy":data_.player[user_id].energy,
            "enemy_energy":data_.player[user_id].enemy.energy,
            "player_shield":data_.player[user_id].shield,
            "enemy_shield":data_.player[user_id].enemy.shield,
            "player_block":data_.player[user_id].block,
            "enemy_block":data_.player[user_id].enemy.block,
            "player_hand_cards":data_.player[user_id].hand_cards,
            "enemy_hand_cards":data_.player[user_id].enemy.hand_cards,
            "player_cards":data_.player[user_id].cards,
            "enemy_cards":data_.player[user_id].enemy.cards,
            "count_library":len(card_library),
            "message_log":data_.message_log[data_.player[user_id].room_num],
            },
    ]


@app.post("/load_cards")
async def load_cards(request: Request):
    data = await request.json()
    user_id = data["user_id"]
    data_.player[user_id].cards = []
    cards = sql_function.load_cards(user_id)
    for card_name in cards:
        card = card_library_dict[card_name]
        data_.player[user_id].cards.append(card)
    if len(data_.player[user_id].cards) == 10:
        data_.player[user_id].get_hand_card()
    return {"message": "读取成功"}


@app.post("/save_cards")
async def save_cards(request: Request):
    data = await request.json()
    user_id = data["user_id"]
    cards=[]
    for card in data_.player[user_id].cards:
        cards.append(card.name)
    sql_function.save_cards(user_id, cards)
    return {"message": "保存成功"}


@app.get("/login")
async def login():
    return FileResponse("templates/login.html")


@app.post("/login")
async def login(request: Request):
    data = await request.json()
    username = data["username"]
    password = data["password"]
    message = sql_function.login(username, password)
    return message









uvicorn.run(app, host="0.0.0.0", port=8000)
