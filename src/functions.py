import random

from MiniSpire.src.cards import Card
from MiniSpire.src.config import game_config
from MiniSpire.src.constants import CardFunction
from MiniSpire.src.entities import Targets


def give_card_function_1(target: Targets, card: Card):
    message = "使用出错"
    if card.function == CardFunction.SHIELD:
        message = function_shield(target, card)
    elif card.function == CardFunction.BLOCK:
        message = function_block(target, card)
    elif card.function == CardFunction.DAMAGE:
        message = function_damage(target, card)
    elif card.function == CardFunction.ENERGY:
        message = function_energy(target, card)
    elif card.function == CardFunction.RANDOM_ENERGY:
        message = function_random_energy(target, card)
    elif card.function == CardFunction.RANDOM_DAMAGE_ATTACK:
        message = function_random_damage_attack(target, card)
    elif card.function == CardFunction.RANDOM_DAMAGE_DEFENSE:
        message = function_random_damage_defense(target, card)
    elif card.function == CardFunction.EXTRA_DAMAGE:
        message = function_extra_damage(target, card)
    elif card.function == CardFunction.CHANGE_CARD:
        message = function_change_card(target, card)
    elif card.function == CardFunction.DAMAGE_REDUCTION:
        message = function_damage_reduction(target, card)
    return message

def give_card_function_2(target1: Targets, target2: Targets, card: Card):
    message = "使用出错"
    if card.function == CardFunction.LUCKEY:
        message = function_lucky(target1, target2, card)
    elif card.function == CardFunction.CHANGE_HEALTH:
        message = function_change_health(target1, target2, card)
    return message

def get_damage(card: Card,target: Targets):
    damage = card.value - target.block
    if damage > 0:
        true_damage = int(damage * (1 + target.extra_damage / 100)*(1-target.damage_reduction/100))
        return true_damage
    else:
        return 0

def lucky_check_self(card: Card,target: Targets):
    return random.randint(0, 100) <= card.value + (card.value * target.lucky)

def lucky_check_enemy(card: Card,target: Targets):
    return random.randint(0, 100) <= card.value - (card.value * target.lucky)

def function_shield(target: Targets, card: Card):
    target.shield += card.value
    message = f"获得{card.value}点护盾"
    return message

def function_block(target: Targets, card: Card):
    target.block += card.value
    message = f"获得{card.value}点防御"
    return message



def function_damage_reduction(target: Targets, card: Card):
    target.damage_reduction += card.value
    if target.damage_reduction > 90:
        target.damage_reduction = 90
    message = f"获得{card.value}%伤害减免(上限90%)"
    return message


def function_damage(target: Targets, card: Card):
    if target.shield > 0 and card.value > target.block:
        target.shield -= 1
        target.block = 0
        message = f"造成0伤害,{get_damage(card,target)}点伤害被抵御"
        return message
    damage = card.value - target.block
    if damage > 0:
        true_damage = get_damage(card,target)
        target.health -= true_damage
        block_damage = target.block
        target.block = 0
        message = f"造成{true_damage}点伤害,{block_damage}点伤害被护盾格挡"
    else:
        target.block -= card.value
        message = f"造成0伤害,{card.value}点伤害被护盾格挡"
    target.extra_damage = 0
    return message

def function_energy(target: Targets, card: Card):
    target.extra_energy += card.value
    message = f"下回合将获得{card.value}点额外能量"
    return message

def function_random_energy(target: Targets, card: Card):
    if random.randint(0, 100) <= card.value + (card.value * target.lucky):
        target.energy += 3
        message = f"占卜判定成功,获得3点能量"
    else:
        message = "占卜判定失败,未获得能量"
    return message

def function_random_damage_attack(target: Targets, card: Card):
    if random.randint(1, 100) <= card.value - (card.value * target.lucky):
        target.health = 0
        message = "赌徒判定成功,有人要倒霉了"
    else:
        message = "赌徒判定失败,下一次说不定就成功了"
    return message

def function_random_damage_defense(target: Targets, card: Card):
    if random.randint(0, 100) <= card.value + (card.value * target.lucky):
        target.health = game_config.BASE_HEALTH
        message = "赌徒判定成功,所有生命被恢复"
    else:
        message = "赌徒判定失败,下一次说不定就成功了"
    return message

def function_extra_damage(target: Targets, card: Card):
    target.extra_damage += card.value
    message = f"下次造成的伤害增加{card.value}%"
    return message

def function_change_card(target: Targets, card: Card):
    num = len(target.hand_cards)
    target.hand_cards = []
    target.get_hand_card(num)
    message = "已更换所有手牌,未消耗能量"
    if random.randint(1, 100) <= card.value * (1 / (1 + target.lucky)):
        target.energy -= 1
        if target.energy < 0:
            target.energy = 0
        message = "已更换所有手牌,消耗1点能量"
    return message

def function_lucky(target1: Targets, target2: Targets, card: Card):
    target1.lucky += card.value
    target2.lucky -= card.value
    message = f"本回合幸运值提升{card.value}点"
    return message

def function_change_health(target1: Targets, target2: Targets, card: Card):
    target1.health, target2.health = target2.health, target1.health
    message = "交换了双方的血量"
    return message
