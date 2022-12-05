# -*- coding: utf-8 -*-

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
        # 現在、タイプはここで決めている
        #self.type = "image_scoring"
        self.type = "standing"

    def play_image_scoring(self, recipient, b, c):
        """
        Image Scoring 戦略
        """
        # もしRecipientのイメージスコアがDonorの戦略値より大きければDonorは協力する
        if self.k <= recipient.score:
            # 協力(cooporate)
            # Donorはcだけコストを払う
            self.fitness -= c
            # Recipientはbだけ報酬を得る
            recipient.fitness += b
            # Donorのイメージスコアを増やす(最大値 5)
            self.score = min(self.score + 1, 5)
        else:
            # 非協力(incooporate)
            # Donorのイメージスコアをへらす(最小値 -5)
            self.score = max(self.score - 1, -5)
            # fitnessの変更はなし

    def play_standing(self, recipient, b, c):
        """
        Standing 戦略
        """
        # もしRecipientのイメージスコアがDonorの戦略値より大きければDonorは協力する
        if self.k <= recipient.score:
            # 協力(cooporate)
            # Donorはcだけコストを払う
            self.fitness -= c
            # Recipientはbだけ報酬を得る
            recipient.fitness += b
            # Donorのイメージスコアを増やす(最大値 5)
            self.score = min(self.score + 1, 5)
        else:
            # 非協力(incooporate)
            # Recipientのイメージスコアが0以上の時に限り、Donorのイメージスコアをへらす(最小値 -5)
            if recipient.score >= 0:
                self.score = max(self.score - 1, -5)
            # fitnessの変更はなし

    def play(self, recipient, b, c):
        """
        Donorの行動
        自分のタイプにより、行動を変える
        """
        if self.type == "image_scoring":
            self.play_image_scoring(recipient, b, c)
        elif self.type == "standing":
            self.play_standing(recipient, b, c)
        else:
            # 未定義のタイプが指定されたらエラー
            raise ValueError("Error: Undefinined type of player")


def one_step(b, c, players):
    """
    1ステップ
    ドナーとレシピエントを選んで、ドナーに行動させる
    この例ではネットワーク構造なし(全員からランダムに二人選ぶ)
    """
    donor, recipient = random.sample(players, 2)
    donor.play(recipient, b, c)


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


def main():
    n = 100  # プレイヤー数
    m = 125  # 1世代あたりの試行回数
    b = 1.0  # Donorが協力を選んだときにRecipientが得る報酬
    c = 0.1  # Donorが協力を選んだときにDonorが払うコスト

    players = []
    for i in range(n):
        p = Player()
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


main()
