import os

class game_config:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'data.db')}"
    GAME_NAME = "MiniSpire"
    GAME_VERSION = "1.0.0"
    GAME_AUTHOR = "iasiw"
    GAME_LICENSE = "MIT"
    BASE_ENERGY = 3
    BASE_CARD_NUM = 10
    BASE_HAND_CARD = 6
    BASE_HEALTH = 100
    WEBSOCKET_URL = "ws://localhost:8000"



    GENE_STATE_LENGTH = 10
    GENE_STATE_NUM = 6
    GENE_CARD_LENGTH = 12
    GENE_CARD_NUM = 3
    GENE_LENGTH = GENE_STATE_LENGTH*GENE_STATE_NUM+(GENE_CARD_LENGTH*GENE_CARD_NUM*GENE_STATE_LENGTH)


    CROSSOVER_POS = 0
    """
    交叉位置
    0表示随机选择
    
    1~10:状态基因
        1.#玩家血量
        2.#敌人血量
        3.#敌人防御
        4.#敌人护盾
        5.#玩家能量
        6.#敌人额外能量
        7.#玩家防御
        8.#玩家护盾
        9.#玩家幸运
        10.#玩家额外伤害
    11~22:卡牌基因
        11.#普通攻击
        12.#强力攻击
        13.#全力攻击
        14.#简单防御
        15.#套盾
        16.#蓄力
        17.#占卜
        18.#赌徒攻
        19.#赌徒防
        20.#收盘
        21.#涂毒
        22.#幸运儿
    """


    AI_TRAINING = 1