
"""
遗传算法
状态基因：6位状态基因 共36位基因
基因1：自己血量影响策略百分比 6位基因
基因2：对方血量影响策略百分比 6位基因
基因3：对方防御影响策略百分比 6位基因
基因4：对方护盾影响策略百分比 6位基因
基因5：自己能量影响策略百分比 6位基因
基因6：对方额外能量影响策略百分比 6位基因

卡片基因：12位卡片基因 共12位基因
"""
from MiniSpire.src.config import game_config


def get_self_health_infect(gene):
    self_health_infect = gene[0:6]
    self_health_infect = int("".join(self_health_infect),2)
    return self_health_infect

def get_enemy_health_infect(gene):
    enemy_health_infect = gene[6:12]
    enemy_health_infect = int("".join(enemy_health_infect),2)
    return enemy_health_infect

def get_enemy_defense_infect(gene):
    enemy_defense_infect = gene[12:18]
    enemy_defense_infect = int("".join(enemy_defense_infect),2)
    return enemy_defense_infect

def get_enemy_shield_infect(gene):
    enemy_shield_infect = gene[18:24]
    enemy_shield_infect = int("".join(enemy_shield_infect),2)
    return enemy_shield_infect

def get_self_energy_infect(gene):
    self_energy_infect = gene[24:30]
    self_energy_infect = int("".join(self_energy_infect),2)
    return self_energy_infect

def get_enemy_extra_energy_infect(gene):
    enemy_extra_energy_infect = gene[30:36]
    enemy_extra_energy_infect = int("".join(enemy_extra_energy_infect),2)
    return enemy_extra_energy_infect

def get_self_block_infect(gene):
    self_block_infect = gene[36:42]
    self_block_infect = int("".join(self_block_infect),2)
    return self_block_infect

def get_self_shield_infect(gene):
    self_shield_infect = gene[42:48]
    self_shield_infect = int("".join(self_shield_infect),2)
    return self_shield_infect

def get_self_luck_infect(gene):
    self_luck_infect = gene[48:54]
    self_luck_infect = int("".join(self_luck_infect),2)
    return self_luck_infect
def get_self_extra_damage_infect(gene):
    self_extra_damage_infect = gene[54:60]
    self_extra_damage_infect = int("".join(self_extra_damage_infect),2)
    return self_extra_damage_infect

def get_card_gene_by_id(gene, card_id,):
    card_gene = gene[(game_config.GENE_STATE_LENGTH*3) +( card_id * 3* game_config.GENE_STATE_LENGTH): (game_config.GENE_STATE_LENGTH*6) +( card_id * 3* game_config.GENE_STATE_LENGTH)]
    infect = []
    for i in range(game_config.GENE_STATE_LENGTH):
        infect.append(4*int(card_gene[i*3])+int(2*card_gene[i*3+1])+int(card_gene[i*3+2]))
    return infect

def get_score(card_id,ai,enemy):
    score = 0
    if card_id == 1:#普通攻击
        if enemy.block >= 6:
            score -= 6
        elif enemy.shield == 1:
            score += 0
        elif ai.extra_damage > 0:
            score += 40
        else:
            score += 15
    elif card_id == 2:#强力攻击
        if enemy.block >= 15:
            score -= 15
        elif enemy.shield > 0:
            score -= 20
        elif ai.extra_damage > 0:
            score += 200
        else:
            score += 40
    elif card_id == 3:#全力攻击
        if enemy.block >= 25:
            score -= 25
        elif enemy.shield > 0:
            score -= 35
        elif ai.extra_damage > 0:
            score += 400
        else:
            score += 60
    elif card_id == 4:#简单防御
        if ai.health <= 50:
            score += 20
        if ai.health <= 30:
            score += 20
        elif ai.shield > 0:
            score -= 30
        elif ai.extra_damage > 0:
            score -= 50
        else:
            score += 20
    elif card_id == 5:#套盾
        if ai.health <= 50:
            score += 20
        if ai.health <= 30:
            score += 20
        elif ai.shield > 0:
            score -= 50
        elif ai.energy >= 5:
            score += 80
        elif ai.extra_damage > 0:
            score -= 50
        elif enemy.extra_energy > 0:
            score += 90
        else:
            score += 60
    elif card_id == 6:#蓄力
        if ai.energy == 1:
            score += 70
    elif card_id == 7:#占卜
        if ai.lucky >= 0:
            score += 80*ai.lucky
    elif card_id == 8:#赌徒攻
        if ai.health <= 20 and enemy.health >= 80 and ai.lucky >= 1:
            score += 40
        else:
            score -= 500
    elif card_id == 9:#赌徒守
        if ai.health <= 60 and ai.lucky >= 1:
            score += (60 - ai.health)*(ai.lucky+1)
    elif card_id == 10:#收盘
        if ai.health < enemy.health:
            score +=10*(enemy.health-ai.health)
        else:
            score -= 10*(ai.health-enemy.health+2)
    elif card_id == 11:#涂毒
        if enemy.shield > 0:
            score -= 500
        elif enemy.block >= 10:
            score +=10
        else:
            score += 60
        if ai.energy <= 2:
            score -= 100
    elif card_id == 12:#幸运儿
        if ai.energy <= 1:
            score -= 200
        else:
            score += 20
        if ai.lucky >= 2:
            score -= 100
    return score
