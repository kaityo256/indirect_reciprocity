import random
from collections import defaultdict


class Player:
    """
    プレイヤークラス
    k: 戦略値。低いほど協力的
    score: 評判。協力行動を取るほど高くなる
    fitness: 適合度(報酬-コスト) 各世代の最後に、この値に比例して子孫を残す
    """

    def __init__(self) -> None:
        self.k = 0         # 戦略値
        self.score = 0     # イメージスコア
        self.fitness = 0.0  # 適合度


def one_step(b, c, players):
    """
    一回の相互作用
    ランダムにDonorとRecipientを選び、協力するかどうかを調べる
    """
    # 無作為にDonorとRecipientを選ぶ
    donor, recipient = random.sample(players, 2)
    # もしRecipientのイメージスコアがDonorの戦略値より大きければDonorは協力する
    if donor.k <= recipient.score:
        # 協力(cooporate)
        # Donorはcだけコストを払う
        donor.fitness -= c
        # Recipientはbだけ報酬を得る
        recipient.fitness += b
        # Donorのイメージスコアを増やす(最大値 5)
        donor.score = min(donor.score + 1, 5)
    else:
        # 非協力(incooporate)
        # Donorのイメージスコアをへらす(最小値 -5)
        donor.score = max(donor.score - 1, -5)
        # fitnessの変更はなし


def one_generation(m, b, c, players):
    """
    1世代分のシミュレーション
    m回の相互作用をさせたあとに、fitness値に比例して子供を作る
    イメージスコアと適合度は世代ごとにクリアする
    """

    for _ in range(m):
        # 無作為に二人選んで協力するか確認
        one_step(b, c, players)

    # 負のfitness値を防ぐため、全体を嵩上げする
    for p in players:
        p.fitness += m * c

    # fitness値に比例して子孫を作る
    fitness_list = {}  # 戦略値kごとのfitnessの合計
    for i in range(-5, 7):
        fitness_list[i] = 0

    for p in players:
        fitness_list[p.k] += p.fitness

    k_list = list(fitness_list.keys())
    f_list = list(fitness_list.values())

    # 次世代の作成
    # イメージスコアと適合度はクリア
    # 戦略値は前世代のそれぞれの戦略値が稼いだ適合度に比例して選ばれる
    for p in players:
        p.score = 0
        p.fitness = 0
        p.k = random.choices(k_list, weights=f_list)[0]


# メイン関数(ここから実行される)
if __name__ == '__main__':
    n = 100  # プレイヤー数
    m = 1000  # 1世代あたりの試行回数
    b = 1.0  # Donorが協力を選んだときにRecipientが得る報酬
    c = 0.1  # Donorが協力を選んだときにDonorが払うコスト

    players = []
    for i in range(n):
        p = Player()
        p.index = i
        p.k = random.randint(-5, 6)  # 最初の世代の戦略値kはランダムに決める
        players.append(p)

    # 200世代ほどシミュレーションする
    for _ in range(200):
        one_generation(m, b, c, players)

    # 最終状態での戦略値kごとのpopulaton
    k_p = defaultdict(int)
    for p in players:
        k_p[p.k] += 1

    for i in range(-5, 7):
        print(i, k_p[i])
