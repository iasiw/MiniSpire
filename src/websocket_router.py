from fastapi import APIRouter, WebSocket, WebSocketDisconnect

import MiniSpire.src.data as data_
from MiniSpire.src import config

router = APIRouter()
@router.get("/getWebSocketUrl")
async def get_websocket_url():
    return {"websocket_url": config.game_config.WEBSOCKET_URL}
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    user_id = websocket.query_params.get("userId")
    data_.connect_dict[user_id] = websocket
    print(f"{user_id}已连接")
    data_.use_card = False
    try:
        while True:
            message = await websocket.receive_text()
            print(f"{user_id}已收到消息：{message}")
    except WebSocketDisconnect:
        del data_.connect_dict[user_id]
        if data_.player[user_id].enemy.id != 0 and data_.player[user_id].enemy.id in data_.connect_dict.keys() and data_.use_card:
            try:
                print(f"{user_id}发送消息给{data_.player[user_id].enemy.id}：reload")
                await data_.connect_dict[data_.player[user_id].enemy.id].send_text("reload")
            except WebSocketDisconnect:
                print(f"{user_id}发送消息给{data_.player[user_id].enemy.id}失败")
        print(f"{user_id}已断开连接")
