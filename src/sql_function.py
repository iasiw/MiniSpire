
from MiniSpire.src.sql import UserPreference, SessionLocal, User


def save_cards(user_id: str, cards: list):
    session = SessionLocal()
    user_preference = UserPreference(id=user_id)
    user_preference.saved_cards = cards
    if session.query(UserPreference).filter(UserPreference.id == user_id).first() is None:
        session.add(user_preference)
    else:
        session.query(UserPreference).filter(UserPreference.id == user_id).update({"saved_cards": cards})
    session.commit()
    session.close()

def load_cards(user_id: str):
    session = SessionLocal()
    user_preference = session.query(UserPreference).filter(UserPreference.id == user_id).first()
    session.close()
    if user_preference is None:
        return []
    else:
        return user_preference.saved_cards

def login(username: str, password: str):
    session = SessionLocal()
    user = session.query(User).filter(User.username == username).first()
    if user is None:
        register(username, password)
        success = True
        message = "未找到用户,已自动注册"
    elif user.password != password:
        success = False
        message = "密码错误"
    else:
        success = True
        message = "登录成功"
    session.commit()
    session.close()
    return {"success": success, "message": message}

def register(username: str, password: str):
    session = SessionLocal()
    user = User(username=username, password=password)
    session.add(user)
    session.commit()
    session.close()

def check_user_exists(username: str):
    session = SessionLocal()
    user = session.query(User).filter(User.username == username).first()
    session.close()
    return user is not None
