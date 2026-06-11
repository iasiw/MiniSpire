import random
import numpy as np

from MiniSpire.src.cards import card_library
from MiniSpire.src.config import game_config
from MiniSpire.src.constants import State, Turn
from MiniSpire.src.entities import Targets
from MiniSpire.src.sql_function import load_best_gene, save_best_gene, load_population
from MiniSpire.src.play import Play


class GeneticAlgorithm:
    
    def __init__(self, fitness_function, gene_length, population_size=100, 
                 mutation_rate=0.01, crossover_rate=0.8, elitism=True, max_generations=1000,
                 elimination_rate:float=0, retain_num:int =0, retain_species:int =0):
        self.fitness_function = fitness_function
        self.gene_length = gene_length
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism = elitism
        self.max_generations = max_generations
        self.population = []
        self.elimination_rate = elimination_rate
        self.best_individual = load_best_gene()
        self.best_fitness = 0
        self.retain_num = retain_num
        self.retain_species = retain_species
        self.using_species = [individual.gene for individual in load_population(retain_species)]

    def initialize_population(self):
        self.population = []
        for _ in range(self.retain_num):
            retain_population = load_population(self.retain_species)
            for individual in retain_population:
                self.population.append(individual.gene)
        for _ in range(self.population_size-len(self.population)):
            individual = [random.randint(0, 1) for _ in range(self.gene_length)]
            self.population.append(individual)
    
    def evaluate_fitness(self):
        fitness_values = []
        for individual in self.population:
            fitness = self.fitness_function(individual,self.population)
            fitness_values.append(fitness)
            if individual not in self.using_species:
                if fitness >= self.best_fitness or self.best_individual in self.using_species:
                    self.best_fitness = fitness
                    self.best_individual = individual.copy()
        return fitness_values
    
    def selection(self, fitness_values):
        total_fitness = sum(fitness_values)
        if total_fitness == 0:
            probabilities = [1/self.population_size] * self.population_size
        else:
            probabilities = [f/total_fitness for f in fitness_values]
        selected_indices = np.random.choice(range(self.population_size), 
                                           size=int(self.population_size*(1-self.elimination_rate)),
                                           p=probabilities,
                                           replace= True)
        selected_population = [self.population[i] for i in selected_indices]
        for i in range(self.population_size - len(selected_indices)):
            selected_population.append([random.randint(0, 1) for _ in range(self.gene_length)])
        return selected_population
    
    def crossover(self, selected_population):
        new_population = []
        if self.elitism and self.best_individual:
            new_population.append(self.best_individual.copy())
        while len(new_population) < self.population_size:
            parent1 = random.choice(selected_population)
            parent2 = random.choice(selected_population)
            if random.random() < self.crossover_rate:
                if game_config.CROSSOVER_POS is None:
                    pos = random.randint(1,game_config.GENE_CARD_LENGTH + game_config.GENE_STATE_LENGTH)
                else :
                    pos = game_config.CROSSOVER_POS
                if pos <= game_config.GENE_STATE_LENGTH:
                    pos = pos*game_config.GENE_STATE_NUM
                    point = random.randint(1,game_config.GENE_STATE_LENGTH)
                else:
                    pos = (pos-game_config.GENE_STATE_LENGTH)*game_config.GENE_CARD_NUM*game_config.GENE_STATE_LENGTH +(game_config.GENE_STATE_LENGTH*game_config.GENE_STATE_NUM)
                    point = random.randint(1, game_config.GENE_CARD_NUM * game_config.GENE_STATE_LENGTH)
                child1 = parent1[:pos] + parent2[pos:pos+point] + parent1[pos+point:]
                child2 = parent2[:pos] + parent1[pos:pos+point] + parent2[pos+point:]
                new_population.extend([child1, child2])
            else:
                new_population.extend([parent1, parent2])
        self.population = new_population[:self.population_size]
    
    def mutate(self):
        for i in range(len(self.population)):
            if self.elitism and i == 0 and self.best_individual and self.population[0] == self.best_individual:
                continue
            for j in range(self.gene_length):
                if random.random() < self.mutation_rate:
                    self.population[i][j] = 1 - self.population[i][j]
    
    def run(self):
        self.initialize_population()
        for generation in range(self.max_generations):
            fitness_values = self.evaluate_fitness()
            length = len(str(generation+1))-1
            #if (generation + 1) % (10**length) == 0:
            if (generation + 1) % 5 == 0:
                save_best_gene(self.best_individual,int(self.best_fitness))
            if (generation+1) % 1 == 0:
                for i in range(1):
                    print("##############################################################################################")
                    print(f"Generation {generation + 1}: Best Fitness = {self.best_fitness}")
            selected_population = self.selection(fitness_values)
            self.crossover(selected_population)
            self.mutate()
        self.evaluate_fitness()
        print(f"Final Best Fitness = {self.best_fitness}")
        print(f"Best Individual = {self.best_individual}")
        return self.best_individual, self.best_fitness

def example_fitness_function(individual,population):
    gene = list(map(str, individual))
    score = 0
    count = 0
    for i in range(100):
        enemy_num =random.randint(0,len(population)-1)
        gene1 = list(map(str, population[enemy_num]))
        player = Targets()
        enemy = Targets()
        game = Play(player,enemy)
        game.turn = Turn.AITURN
        for j in range(12):
            game.enemy.cards.append(card_library[j+1])
        game.player.cards = game.enemy.cards
        game.enemy.get_hand_card()
        game.player.get_hand_card()
        error = 0
        while game.state == State.PLAYING:
            game.rounds_training(gene,gene1)
            error += 1
            if error > 5000:
                print("error")
                return 0
        if game.state == State.WON:
            #print("玩家胜利")

            count +=1
        #if game.score != 0:
            #print(game.score)
        if game.score > 4000:
            score += 2000
        elif game.score < -2000:
            score -= 1000
        else:
            score += game.score // 2
    #"""
    if score < 0:
        score = 0
    if score >= 0 :
        print(f"训练结束，胜利次数：{count}，总分数：{score}")
    #"""
    #"""
    if count >=1 and score >= 1:
        score = (score/100) + (count*7)
    else:
        score = (count*3) + (score/1000)
    #"""
    return score

if __name__ == "__main__":
    ga = GeneticAlgorithm(
        fitness_function=example_fitness_function,
        gene_length=game_config.GENE_LENGTH,
        population_size=200,
        mutation_rate=0.05,
        crossover_rate=0.95,
        elitism=False,
        max_generations=100,
        elimination_rate=0.05,
        retain_num=20,
        retain_species =10,
    )
    
    # 运行算法
    best_individual, best_fitness = ga.run()
    save_best_gene(best_individual,int(best_fitness))
    print("\nExample Results:")
    print(f"Best Individual: {best_individual}")
    print(f"Best Fitness: {best_fitness}")
    print(f"Number of 1s: {sum(best_individual)}")
