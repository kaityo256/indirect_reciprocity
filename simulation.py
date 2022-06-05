import random
from collections import defaultdict

class Player:
    def __init__(self) -> None:
        self.k = 0         # 戦略値
        self.score = 0     # イメージスコア
        self.fitness = 0.0 # 適合度

def one_step(b,c,players):
    # 無作為にDonerとRecipientを選ぶ
    donor, recipient = random.sample(players, 2)
    # もしRecipientのイメージスコアがDonorの戦略値より大きければDonorは協力する
    if donor.k <= recipient.score:
        # Donorはcだけコストを払う
        donor.fitness -= c
        # Recipientはbだけ報酬を得る
        recipient.fitness += b
        # Donorのイメージスコアを増やす(最大値 5)
        donor.score = min(donor.score+1, 5)
    else:
        # Donorのイメージスコアをへらす(最小値 -5)
        donor.score = max(donor.score-1, -5)
        # fitnessの変更はなし

def one_generation(players):
    m = 125 # 1世代あたりの試行回数
    b = 1.0 # Donorが協力を選んだときにRecipientが得る報酬
    c = 0.1 # Donorが協力を選んだときにDonorが払うコスト
    for _ in range(m):
        # 無作為に二人選んで協力するか確認
        one_step(b,c, players)
    # 負のfitness値を防ぐため、全体を嵩上げする
    for p in players:
        p.fitness += m * c

    # fitness値に比例して子孫を作る
    n = len(players) # 人数
    total_fitness = 0.0
    fitness_list = {}
    for i in range(-5,7):
        fitness_list[i] = 0

    for p in players:
        total_fitness += p.fitness
        fitness_list[p.k] += p.fitness

    for i in range(-5,7):
        fitness_list[i] = round(fitness_list[i]/total_fitness * n)

    # 切り捨てによる誤差を修正 (足りない分は最大勢力に割り振る)
    max_k = max(fitness_list, key=fitness_list.get)
    n_sum = sum(fitness_list.values())
    print(n_sum)
    fitness_list[max_k] += (n-n_sum)
 
    # 次の世代の戦略値のリストを作る
    nextgeneration_klist = []
    for k,v in fitness_list.items():
        nextgeneration_klist += [k]*v

    # 次世代のプレイヤーを作る
    for i in range(n):
        players[i].score = 0
        players[i].fitness = 0.0
        players[i].k = nextgeneration_klist[i]

    for k,v in fitness_list.items():
        print(k,v)

if __name__ == '__main__':
    n = 100 # プレイヤー数
    random.seed(4)
    players = []
    for _ in range(n):
        p = Player()
        p.k = random.randint(-5,6) # 最初の世代の戦略値kはランダムに決める
        players.append(p)
    for _ in range(100):
        print("------------")
        one_generation(players)