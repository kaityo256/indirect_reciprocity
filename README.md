# 協調行動のシミュレーション

## 概要

以下の論文で提案された間接互恵行動のシミュレーションを実装。

Martin A. Nowak and Karl Sigmund, "Evolution of indirect reciprocity by image scoring", Nature vol. 393, pp. 573–577 (1998)

## アルゴリズム

* n人のプレイヤーを用意
* 各プレイヤーは、戦略値`k`とイメージスコア`score`、適合度`fitness`を持つ
* 各世代において、m回のDonorとRecipientが選ばれる
* DonorはRecipientのイメージスコア`score`を見て、自分の戦略値`k`よりも高ければ協力する、そうでなければ協力しない
    * Donorが協力を選んだ場合
        * Donorはコスト`c`を支払い、Recipientは報酬`b`を得る(それぞれの適合度が、`-c`、`+b`される)
        * Donorのイメージスコアが+1される(最大5)
    * Donorが非協力を選んだ場合
        * Donorのイメージスコアが-1される(最小-5)
        * それぞれの適合度は変化なし
* m回の相互作用の後、各プレイヤーは適合度に比例して子供を残す
* 子供は親から戦略値`k`は引き継ぐが、イメージスコアと適合度は引き継がない(クリアされる)
