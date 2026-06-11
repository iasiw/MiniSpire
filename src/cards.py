from dataclasses import dataclass

from MiniSpire.src.constants import CardType, CardTarget, CardFunction


@dataclass
class Card:
    name: str
    cost: int
    type: CardType
    target: CardTarget
    function: CardFunction
    value: int
    description:str



card_library = {
     1: Card(name="普通攻击",cost=1,type=CardType.ATTACK,target=CardTarget.ENEMY,function=CardFunction.DAMAGE,value=6,description="花费1点能量,对敌人造成6点伤害")
    ,2: Card(name="强力攻击",cost=2,type=CardType.ATTACK,target=CardTarget.ENEMY,function=CardFunction.DAMAGE,value=15,description="花费2点能量,造成15点伤害")
    ,3: Card(name="全力攻击",cost=3,type=CardType.ATTACK,target=CardTarget.ENEMY,function=CardFunction.DAMAGE,value=25,description="花费3点能量,造成25点伤害")
    ,4: Card(name="简单防御",cost=1,type=CardType.DEFENSE,target=CardTarget.SELF,function=CardFunction.BLOCK,value=10,description="花费1点能量,获得10点格挡")
    ,5: Card(name="套盾",cost=1,type=CardType.DEFENSE,target=CardTarget.SELF,function=CardFunction.SHIELD,value=1,description="花费1点能量,获得1层护盾")
    ,6: Card(name="蓄力",cost=1,type=CardType.FUNCTION,target=CardTarget.SELF,function=CardFunction.ENERGY,value=1,description="花费1点能量,下回合获得1点能量")
    ,7: Card(name="占卜",cost=1,type=CardType.FUNCTION,target=CardTarget.SELF,function=CardFunction.RANDOM_ENERGY,value=30,description="花费1点能量,30%概率获得3点能量")
    ,8: Card(name="赌徒(攻)",cost=1,type=CardType.FUNCTION,target=CardTarget.ENEMY,function=CardFunction.RANDOM_DAMAGE_ATTACK,value=2,description="花费1点能量,2%概率秒杀敌人")
    ,9:Card(name="赌徒(守)",cost=3,type=CardType.FUNCTION,target=CardTarget.SELF,function=CardFunction.RANDOM_DAMAGE_DEFENSE,value=10,description="花费3点能量,15%概率恢复所有生命")
    ,10:Card(name="收盘",cost=5,type=CardType.FUNCTION,target=CardTarget.ALL,function=CardFunction.CHANGE_HEALTH,value=0,description="花费5点能量,交换双方的血量")
    ,11:Card(name="涂毒",cost=1,type=CardType.FUNCTION,target=CardTarget.ENEMY,function=CardFunction.EXTRA_DAMAGE,value=100,description="花费1点能量,使本回合内敌人下一次受到的伤害增加100%")
    ,12:Card(name="幸运儿",cost=1,type=CardType.LUCKEY,target=CardTarget.ALL,function=CardFunction.LUCKEY,value=1,description="花费1点能量,本回合幸运值提升1点")
    ,13:Card(name="制衡",cost=0,type=CardType.FUNCTION,target=CardTarget.SELF,function=CardFunction.CHANGE_CARD,value=30,description="更换所有手牌,30%概率花费一点能量")



    #,13: Card(name="烈火刀刀爆",cost=0,type=CardType.ATTACK,target=CardTarget.ENEMY,function=CardFunction.DAMAGE,value=999,description="开发者模式卡牌,一刀999")
}
ai_card_library = {
     1: Card(name="普通攻击",cost=1,type=CardType.ATTACK,target=CardTarget.ENEMY,function=CardFunction.DAMAGE,value=6,description="花费1点能量,对敌人造成6点伤害")
    ,2: Card(name="强力攻击",cost=2,type=CardType.ATTACK,target=CardTarget.ENEMY,function=CardFunction.DAMAGE,value=15,description="花费2点能量,造成15点伤害")
    ,3: Card(name="全力攻击",cost=3,type=CardType.ATTACK,target=CardTarget.ENEMY,function=CardFunction.DAMAGE,value=25,description="花费3点能量,造成25点伤害")
    ,4: Card(name="简单防御",cost=1,type=CardType.DEFENSE,target=CardTarget.SELF,function=CardFunction.BLOCK,value=10,description="花费1点能量,获得10点格挡")
    ,5: Card(name="套盾",cost=1,type=CardType.DEFENSE,target=CardTarget.SELF,function=CardFunction.SHIELD,value=1,description="花费1点能量,获得1层护盾")
    ,6: Card(name="蓄力",cost=1,type=CardType.FUNCTION,target=CardTarget.SELF,function=CardFunction.ENERGY,value=1,description="花费1点能量,下回合获得1点能量")
    ,
}
card_library_dict = {card.name: card for card in card_library.values()}
card_id_dict = {card.name: card_id for (card_id,card) in card_library.items()}
"""enemy_card_library = {
     1: Card(name="普通攻击", cost=1, type=CardType.ATTACK, target=CardTarget.ENEMY, function=CardFunction.DAMAGE,value=6, description="花费1点能量,对敌人造成6点伤害")
    ,2: Card(name="强力攻击", cost=2, type=CardType.ATTACK, target=CardTarget.ENEMY, function=CardFunction.DAMAGE,value=15, description="花费2点能量,造成15点伤害")
    ,3: Card(name="全力攻击", cost=3, type=CardType.ATTACK, target=CardTarget.ENEMY, function=CardFunction.DAMAGE,value=25, description="花费3点能量,造成25点伤害")
    ,4: Card(name="简单防御", cost=1, type=CardType.DEFENSE, target=CardTarget.SELF, function=CardFunction.BLOCK,value=10, description="花费1点能量,获得10点格挡")
    ,5: Card(name="套盾", cost=1, type=CardType.DEFENSE, target=CardTarget.SELF, function=CardFunction.SHIELD,value=1, description="花费1点能量,获得1层护盾")
    ,6: Card(name="蓄力", cost=1, type=CardType.FUNCTION, target=CardTarget.SELF, function=CardFunction.ENERGY,value=1, description="花费1点能量,下回合获得1点能量")
    ,7: Card(name="占卜", cost=1, type=CardType.FUNCTION, target=CardTarget.SELF, function=CardFunction.RANDOM_ENERGY,value=30, description="花费1点能量,30%概率获得3点能量")
    ,8: Card(name="赌徒(攻)", cost=1, type=CardType.FUNCTION, target=CardTarget.ENEMY,function=CardFunction.RANDOM_DAMAGE_ATTACK, value=2, description="花费1点能量,2%概率秒杀敌人")
    ,9: Card(name="赌徒(守)", cost=3, type=CardType.FUNCTION, target=CardTarget.SELF,function=CardFunction.RANDOM_DAMAGE_DEFENSE, value=10, description="花费3点能量,15%概率恢复所有生命")
    ,10: Card(name="收盘", cost=5, type=CardType.FUNCTION, target=CardTarget.ALL, function=CardFunction.CHANGE_HEALTH,value=0, description="花费5点能量,交换双方的血量")
    ,11: Card(name="涂毒", cost=1, type=CardType.FUNCTION, target=CardTarget.ENEMY, function=CardFunction.EXTRA_DAMAGE,value=100, description="花费1点能量,使本回合内敌人下一次受到的伤害增加100%")
    ,12: Card(name="幸运儿", cost=1, type=CardType.LUCKEY, target=CardTarget.ALL, function=CardFunction.LUCKEY, value=1, description="花费1点能量,本回合幸运值提升1点")
}"""
library_card_name = {key: card_library[key].name for key in card_library.keys()}
library_card_cost = {key: card_library[key].cost for key in card_library.keys()}
library_card_desc = {key: card_library[key].description for key in card_library.keys()}
library_card_type = {}
for key in card_library.keys():
    if card_library[key].type == CardType.ATTACK:
        library_card_type[key] = "攻击"
    elif card_library[key].type == CardType.DEFENSE:
        library_card_type[key] = "防御"
    elif card_library[key].type == CardType.FUNCTION:
        library_card_type[key] = "功能"
    elif card_library[key].type == CardType.LUCKEY:
        library_card_type[key] = "运势"



def find_card_by_name(name):
    return card_library_dict[name]

"""def print_cards_dict(library: dict):
    print("-------------------------------------------------")
    for card in library.keys():
        if card % 3 == 1 and card != 1:
            print()
        print(f"\t{card :3}.{library[card].name:<7}", end="")
    print()
    print("-------------------------------------------------")
    return

def print_card(card: Card):
    print("----------------------")
    print("卡片信息：")
    print(f"{card.description}")
    print("----------------------")


def print_cards(cards: list):
    print("当前卡牌：")
    print("-------------------------------------------------")
    for i in range(len(cards)):
        if i % 3 == 0 and i != 0:
            print()
        print(f"\t{i+1 :3}.{cards[i].name:<7}", end="")
    print()
    print("-------------------------------------------------")"""

