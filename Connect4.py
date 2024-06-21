import random

TATE = 6
YOKO = 7

def show_connect4_board(board: list):
    """
    ゲーム盤を表示する関数
    引数 board: 盤面を保存した2次元リスト
    """
    for row in board:
        print("---------------")
        for col in row:
            print("|", end="")
            if col == 0:
                print(" ", end="")
            elif col == 1:
                print("1", end="")
            elif col == 2:
                print("2", end="")
            else:
                print("E", end="")
        print("|")
    print("---------------")
    for i in range(1, YOKO+1):
        print(f" {i}", end="")
    print()

def draw_connect4_board(board, f):
    """
    ファイルに盤面を書き出すための関数
    引数1 board: 盤面を保存した2次元リスト
    引数2 f: ファイルオブジェクト
    """
    for row in board:
        print("---------------", file=f)
        for col in row:
            print("|", end="", file=f)
            if col == 0:
                print(" ", end="", file=f)
            elif col == 1:
                print("1", end="", file=f)
            elif col == 2:
                print("2", end="", file=f)
            else:
                print("E", end="", file=f)
        print("|", file=f)
    print("---------------", file=f)
    for i in range(1, YOKO+1):
        print(f" {i}", end="", file=f)
    print(file=f)

def get_next_move(board: list):
    """
    手を入力する関数
    引数 board: 盤面を保存した2次元リスト
    戻り値 座標[row, col]
    """
    col = 0
    while True:
        try:
            col = int(input("列を入力します(1~7): "))
        except ValueError:
            print("1~7の数字を入力してください")
            continue
        # 空きマス確認
        if 1 <= col <= YOKO:
            col -= 1
            row = check_lower(board, col)
            if row == -1:
                print("そのマスはすでに埋まっています")
            else:
                break
    return [row, col]
        
def check_lower(board: list, col: int):
    """
    列の一番下の空きマスの座標を取得する関数
    引数1 board: 盤面を保存した2次元リスト
    引数2 col: 調べる列番号
    戻り値 空きマスがあるときrow, 空きマスがないとき-1
    """
    for row in range(TATE-1, -2, -1):
        if board[row][col] == 0:
            return row
    else:
        return -1
    
def check_winner(board: list, num: int):
    """
    勝利条件を確認する関数
    引数1 board: 盤面を保存した2次元リスト
    引数2 num: プレイヤーナンバー(先手1, 後手2)
    戻り値 True(勝利条件を満たした)/False(勝利条件を満たしていない)
    """
    # ヨコ
    for row in range(TATE):
        line = []
        for i in range(YOKO-3):
            line = board[row][i:i+4] 
            if line[0]==line[1]==line[2]==line[3]==num:
                return True
    # タテ
    for col in range(YOKO):
        line = []
        for row in range(TATE):
            line.append(board[row][col])
        for i in range(TATE-3):
            l = line[i:i+4]
            if l[0]==l[1]==l[2]==l[3]==num:
                return True
        
    # ナナメ(左上から右下方向)
    for row in range(TATE-3):    
        for col in range(YOKO-3):
            line = []
            for i in range(4):
                line.append(board[row+i][col+i])
            if line[0]==line[1]==line[2]==line[3]==num:
                return True
    
    # ナナメ(右上から左下方向)
    for row in range(TATE-3):
        for col in range(YOKO, 3, -1):
            line = []
            for i in range(4):
                line.append(board[row+i][col-i-1])
            if line[0]==line[1]==line[2]==line[3]==num:
                return True
    # 条件を満たさない場合
    return False

def get_brank(board:list):
    """
    各列の空いている1番下の座標をリストで返す関数
    引数 board: 盤面を保存した2次元リスト
    戻り値 brank: 空きマスのリスト[[row,col],[],]
    """
    brank = []
    for col in range(YOKO):
        row = check_lower(board, col)
        if row != -1:
            brank.append([row,col])
    return brank

def random_choice(board: list):
    """
    ランダムでマスを選択する関数
    引数 board: 盤面を保存した2次元リスト
    """
    brank = get_brank(board)
    return random.choice(brank)

def deep_copy(lst: list) -> list:
    """
    リストの深いコピーを作成する関数
    引数 lst: コピーしたいリスト
    戻り値 copied: コピーしたリスト
    """
    copied = []
    for row in lst:
        tmp = []
        for r in row:
            tmp.append(r)
        copied.append(tmp)
    return copied

class SearchMinMax():
    """
    MinMax探索に関するクラス
    第6回で追加
    """
    def __init__(self, thr=20, sec=10):
        """
        初期化関数
        引数1 thr: 3連結したときのスコア 初期値20
        引数2 sec: 2連結したときのスコア 初期値10
        """
        self.infinite = 30000
        self.win = 20000
        self.max_depth = 5
        self.best_move = None
        self.score = None
        self.thr = thr
        self.sec = sec
        self.notchain = 0

    def get_nextmove(self, board, No_pl):
        self.score, self.best_move = self.decide_minmax_ai_move(board, No_pl, No_pl)
        return self.score, self.best_move

    def decide_minmax_ai_move(self, board, decidePL, currentPL, depth=0):
        """
        Min-max探索
        MinPLは自分から見て相手。評価点は最低を選ぶ。
        MaxPLは自分の手。評価点は最高を選ぶ。
        引数1 board: 盤面を保存した2次元リスト
        引数2 decidePL: max探索/min探索を保存する
        引数3 currentPL: 現在の手番プレイヤー(先手1/後手0)
        引数4 depth: 探索の深さ(初期値0)
        戻り値1 score: 評価点
        戻り値2 best: 次手の座標[row, col]
        """
        # 深度が最大なら評価関数
        if depth == self.max_depth:
            if decidePL == 0:
                calcPL = 2
            else:
                calcPL = 1
            return self.calc_evalute(board, calcPL), None

        # score初期値設定
        if decidePL == currentPL:
            score = -self.infinite # MaxPLのとき、scoreを最低値に
        else:
            score = self.infinite # MinPLのとき、scoreを最高値に
        
        # print(f"深さ: {depth}")
        best_move = None
        setflag = True
        brank = get_brank(board)
        for next_move in brank:
            board[next_move[0]][next_move[1]] = decidePL+1
            if check_winner(board, decidePL+1):
                board[next_move[0]][next_move[1]] = 0
                if decidePL == currentPL:
                    score = self.win
                    best_move = next_move
                else:
                    score = -self.win
                    best_move = next_move
                return score, best_move
            else:
                new_score, _ = self.decide_minmax_ai_move(board, (decidePL+1)%2, currentPL, depth+1)
            
                board[next_move[0]][next_move[1]] = 0
                if depth == 0 and score == new_score:
                    setflag = random.choice([True, False])
                if setflag:
                    # decidePL==currentPL -> 自分の手番
                    # decidePL!=currentPL -> 相手の手番
                    if decidePL == currentPL and new_score >= score:
                        score = new_score
                        best_move = next_move
                    elif decidePL != currentPL and new_score <= score:
                        score = new_score
                        best_move = next_move

        else:
            if len(brank) == 0:
                return 0, None # 引き分け(0)
            if best_move is None:
                best_move = brank[0]
            return score, best_move

    def calc_evalute(self, board, num):
        """
        評価関数にわたすlineを作り、評価関数を呼び出す関数
        引数1 board: 盤面を保存した2次元リスト
        引数2 num: (MinMax探索から見て) 自分->1, 相手->2
        戻り値 score: 2連結で10, 3連結で20, 何もないなら0
        """
        self.num = num
        exist = [] # コマがある座標のリスト
        for row in range(TATE):
            for col in range(YOKO):
                if board[row][col] != 0:
                    exist.append([row, col])

        sum_score = 0
        for place in exist:
            # ヨコ
            line = []
            for i in range(-2, 3):
                try:
                    if place[1]+i < 0:
                        line.append(0)
                    else:
                        line.append(board[place[0]][place[1]+i])
                except IndexError:
                    line.append(0)
            # 両隣が空きマスなら次のplaceへ
            if line[1] == line[3] == 0: 
                continue
            sum_score += self.check_chain(line)
            
            # タテ
            line = []
            for i in range(-2, 3):
                try:
                    if place[0]+i < 0:
                        line.append(0)
                    else:
                        line.append(board[place[0]+i][place[1]])
                except IndexError:
                    line.append(0)
            # 両隣判定
            if line[1] == line[3] == 0:
                continue
            sum_score += self.check_chain(line)
            
            # ナナメ1(左上->右下)
            line = []
            for i in range(-2, 3):
                try:
                    if place[0]+i < 0 or place[1]+i < 0:
                        line.append(0)
                    else:
                        line.append(board[place[0]+i][place[1]+i])
                except IndexError:
                    line.append(0)
            #両隣判定
            if line[1] == line[3] == 0:
                continue
            sum_score += self.check_chain(line)
            
            # ナナメ2(右上->左下)
            line = []
            for i in range(2, -3, -1):
                try:
                    if place[0]+i < 0 or place[1]-i < 0:
                        line.append(0)
                    else:
                        line.append(board[place[0]+i][place[1]-i])
                except IndexError:
                    line.append(0)
            # 両隣判定
            if line[1] == line[3] == 0:
                continue
            sum_score += self.check_chain(line)
        return sum_score


    def check_chain(self, line: list) -> int:
        """
        引数のlineに、同じコマが連結しているか判定する関数
        self.thr, self.secを参照する
        戻り値: 3連結でself.thr, 2連結でself.sec
        """
        if line[2] != 0:
            # 3連結
            if line[1] == line[2] == line[3] and \
                (line[0] == 0 or line[4] == 0):
                if line[2] == self.num: # 先手(自分)なら正のスコアを返す
                    return self.thr
                else: # 後手(相手)なら負のスコアを返す
                    return -self.thr
                
            # 2連結(左と真ん中)
            elif line[1] == line[2] and (line[0] == 0 or line[3] == 0):
                if line[2] == self.num: # 先手(自分)なら正のスコアを返す
                    return self.sec
                else: # 後手(相手)なら負のスコアを返す
                    return -self.sec
                
            # 2連結(真ん中と右)
            elif line[2] == line[3] and (line[1] == 0 or line[4] == 0):
                if line[2] == self.num: # 先手(自分)なら正のスコアを返す
                    return self.sec
                else: # 後手(相手)なら負のスコアを返す
                    return -self.sec
            else:
                return self.notchain
        else:
            return self.notchain

def humanVShuman():
    """
    人間vs人間
    """
    # board初期化
    board = [[0 for i in range(YOKO)] for j in range(TATE)]
    cnt = 0
    while True:
        is_full_board = True
        show_connect4_board(board)
        # ユーザーの入力
        print(fr"{['先手', '後手'][cnt%2]}の番")
        move = get_next_move(board)
        board[move[0]][move[1]] = cnt%2 + 1

        # 終了チェック
        if check_winner(board, cnt%2+1):
            show_connect4_board(board)
            print(fr"{['先手', '後手'][cnt%2]}の勝利！")
            break

        for row in board:
            for x in row:
                if x == 0:
                    is_full_board = False

        if is_full_board:
            show_connect4_board(board)
            print("引き分け")
            break
        
        cnt += 1

def minmaxVSrandom(name: list, switch=0):
    """
    minmax VS random
    引数1 name: AIの名前のリスト[先手, 後手]
    引数2 switch: 0->Minmaxが先手 / 1->Minmaxが後手
    戻り値 引き分け->3, 先手勝利->0, 後手勝利->1
    """
    # board初期化
    board = [[0 for i in range(YOKO)] for j in range(TATE)]
    minmaxAI = SearchMinMax()
    cnt = 0
    while True:
        is_full_board = True
        show_connect4_board(board)
        # ユーザーの入力
        print(fr"{['先手', '後手'][cnt%2]}の番")
        if cnt%2 == switch:
            move = random_choice(board)
            # move = get_next_move(board)
        else:
            score, move = minmaxAI.get_nextmove(board, cnt%2, cnt%2)
            print(f"スコア: {score}")
        board[move[0]][move[1]] = cnt%2 + 1

        # 終了チェック
        if check_winner(board, cnt%2+1):
            show_connect4_board(board)
            print(fr"{['先手', '後手'][cnt%2]},{name[cnt%2]}の勝利！")
            return cnt%2

        for row in board:
            for x in row:
                if x == 0:
                    is_full_board = False

        if is_full_board:
            show_connect4_board(board)
            print("引き分け")
            return 3
        
        cnt += 1

def test_minmaxVSrandom(num):
    """
    Minmax探索とランダムAIの性能試験
    引数 num: 先手後手、それぞれの試行回数
    """
    min_win = 0
    rand_win = 0
    draw = 0
    for i in range(num):
        print(f"{i+1}回目のゲーム開始...")

        win = minmaxVSrandom(["Min-maxAI", "ランダムAI"])
        if win == 3:
            draw += 1
            print("引き分け")
        elif win == 0:
            min_win += 1
            print("Min-maxの勝利")
        elif win == 1:
            rand_win += 1
            print("ランダムAIの勝利")
        else:
            print("ERROR!!")
            return
        print(f"Min-max : Random - {min_win} : {rand_win}")
        print(f"引き分け: {draw}")
    
    print("-----------","先手後手交代","----------",sep="\n")

    for i in range(num):
        print(f"{i+num+1}回目のゲーム開始...")

        win = minmaxVSrandom(["ランダムAI", "Min-maxAI"], 1)
        if win == 3:
            draw += 1
            print("引き分け")
        elif win == 0:
            rand_win += 1
            print("ランダムAIの勝利")
        elif win == 1:
            min_win += 1
            print("Min-maxの勝利")
        print(f"Min-max : Random - {min_win} : {rand_win}")
        print(f"引き分け: {draw}")

def minmaxVSminmax():
    """
    Min-max探索 VS Min-max探索
    """
    # board初期化
    board = [[0 for i in range(YOKO)] for j in range(TATE)]
    sente_minmaxAI = SearchMinMax()
    gote_minmaxAI = SearchMinMax()
    cnt = 0
    while True:
        is_full_board = True
        show_connect4_board(board)
        # 入力
        print(f"{cnt+1}手目:{['先手', '後手'][cnt%2]}の番")
        if cnt%2 == 0:
            score, move = sente_minmaxAI.get_nextmove(board, cnt%2)
        else:
            score, move = gote_minmaxAI.get_nextmove(board, cnt%2)
        print(f"スコア: {score}")
        board[move[0]][move[1]] = cnt%2 + 1

        # 終了チェック
        if check_winner(board, cnt%2+1):
            show_connect4_board(board)
            print(fr"{['先手', '後手'][cnt%2]}の勝利！")
            return cnt%2

        for row in board:
            for x in row:
                if x == 0:
                    is_full_board = False

        if is_full_board:
            show_connect4_board(board)
            print("引き分け")
            return 3
        
        cnt += 1
    
def bestVStest_minmax():
    """
    最適param VS テストparam
    """
    # board初期化
    board = [[0 for i in range(YOKO)] for j in range(TATE)]
    sente_minmaxAI = SearchMinMax()
    gote_minmaxAI = SearchMinMax(10, 20)
    cnt = 0
    while True:
        is_full_board = True
        show_connect4_board(board)
        # 入力
        print(f"{cnt+1}手目:{['先手', '後手'][cnt%2]}の番")
        if cnt%2 == 0:
            score, move = sente_minmaxAI.get_nextmove(board, cnt%2)
        else:
            score, move = gote_minmaxAI.get_nextmove(board, cnt%2)
        print(f"スコア: {score}")
        board[move[0]][move[1]] = cnt%2 + 1

        # 終了チェック
        if check_winner(board, cnt%2+1):
            show_connect4_board(board)
            print(fr"{['先手', '後手'][cnt%2]}の勝利！")
            return cnt%2

        for row in board:
            for x in row:
                if x == 0:
                    is_full_board = False

        if is_full_board:
            show_connect4_board(board)
            print("引き分け")
            return 3
        
        cnt += 1

def file_bestVStest_minmax(f):
    """
    ファイル出力用 best VS test
    引数 f: 書き出し用ファイルオブジェクト(txt)
    戻り値: 引き分け(3), 先手勝利(0), 後手勝利(1)
    """
    # board初期化
    board = [[0 for i in range(YOKO)] for j in range(TATE)]
    sente_minmaxAI = SearchMinMax()
    gote_minmaxAI = SearchMinMax(10, 20)
    cnt = 0
    while True:
        is_full_board = True
        draw_connect4_board(board, f)
        # 入力
        print(f"{cnt+1}手目:{['先手', '後手'][cnt%2]}の番", file=f)
        if cnt%2 == 0:
            score, move = sente_minmaxAI.get_nextmove(board, cnt%2)
        else:
            score, move = gote_minmaxAI.get_nextmove(board, cnt%2)
        print(f"スコア: {score}", file=f)
        board[move[0]][move[1]] = cnt%2 + 1

        # 終了チェック
        if check_winner(board, cnt%2+1):
            draw_connect4_board(board, f)
            print(fr"{['先手', '後手'][cnt%2]}の勝利！", file=f)
            return cnt%2

        for row in board:
            for x in row:
                if x == 0:
                    is_full_board = False

        if is_full_board:
            draw_connect4_board(board, f)
            print("引き分け", file=f)
            return 3
        
        cnt += 1

def test_bestVStest_minmax():
    f = open("Connect4SelfPlayData.txt", "w")
    sente_win = 0
    gote_win = 0
    draw = 0
    for i in range(100):
        print(f"{i+1}回目のゲーム開始...")
        print(f"{i+1}回目のゲーム開始...", file=f)
        win = file_bestVStest_minmax(f)
        print("ゲームオーバー: ", end="")
        print("ゲームオーバー: ", end="", file=f)
        if win == 0:
            sente_win += 1
            print("Bestの勝利")
            print("Bestの勝利", file=f)
        elif win == 1:
            gote_win += 1
            print("Testの勝利")
            print("Testの勝利", file=f)
        elif win == 3:
            draw += 1
            print("引き分け")
            print("引き分け", file=f)
        print(f"Best AI - Test AI : {sente_win} - {gote_win} (引き分け: {draw})")
        print(f"Best AI - Test AI : {sente_win} - {gote_win} (引き分け: {draw})", file=f)
    f.close()


if __name__ == "__main__":
    # humanVShuman()
    # minmaxVSrandom(["Min-maxAI", "ランダムAI"]) # Minmaxが先手
    # minmaxVSrandom(["ランダムAI", "Min-maxAI"], 1) # Minmaxが後手
    # minmaxVSminmax()
    # bestVStest_minmax()
    test_bestVStest_minmax()