import random
from typing import Optional

import MiniSpire.src.cards as cards
from MiniSpire.src.config import game_config

class Targets:
    def __init__(self, health: int = game_config.BASE_HEALTH):
        self.health = health
        self.shield = 0
        self.block = 0
        self.damage_reduction = 0
        self.cards = []
        self.hand_cards = []
        self.energy = game_config.BASE_ENERGY
        self.extra_energy = 0
        self.extra_damage = 0
        self.lucky = 0
        self.enemy: Optional[Targets] = None
        self.room_num = 0
        self.id = 0

    def reset(self):
        self.health = game_config.BASE_HEALTH
        self.shield = 0
        self.block = 0
        self.damage_reduction = 0
        self.energy = game_config.BASE_ENERGY
        self.extra_energy = 0
        self.extra_damage = 0
        self.lucky = 0

    def check_dead(self):
        if self.health <= 0:
            return True
        else:
            return False

    def get_cards(self,n: int,card_id: int, skip:bool=True, library: dict = cards.card_library)->None:
        if n < 1:
            return
        #cards.print_cards(self.cards)
        #print("可添加的卡牌：")
        #cards.print_cards_dict(library)
        #print(f"(当前待添加{n}张卡片)")
        """if skip:
            print("此次添加可以跳过(负数表示跳过)")
        else:
            print("此次添加不能跳过")
        print("请选择要添加的卡片编号：")"""
        if card_id < 0 and skip:
            return
        if card_id not in library.keys():
            print("输入错误,请重新输入")
            return
        #print("添加的卡片数量：")
        num = 1
        if num > n or num < 0:
            #print(f"最多只能添加{n}张卡片,请重新输入")
            return
        for i in range(num):
            self.cards.append(library[card_id])
        n -= num
        return

    def get_hand_card(self, num: int = game_config.BASE_HAND_CARD):
        self.hand_cards = []
        n = len(self.cards)
        for i in range(num):
            random_num = random.randint(0, n - 1)
            self.hand_cards.append(self.cards[random_num])
        return self.hand_cards




