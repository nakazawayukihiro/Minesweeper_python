# Minesweeper python
import random

MS_SIZE = 8          # ゲーム盤のサイズ
CLOSE, OPEN, FLAG = 0, 1, 2

class Game:

    def __init__(self, number_of_mines = 10):
        """ ゲーム盤の初期化
        Arguments:
        number_of_mines -- 地雷の数のデフォルト値は10

        Side effects:
        mine_map[][] -- 地雷マップ(-1: 地雷，>=0 8近傍の地雷数)
        game_board[][] -- 盤面 (0: CLOSE(初期状態), 1: 開いた状態, 2: フラグ)

        """
        self.init_game_board()
        self.init_mine_map(number_of_mines)
        self.count_mines()

    def init_game_board(self):
        """ ゲーム盤を初期化 """
        self.game_board = [[CLOSE] * MS_SIZE for _ in range(MS_SIZE)]

    def init_mine_map(self, number_of_mines):
        """ 地雷マップ(self->mine_map)の初期化
        Arguments:
        number_of_mines -- 地雷の数
        
        地雷セルに-1を設定する．      
        """
        mine_num = 0
        self.mine_map = [[0] * MS_SIZE for _ in range(MS_SIZE)]
        
        while mine_num < number_of_mines and mine_num < MS_SIZE * MS_SIZE:
            x = random.randint(0, MS_SIZE-1)
            y = random.randint(0, MS_SIZE-1)

            if self.mine_map[y][x] != -1:
                self.mine_map[y][x] = -1
                mine_num += 1

    def count_mines(self):
        """ 8近傍の地雷数をカウントしmine_mapに格納 
        地雷数をmine_map[][]に設定する．
        """
        for y in range(MS_SIZE):
            for x in range(MS_SIZE):

                # そのマスが地雷の場合は何もしない
                if self.mine_map[y][x] == -1:
                    continue

                # 隣接する８方向のマスの地雷の数をカウント
                mine_sum = 0

                # 方向を決める２重ループ
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i != 0 or j != 0:
                            # その方向に地雷があるかチェック
                            is_mine = self.is_mine(y + i, x + j)

                            if is_mine:
                                # 地雷があればカウントアップ
                                mine_sum += 1

                # 周りの地雷の数をセット
                self.mine_map[y][x] = mine_sum
    
    def is_mine(self, y, x):

        # ボード内の座標かチェック
        if x >= 0 and y >= 0 and x < MS_SIZE  and y < MS_SIZE:

            # その座標に地雷があるかどうかをチェック
            if self.mine_map[y][x] == -1:

                # そのマスが地雷の場合はTrueを返却
                return True

        # ボード外 or 地雷でない場合はFalseを返却
        return False
    
    def open_cell(self, x, y):
        """ セル(x, y)を開ける
        Arguments:
        x, y -- セルの位置
        
        Returns:
          True  -- 8近傍セルをOPENに設定．
                   ただし，既に開いているセルの近傍セルは開けない．
                   地雷セル，FLAGが設定されたセルは開けない．
          False -- 地雷があるセルを開けてしまった場合（ゲームオーバ）
        """
        if self.board_range(y, x) == False: # 選択したセルが範囲外
            return True

        if self.mine_map[y][x] != FLAG and self.mine_map[y][x] == -1: # 選択したセルがフラグ、もしくは地雷
            return False

        elif self.game_board[y][x] != CLOSE: # 選択したセルが開いていない
            return True

        else: # 近傍8マスに対して
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if self.board_range(y + i, x + j):
                        if  self.mine_map[y + i][x + j] == -1 or self.game_board[y + i][x + j] == FLAG: # セルがフラグ、もしくは地雷
                            continue
                        elif self.game_board[y + i][x + j] == CLOSE: # セルが開いていない
                            self.game_board[y + i][x + j] = OPEN
        return True
    
    def board_range(self, y, x):
        """選択したセルがボード内にあるか
        Arguments:
        x, y -- セルの位置

        Returns:
          True  -- 選択したセルがボード内に存在する
          False -- 選択したセルがボード内に存在しない
        """
        if x >= 0 and y >= 0 and x < MS_SIZE and y < MS_SIZE:
            return True
        
        else:
            return False

    def flag_cell(self, x, y):
        """
        セル(x, y)にフラグを設定する，既に設定されている場合はCLOSE状態にする
        """
        if self.game_board[y][x] == FLAG: # 既にフラグが設定
            self.game_board[y][x] = CLOSE

        elif self.game_board[y][x] == OPEN: # セルがOPEN状態
            pass

        else: 
            self.game_board[y][x] = FLAG

            
    def is_finished(self):
        """ 地雷セル以外のすべてのセルが開かれたかチェック 
        Arguments:
        not_mine_sum = 地雷セル以外のセルの数

        Returns:
          True  -- 地雷セル以外の全てのセルが開いた
          False -- 地雷セル以外で、開かれていないセルが存在
        """
        not_mine_sum = 0
        for i in range(MS_SIZE):
            for j in range(MS_SIZE):
                if self.mine_map[i][j] == -1: # 地雷セルをカウント
                    not_mine_sum += 1
                elif self.game_board[i][j] == OPEN: # OPEN状態のセルをカウント
                    not_mine_sum += 1
        
        if not_mine_sum == MS_SIZE * MS_SIZE: 
            return True

        return False

    ### ★ 以降は表示に関するコード ###
    
    def print_header(self):
        print("=====================================")
        print("===  MineSweeper Python Ver. 1  =====")
        print("=====================================")

    def print_footer(self):
        print("   ", end="")
        for x in range(MS_SIZE):
            print("---", end="")
        print("[x]\n   ", end="")
        for x in range(MS_SIZE):
            print(f"{x:3d}", end="")
        print("")
        
    def print_mine_map(self):
        print(" [y]")
        for y in range(MS_SIZE):
            print(f"{y:2d}|", end="")
            for x in range(MS_SIZE):
                print(f"{self.mine_map[y][x]:2d}", end="")
            print("")
        
    def print_game_board(self):
        marks = ['x', ' ', 'P']
        self.print_header()
        print("[y]")
        for y in range(MS_SIZE):
            print(f"{y:2d}|", end="")
            for x in range(MS_SIZE):
                if self.game_board[y][x] == OPEN and self.mine_map[y][x] > 0:
                    print(f"{self.mine_map[y][x]:3d}", end="")
                else:
                    print(f"{marks[self.game_board[y][x]]:>3}", end="")
            print("")
        self.print_footer()

if __name__ == '__main__':
    b = Game()
    quitGame = False
    while not quitGame:
        b.print_game_board()
        print("o x y: セルを開く，f x y: フラグ設定/解除, q: 終了 -->", end="")
        command_str = input()

        try:
            cmd = command_str.split(" ")
            if cmd[0] == 'o':
                x, y = cmd[1:]
                if b.open_cell(int(x), int(y)) == False:
                    print("ゲームオーバー!")
                    quitGame = True
            elif cmd[0] == 'f':
                x, y = cmd[1:]
                b.flag_cell(int(x), int(y))
            elif cmd[0] == 'q':
                print("ゲームを終了します．")
                quitGame = True
                break
            else:
                print("コマンドはo, f, qのいずれかを指定してください．")
        except:
            print("もう一度，コマンドを入力してください．")
            
        if b.is_finished():
            b.print_game_board()
            print("ゲームクリア!")
            quitGame = True

            
