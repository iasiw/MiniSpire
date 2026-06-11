import collections

import MiniSpire.src.cards as cards
from MiniSpire.src.cards import card_library, card_id_dict
from MiniSpire.src.constants import State, Turn
from MiniSpire.src.config import game_config
from MiniSpire.src.entities import Targets
import MiniSpire.src.functions as functions
from MiniSpire.src.sql_function import load_best_gene
from MiniSpire.src.training_function import (
    get_card_gene_by_id,
    get_self_health_infect,
    get_enemy_health_infect,
    get_enemy_defense_infect,
    get_enemy_shield_infect,
    get_self_energy_infect,
    get_enemy_extra_energy_infect,
    get_self_block_infect,
    get_self_luck_infect,
    get_self_shield_infect,
    get_self_extra_damage_infect,
    get_score
)

import random

class Play:
    def __init__(self,target1: Targets,target2: Targets):
        self.state = State.PLAYING
        self.player = target1
        self.enemy = target2
        self.turn = Turn.PLAYERTURN1
        self.round = 1
        self.score = 0
        self.count_dict = collections.defaultdict(int)


    def player_get_cards(self, n: int,skip:bool=True, library: dict = cards.card_library):
        if n < 1:
            return 0
        cards.print_cards(self.player.cards)
        print("可添加的卡牌：")
        cards.print_cards_dict(library)
        print(f"(当前待添加{n}张卡片)")
        if skip:
            print("此次添加可以跳过(负数表示跳过)")
        else:
            print("此次添加不能跳过")
        print("请选择要添加的卡片编号(进入卡牌查看详情)：")
        try:
            card_id = int(input())
        except ValueError:
            print("输入的不是整数,请重新输入")
            return self.player_get_cards(n, skip, library)
        if card_id < 0 and skip:
            return self.player_get_cards(n, skip, library)
        if card_id not in library.keys():
            print("未找到该卡片编号,请重新输入")
            return self.player_get_cards(n, skip, library)
        cards.print_card(library[card_id])
        print("请输入要添加的卡片数量(0表示不添加)：")
        try:
            num = int(input())
        except ValueError:
            print("输入的不是整数,请重新输入")
            return self.player_get_cards(n, skip, library)
        if num > n or num < 0:
            print(f"最多只能添加{n}张卡片,请重新输入")
            return self.player_get_cards(n, skip, library)
        for i in range(num):
            self.player.cards.append(library[card_id])
        n -= num
        return self.player_get_cards(n, skip, library)

    @classmethod
    def use_card(cls, target1: Targets, target2: Targets, card: cards.Card):
        message = "卡片使用出错"
        if card.cost > target1.energy:
            message = "能量不足"
            return message
        else:
            target1.energy -= card.cost
        if card.target == cards.CardTarget.SELF:
            message= functions.give_card_function_1(target1,card)
            return message
        elif card.target == cards.CardTarget.ENEMY:
            message= functions.give_card_function_1(target2,card)
            return message
        elif card.target == cards.CardTarget.ALL:
            message = functions.give_card_function_2(target1,target2,card)
            return message
        return message

    def start_round(self):
        self.player.energy = game_config.BASE_ENERGY + self.player.extra_energy
        self.enemy.energy = game_config.BASE_ENERGY + self.enemy.extra_energy
        self.player.extra_energy = 0
        self.enemy.extra_energy = 0
        self.enemy.extra_damage = 0
        self.player.extra_damage = 0
        if game_config.AI_TRAINING == 1:
            self.turn = Turn.ENEMYTURN
        else:
            self.turn = Turn.PLAYERTURN1
        self.player.block = 0
        self.player.shield = 0
        self.player.damage_reduction = 0
        self.round += 1
        #print(f"当前回合：{self.round}")
        return {"message":f"新的回合开始了,当前回合：{self.round}","use_card":True,"used_card":None}

    def player1_round(self, card_id: int)->dict:
        #print("玩家行动")
        #cards.print_cards(self.player.hand_cards)
        #print("请选择要使用的的卡片编号(0结束回合)：")
        #print(f"当前能量：{self.player.energy}")
        if card_id == 0:
            if self.player.enemy.id == 0:
                self.turn = Turn.AITURN
            else:
                self.turn = Turn.PLAYERTURN2
            self.enemy.shield = 0
            self.enemy.block = 0
            self.enemy.damage_reduction = 0
            self.player.lucky = 0
            self.enemy.lucky = 0
            self.player.get_hand_card()
            return {"message":"玩家1结束了回合","use_card":True,"used_card":None}  #if card_id not in range(len(self.player.hand_cards) + 1):
            #print("输入错误,请重新输入")
            #return {"message":"输入错误,请重新输入","use_card":True}

        else:
            if self.player.energy >= self.player.hand_cards[card_id - 1].cost:
                can_use = True
            else:
                can_use = False
            if can_use:
                used_card = self.player.hand_cards[card_id - 1]
                message= Play.use_card(self.player, self.enemy, self.player.hand_cards[card_id - 1])
                self.player.hand_cards.pop(card_id - 1)
                return {"message":f"玩家1使用了\"{used_card.name}\", {message}","use_card":True,"used_card":used_card}
            else:
                return {"message":f"玩家1试图使用\"{self.player.hand_cards[card_id - 1].name}\",但能量不足","use_card":False,"used_card":None}

    def player2_round(self, card_id: int)->dict:
        if card_id == 0:
            self.turn = Turn.START
            self.player.shield = 0
            self.player.block = 0
            self.player.damage_reduction = 0
            self.player.lucky = 0
            self.enemy.lucky = 0
            self.enemy.get_hand_card()
            return {"message":"玩家2结束了回合","use_card":True,"used_card":None}
        else:
            if self.enemy.energy >= self.enemy.hand_cards[card_id - 1].cost:
                can_use = True
            else:
                can_use = False
            if can_use:
                used_card = self.enemy.hand_cards[card_id - 1]
                message= Play.use_card(self.enemy, self.player, self.enemy.hand_cards[card_id - 1])
                self.enemy.hand_cards.pop(card_id - 1)
                return {"message":f"玩家2使用了\"{used_card.name}\", {message}","use_card":True,"used_card":used_card}
            else:
                return {"message":f"玩家2试图使用\"{self.enemy.hand_cards[card_id - 1].name}\",但能量不足","use_card":False,"used_card":None}

    def enemy_round(self):
        #print("敌人行动")
        if self.player.energy != 0:
            use_card = False
            while not use_card:
                if self.player.health < game_config.BASE_HEALTH/4 and self.player.health < self.enemy.health and random.randint(0,2) == 3:
                    card_id = 10
                elif self.player.energy >= 4 and self.enemy.shield == 0 and random.randint(0,2) == 0:
                    card_id = 11
                elif random.randint(0,1) == 0:
                    if self.player.health <= game_config.BASE_HEALTH/2 and random.randint(0,1) == 0:
                        card_id =random.randint(4,5)
                    elif self.player.health >= game_config.BASE_HEALTH*3/4 and random.randint(0,1) == 0:
                        card_id =random.randint(1,3)
                    else:
                        card_id = random.randint(1,3)
                elif self.player.energy >= 3 and random.randint(0,3) == 0:
                    card_id = 12
                elif random.randint(0,1) == 0:
                    card_id = 6
                else:
                    card_id = random.randint(1,9)
                message = self.use_card(self.player, self.enemy, cards.card_library[card_id])
                if message != "卡片使用出错" and message != "能量不足":
                    use_card = True
        else:
            self.turn = Turn.AITURN
            self.player.lucky = 0
            self.enemy.lucky = 0
            return {"message":"敌人结束了它的回合","use_card":True,"used_card":None}
        return {"message":f"敌人使用了\"{cards.card_library[card_id].name}\", {message}","use_card":True,"used_card":cards.card_library[card_id]}


    def rounds(self, card_id: int)->dict:
        if self.player.check_dead():
            print("玩家死亡")
            self.state = State.LOST
            return {"message":"玩家死亡,游戏结束"}
        if self.enemy.check_dead():
            print("敌人死亡")
            self.state = State.WON
            return {"message":"敌人死亡,游戏结束"}
        if self.turn == Turn.PLAYERTURN1:
            return self.player1_round(card_id)
        if self.turn == Turn.PLAYERTURN2:
            return self.player2_round(card_id)
        if self.turn == Turn.AITURN:
            return self.ai_round(list(map(str,load_best_gene())))
        if self.turn == Turn.START:
            for card in self.enemy.hand_cards:
                print(card.name,end = "    ")
            return self.start_round()
        #if self.turn == Turn.ENDTURN:
            #return self.end_round()
        return {"message":"未知状态,程序异常"}

    def ai_round(self,gene):
        self_health_infect = get_self_health_infect(gene)
        infect1 = (self_health_infect * self.player.health)
        enemy_health_infect = get_enemy_health_infect(gene)
        infect2 = (enemy_health_infect * self.enemy.health)
        enemy_defense_infect = get_enemy_defense_infect(gene)
        infect3 = (enemy_defense_infect * self.enemy.block)*10
        enemy_shield_infect = get_enemy_shield_infect(gene)
        infect4 = (enemy_shield_infect * self.enemy.shield)*100
        self_energy_infect = get_self_energy_infect(gene)
        infect5 = (self_energy_infect * self.player.energy)*100
        enemy_extra_energy_infect = get_enemy_extra_energy_infect(gene)
        infect6 = (enemy_extra_energy_infect * self.player.energy)*100
        self_block_infect = get_self_block_infect(gene)
        infect7 = (self_block_infect * self.player.block)*100
        self_shield_infect = get_self_shield_infect(gene)
        infect8 = (self_shield_infect * self.player.shield)*100
        self_luck_infect = get_self_luck_infect(gene)
        infect9 = (self_luck_infect * self.player.lucky)*100
        self_extra_damage_infect = get_self_extra_damage_infect(gene)
        infect10 = (self_extra_damage_infect * self.player.extra_damage)*100

        infect = [infect1,infect2,infect3,infect4,infect5,infect6,infect7,infect8,infect9,infect10]
        card_infect = []
        for i in range(12):
            card_infect.append(get_card_gene_by_id(gene, i+1))
        #"""
        card_list = []
        for i in range(len(self.enemy.hand_cards)):
            temp = 0
            for j in range(game_config.GENE_STATE_LENGTH):
                temp += card_infect[card_id_dict[self.enemy.hand_cards[i].name]-1][j]*infect[j]
            card_list.append(temp)
        #"""

        """
        for i in range(12):
            temp =0
            for j in range(game_config.GENE_STATE_LENGTH):
                temp += card_infect[i][j]*infect[j]
            card_infect[i] = temp
        #"""
        if card_list:
            card_id = card_id_dict[self.enemy.hand_cards.pop(card_list.index(max(card_list))).name]
        if card_list and self.enemy.energy >= card_library[card_id].cost:
            self.score += get_score(card_id,self.enemy,self.player)
            message = self.use_card(self.enemy, self.player, card_library[card_id])
            if game_config.AI_TRAINING == 1:
                return card_id
            return {"message":f"敌人使用了\"{card_library[card_id].name}\", {message}","use_card":True,"used_card":card_library[card_id]}
        else:
            self.turn = Turn.START
            self.score -= 100*(self.enemy.energy**2)
            self.score -= self.player.extra_damage
            self.enemy.get_hand_card()
            self.enemy.lucky = 0
            self.player.lucky = 0
            if game_config.AI_TRAINING == 1:
                return None
            return {"message":"敌人结束了它的回合","use_card":True,"used_card":None}

    def rounds_training(self, gene: list, gene1: list)->int:
        if self.round >= 50:
            self.state = State.LOST
        if self.enemy.check_dead():
            self.state = State.LOST
            self.score += (self.round*2)
            self.score -= self.count_dict[8]*70
            #print("玩家死亡")
            return self.score
        if self.player.energy >= 30:
            self.player.energy = 0
        if self.player.check_dead() :
            self.score += 1500
            self.score += self.enemy.health*5
            #print("敌人死亡")
            self.state = State.WON
            return self.score
        if self.turn == Turn.START:
            self.start_round()
            #self.player.energy +=0
            #self.player.shield += self.round % 2
            return self.score
        if self.turn == Turn.AITURN:
            card_id = self.ai_round(gene)
            if card_id is not None:
                self.count_dict[card_id] += 1
            return self.score
        if self.turn == Turn.ENEMYTURN:
            self.ai_round_player(gene1)
            return self.score

    def ai_round_player(self,gene):
        self_health_infect = get_self_health_infect(gene)
        infect1 = (self_health_infect * self.enemy.health)
        enemy_health_infect = get_enemy_health_infect(gene)
        infect2 = (enemy_health_infect * self.player.health)
        enemy_defense_infect = get_enemy_defense_infect(gene)
        infect3 = (enemy_defense_infect * self.player.block)*10
        enemy_shield_infect = get_enemy_shield_infect(gene)
        infect4 = (enemy_shield_infect * self.player.shield)*100
        self_energy_infect = get_self_energy_infect(gene)
        infect5 = (self_energy_infect * self.enemy.energy)*100
        enemy_extra_energy_infect = get_enemy_extra_energy_infect(gene)
        infect6 = (enemy_extra_energy_infect * self.enemy.energy)*100
        self_block_infect = get_self_block_infect(gene)
        infect7 = (self_block_infect * self.enemy.block)*100
        self_shield_infect = get_self_shield_infect(gene)
        infect8 = (self_shield_infect * self.enemy.shield)*100
        self_luck_infect = get_self_luck_infect(gene)
        infect9 = (self_luck_infect * self.enemy.lucky)*100
        self_extra_damage_infect = get_self_extra_damage_infect(gene)
        infect10 = (self_extra_damage_infect * self.enemy.extra_damage)*100

        infect = [infect1,infect2,infect3,infect4,infect5,infect6,infect7,infect8,infect9,infect10]
        card_infect = []
        for i in range(12):
            card_infect.append(get_card_gene_by_id(gene, i+1))
        #"""
        card_list = []
        for i in range(len(self.player.hand_cards)):
            temp = 0
            for j in range(game_config.GENE_STATE_LENGTH):
                temp += card_infect[card_id_dict[self.player.hand_cards[i].name]-1][j]*infect[j]
            card_list.append(temp)
        #"""
        if card_list:
            card_id = card_id_dict[self.player.hand_cards.pop(card_list.index(max(card_list))).name]
        if card_list and self.player.energy >= card_library[card_id].cost:
            message = self.use_card(self.player, self.enemy, card_library[card_id])
            if game_config.AI_TRAINING == 1:
                return card_id
            return {"message":f"玩家使用了\"{card_library[card_id].name}\", {message}","use_card":True,"used_card":card_library[card_id]}
        else:
            self.turn = Turn.AITURN
            self.enemy.block =0
            self.enemy.shield =0
            self.player.get_hand_card()
            self.player.lucky = 0
            self.enemy.lucky = 0
            if game_config.AI_TRAINING == 1:
                return None
            return {"message":"玩家结束了它的回合","use_card":True,"used_card":None}
