import random
from MiniSpire.src.config import game_config
from MiniSpire.src.constants import State, Turn
from MiniSpire.src.entities import Targets
from MiniSpire.src.genetic_algorithm import example_fitness_function
from MiniSpire.src.play import Play
from MiniSpire.src.sql_function import save_best_gene, load_best_gene, load_population
from MiniSpire.src.training_function import get_self_health_infect, get_enemy_health_infect, get_enemy_defense_infect, \
    get_enemy_shield_infect, get_self_energy_infect, get_enemy_extra_energy_infect, get_card_gene_by_id, \
    get_self_block_infect, get_self_luck_infect, get_self_shield_infect, get_self_extra_damage_infect

#随机生成基因
"""
individual = [random.randint(0, 1) for _ in range(game_config.GENE_LENGTH)]
save_best_gene(individual,0)
#"""
#自行导入基因
"""
gene=             [1, 1, 1, 1, 0, 1,    #玩家血量          #1
                   1, 1, 0, 0, 0, 0,    #敌人血量          #2
                   1, 1, 1, 0, 0, 1,    #敌人防御          #3
                   1, 1, 1, 1, 1, 1,    #敌人护盾          #4
                   1, 0, 1, 1, 0, 0,    #玩家能量          #5
                   1, 1, 0, 1, 1, 0,    #敌人额外能量       #6
                   1, 0, 1, 1, 0, 0,    #玩家防御          #7
                   1, 1, 1, 1, 1, 1,    #玩家护盾          #8
                   1, 0, 1, 1, 0, 0,    #玩家幸运          #9
                   1, 1, 0, 1, 1, 0,    #玩家额外伤害       #10
                 #玩家血量   敌人血量    敌人防御   敌人护盾    玩家能量  敌人额外能量   玩家幸运   玩家防御   玩家护盾   玩家额外伤害
                   0,0,1,    1,0,0,    0,0,0,    1,1,0,    1,0,1,    0,1,0,    1,0,1,                                   #1普通攻击
                   0,1,0,    1,0,1,    0,0,1,    0,0,0,    1,1,0,    1,0,0,    1,1,0                                    #2强力攻击
                   1,0,0,    1,0,1,    0,0,1,    0,0,0,    1,1,0,    0,1,0,    1,0,1,                                   #3全力攻击
                   1,0,1,    0,0,1,    0,1,0,    1,0,0,    0,0,0,    1,1,0,                                        #4简单防御
                   1,0,1,    0,0,0,    0,1,0,    1,0,0,    0,0,1,    1,1,0,                                        #5套盾
                   1,0,0,    0,1,0,    0,0,1,    0,0,0,    1,1,0,    1,0,1,                                        #6蓄力
                   1,0,0,    0,1,0,    0,0,0,    0,0,1,    1,1,0,    1,0,1,                                        #7占卜    
                   0,0,0,    1,1,0,    1,0,0,    1,0,1,    0,1,0,    0,0,1,                                        #8赌徒攻
                   1,1,0,    0,0,0,    0,1,0,    1,0,1,    0,0,1,    1,0,0,                                        #9赌徒守
                   1,0,0,    1,1,0,    0,0,0,    0,0,1,    1,0,1,    0,1,0,                                        #10收盘
                   1,1,0,    1,0,1,    0,0,0,    0,0,1,    1,0,0,    0,0,1,                                        #11涂毒
                   1,0,0,    0,1,0,    0,0,0,    0,0,1,    1,0,0,    0,1,0]                                        #12幸运
save_best_gene(gene,0)
#"""
#查看基因
"""
num = 2
count = 1
population = load_population(num)
for individual in population:
    gene =list(map(str,individual.gene))
    print("第",count,"个个体")
    count += 1
    print(len(gene))
    print(get_self_health_infect(gene))
    print(get_enemy_health_infect(gene))
    print(get_enemy_defense_infect(gene))
    print(get_enemy_shield_infect(gene))
    print(get_self_energy_infect(gene))
    print(get_enemy_extra_energy_infect(gene))
    print(get_self_block_infect(gene))
    print(get_self_shield_infect(gene))
    print(get_self_luck_infect(gene))
    print(get_self_extra_damage_infect(gene))
    print("普通攻击:",get_card_gene_by_id(gene, 1))
    print("强力攻击:",get_card_gene_by_id(gene, 2))
    print("全力攻击:",get_card_gene_by_id(gene, 3))
    print("简单防御:",get_card_gene_by_id(gene, 4))
    print("套盾:",get_card_gene_by_id(gene, 5))
    print("蓄力:",get_card_gene_by_id(gene, 6))
    print("占卜:",get_card_gene_by_id(gene, 7))
    print("赌徒攻:",get_card_gene_by_id(gene, 8))
    print("赌徒守:",get_card_gene_by_id(gene, 9))
    print("收盘:",get_card_gene_by_id(gene, 10))
    print("涂毒:",get_card_gene_by_id(gene, 11))
    print("幸运:",get_card_gene_by_id(gene, 12))
#"""
#评估基因
#"""
num = 11
population =[individual.gene for individual in load_population(num)]
for i in range(len(population)):
    example_fitness_function(population[len(population)-i-1],population)



#"""