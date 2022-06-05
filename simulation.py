import random

class Player:
    def __init__(self) -> None:
        self.k = 0         # 戦略値
        self.score = 0     # イメージスコア
        self.fitness = 0.0 # 適合度

def one_step(b,c,players):
    # 無作為にDonerとRecipientを選ぶ
    donor, recipient = random.sample(players, 2)
    # Donorの戦略値がRecipientのイメージスコアよりも高ければ協力しない
    if donor.k > recipient.score:
        # Donorのイメージスコアをへらす(最小値 -5)
        donor.k = max(donor.k-1, -5)
        # fitnessの変更はなし
    else:
        # Donorはcだけコストを払う
        donor.fitness -= c
        # Recipientはbだけ報酬を得る
        recipient.fitness += b
        # Donorのイメージスコアを増やす(最大値 5)
        donor.k = min(donor.k+1, 5)

def one_generation(players):
    m = 125 # 1世代あたりの試行回数
    b = 1.0 # Donorが協力を選んだときにRecipientが得る報酬
    c = 0.1 # Donorが協力を選んだときにDonoerが払うコスト
    for _ in range(m):
        # 無作為に二人選んで協力するか確認
        one_step(b,c, players)
    # 負のfitness値を防ぐため、全体を嵩上げする
    for p in players:
        p.fitness += m * c
        print(p.fitness)
    # TODO:fitness値に比例して子孫を作る

if __name__ == '__main__':
    n = 100 # プレイヤー数
    players = []
    for _ in range(n):
        p = Player()
        p.k = random.randint(-5,6) # 最初の世代の戦略値kはランダムに決める
        players.append(p)
    
    one_generation(players)