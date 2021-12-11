# Minesweeper GUI                 
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import random

MS_SIZE = 8         # ゲーム盤のサイズ
CLOSE, OPEN, FLAG = 0, 1, 2

# Minesweeper.pyのクラスGameをコピー
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

class MyPushButton(QPushButton):
    
    def __init__(self, text, x, y, parent):
        """ セルに対応するボタンを生成 """
        super(MyPushButton, self).__init__(text, parent)
        self.parent = parent
        self.x = x
        self.y = y
        self.setMinimumSize(25, 25)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, 
            QSizePolicy.MinimumExpanding)
        
    def set_bg_color(self, colorname):
        """ セルの色を指定する
        Arguments:
            self
            colorname: 文字列 -- 色名 (例, "white")
        """
        self.setStyleSheet("MyPushButton{{background-color: {}}}".format(colorname))
        
    def on_click(self):
        """ セルをクリックしたときの動作 """
        
        modifiers = QApplication.keyboardModifiers()
        
        if modifiers == Qt.ShiftModifier: # SHIFTが押された
            self.parent.game.flag_cell(self.x, self.y)
        else:
            #地雷セルをクリック フラグ無し -> Game Over
            if self.parent.game.game_board[self.y][self.x] != FLAG and self.parent.game.mine_map[self.y][self.x] == -1:
                self.parent.ans_of_minemap() # 正解を表示
                if QMessageBox.information(self, "Game Over", "ゲームオーバー！") == QMessageBox.Ok:
                    self.parent.close() # アプリを閉じる

            self.parent.game.open_cell(self.x, self.y) # セルを開く

        # セルの状態を表示
        self.parent.show_cell_status()

        # 終了しているか確認
        if self.parent.game.is_finished():
            self.parent.ans_of_minemap() #正解を表示
            if QMessageBox.information(self, "Game Clear", "ゲームクリア！") == QMessageBox.Ok:
                self.parent.close()

class MinesweeperWindow(QMainWindow):
    
    def __init__(self):
        """ インスタンスが生成されたときに呼び出されるメソッド """
        super(MinesweeperWindow, self).__init__()
        self.game = Game()
        self.initUI()
    
    def initUI(self):
        """ UIの初期化 """        
        self.resize(100, 100) 
        self.setWindowTitle('Minesweeper')
        
        # ステータスバーに”Shift+クリックでフラグをセット”と表示
        sb = self.statusBar()
        sb.showMessage("Shift+クリックでフラグをセット")

        # MyPushButtonクラスのインスタンスbuttonを8*8生成
        self.button = [[0] * MS_SIZE for _ in range(MS_SIZE)]
        for x in range(0, MS_SIZE):
            for y in range(0, MS_SIZE):
                self.button[y][x] = MyPushButton(' ', x, y, self)
                self.button[y][x].set_bg_color('gray')
                self.button[y][x].clicked.connect(self.button[y][x].on_click)    
                self.button[y][x].setIcon(QIcon('close.png'))  

        # 8列
        hbox = [0] * MS_SIZE
        for i in range(MS_SIZE):
            hbox[i] = QHBoxLayout()
        vbox = QVBoxLayout(spacing = 0)
        # 8行
        for y in range(0, MS_SIZE):
            for x in range(0, MS_SIZE):
                hbox[y].addWidget(self.button[y][x])
            vbox.addLayout(hbox[y])
        container = QWidget()
        container.setLayout(vbox)
        self.setCentralWidget(container)

        self.show()

    #ボタンにテキスト、もしくはアイコンをつける
    def show_cell_status(self):
        """ ゲームボードを表示 """
        for x in range(MS_SIZE):
            for y in range(MS_SIZE):
                # CLOSE -> x gray
                if(self.game.game_board[y][x] == CLOSE):
                    self.button[y][x].setText(' ')
                    self.button[y][x].set_bg_color('gray')
                    self.button[y][x].setIcon(QIcon('close.png'))
                # FLAG -> P yellow
                elif(self.game.game_board[y][x] == FLAG):
                    self.button[y][x].setText(' ')
                    self.button[y][x].set_bg_color('yellow')
                    self.button[y][x].setIcon(QIcon('flag.png'))
                # OPEN かつ not地雷 -> 数字 blue
                elif(self.game.game_board[y][x] == OPEN and self.game.mine_map[y][x] != -1):
                    self.button[y][x].setIcon(QIcon())
                    if(self.game.mine_map[y][x] != 0): # 周囲の地雷が0じゃない
                        self.button[y][x].setText(str(self.game.mine_map[y][x]))
                    else: # 周囲の地雷が0
                        self.button[y][x].setText(' ')
                    self.button[y][x].set_bg_color('blue')

    #正解の表示 地雷ならM それ以外は空白
    def ans_of_minemap(self):
        for y in range(MS_SIZE):
            for x in range(MS_SIZE):
                self.button[y][x].setText(' ')
                if(self.game.mine_map[y][x] == -1):
                    self.button[y][x].setIcon(QIcon('bomb.png'))
                else:
                    self.button[y][x].setIcon(QIcon())
                
def main():
    app = QApplication(sys.argv)
    w = MinesweeperWindow()
    app.exec_()
            
if __name__ == '__main__':
    main()