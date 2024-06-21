# Connect4
## 実行環境の必要条件
* python >= 3.10

## プロジェクト概要
Connect4とは
* 7x6マスの盤面に同じ色のコマをタテ・ヨコ・ナナメに4つそろえるゲーム
* 実際のボードゲームでは盤を直立させて遊ぶ
* コマは盤の上から落とす方法でしかできないため、1手目に最上段に置くなどはできない
* プレイヤーは「どの列にコマを落とすか」を決めることができる
* 日本では四目並べとも呼ばれている
* 参照: https://ja.wikipedia.org/wiki/四目並べ

ルールベースAI同士の対戦で、どのパラメータが対戦成績に影響を及ぼすか検証するために、プロジェクトを作成した。

## 検証したパラメータ
手番のプレイヤーがどれくらい勝ちに近づいているかを表すスコアを盤面スコアとする。
この盤面スコアは以下のように決定される。
* 現在の盤面から5手先の盤面で決定される
* 同じ色のコマが2つか3つ連続しておいてあるとき、スコアが変動する
* 自分の色ならスコアが増加し、相手の色ならスコアが減少する  

この増減するスコアの値を変更することで、盤面における重要度は、2つ連続したものと3つ連続したものでは、どちらがより影響するのかについて検証した。

