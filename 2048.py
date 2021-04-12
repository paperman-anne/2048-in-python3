# -*- coding: utf-8 -*-

import wx
import random
import copy

"""
    Game 2048 in python
    1. draw the screen using wxpython
    2. capture the pressing button from keyborad and clicking from mouse
    3. initialize the page with 2 square randomly, renew the number and color while the button is pressed
    4. the ending condition is there is no 0 and each number has no nearby same number
    5. counting the score, and recording the highest rate
    6. can restart a game by clicking the restart button

"""

class MyFrame(wx.Frame):
    PANEL_ORIG_POINT = wx.Point(15,150)
    VALUE_COLOR_DEF = {
        0: "#98ddca",
        2: "#eff3f6",
        4: "#efe9e5",
        8: "#fff9ea",
        16: "#ced7df",
        32: "#D8E6E7",
        64: "#9DC3C1",
        128: "#77AAAD",
        256: "#3797a4",
        512: "#008891",
        1024: "#00587a",
        2048: "#28527a",
        4096: "#7f9eb2",
        8192: "#77919d",
        16384: "#6E7783",
        32768: "#274c5e",
        
    }
    IS_INITED = False
    tile_values = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    score = 0
    record = 0


    def __init__(self, title):
        super(MyFrame, self).__init__(None, title=title, size=(500,800))
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key)
        self.Centre()
        self.SetFocus()
        self.Show()

    def on_paint(self, event):
        if not self.IS_INITED:
            self.start_game()
            self.IS_INITED = True
    
    def init_screen(self):
        dc = wx.ClientDC(self)
        dc.SetBackground(wx.Brush("#5eaaa8"))
        dc.Clear()
        dc.SetPen(wx.Pen("#a3d2ca", 1, wx.PENSTYLE_SOLID))
        dc.SetBrush(wx.Brush("#a3d2ca"))
        dc.DrawRoundedRectangle(self.PANEL_ORIG_POINT.x, self.PANEL_ORIG_POINT.y, 450, 450, 5)

        self.score_text.SetLabel("0")
        self.record_text.SetLabel(str(self.record))

    def draw_tiles(self):
        dc = wx.ClientDC(self)
        dc.SetBackground(wx.Brush("#5eaaa8"))
        dc.Clear()
        dc.SetPen(wx.Pen("#a3d2ca", 1, wx.PENSTYLE_SOLID))
        dc.SetBrush(wx.Brush("#a3d2ca"))
        dc.DrawRoundedRectangle(self.PANEL_ORIG_POINT.x, self.PANEL_ORIG_POINT.y, 450, 450, 5)
        for row in range(4):
            for column in range(4):
                tile_value = self.tile_values[row][column]
                tile_color = self.VALUE_COLOR_DEF[tile_value]
                dc.SetBrush(wx.Brush(tile_color))
                dc.DrawRoundedRectangle(self.PANEL_ORIG_POINT.x + 110 * column + 10,
                                        self.PANEL_ORIG_POINT.y + 110 * row + 10, 100, 100, 5)
                dc.SetTextForeground("#000000")
                text_font = wx.Font(30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, faceName=u"Roboto")
                dc.SetFont(text_font)
                if tile_value != 0:
                    size = dc.GetTextExtent(str(tile_value))
                    if size[0] > 100:
                        text_font = wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, faceName=u"Roboto")
                        dc.SetFont(text_font)
                        size = dc.GetTextExtent(str(tile_value))
                    dc.DrawText(str(tile_value), self.PANEL_ORIG_POINT.x + 110 * column + 10 + (100 - size[0]) / 2,
                                self.PANEL_ORIG_POINT.y + 110 * row + 10 + (100 - size[1]) / 2)


    def on_key(self, event):
        key_code = event.GetKeyCode()
        last_values = copy.deepcopy(self.tile_values)
        if  key_code == wx.WXK_UP:
            self.merge_up()
        elif key_code == wx.WXK_DOWN:
            self.merge_down()
        elif key_code == wx.WXK_LEFT:
            self.merge_left()
        elif key_code == wx.WXK_RIGHT:
            self.merge_right()
        elif key_code == wx.WXK_SPACE:
            self.test_update_tiles()
            return
        if last_values == self.tile_values:
            if self.check_game_over():
                self.game_over()
        else:
            self.draw_score()
            self.add_square_random()
            self.draw_tiles()

    def on_btn_restart(self, event):
        self.game_over()

    def init_widgets(self):
        self.label_score_text = wx.StaticText(self, -1, "Score", (50,50),(70, 25), wx.ALIGN_CENTER)
        self.label_score_text.Font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, faceName=u"Roboto")
        self.label_score_text.SetForegroundColour("#eff3f6")
        self.label_score_text.SetBackgroundColour("#5eaaa8")

        self.label_record_text = wx.StaticText(self, -1, "Record", (200,50),(70, 25), wx.ALIGN_CENTER)
        self.label_record_text.Font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, faceName=u"Roboto")
        self.label_record_text.SetForegroundColour("#eff3f6")
        self.label_record_text.SetBackgroundColour("#5eaaa8")

        self.score_text = wx.StaticText(self, -1, "0", (50, 100), (70,25), wx.ALIGN_CENTER)
        self.score_text.Font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, faceName=u"Roboto")
        self.score_text.SetForegroundColour("#eff3f6")
        self.score_text.SetBackgroundColour("#5eaaa8")

        self.record_text = wx.StaticText(self, -1, str(self.record), (200, 100), (70,25), wx.ALIGN_CENTER)
        self.record_text.Font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, faceName=u"Roboto")
        self.record_text.SetForegroundColour("#eff3f6")
        self.record_text.SetBackgroundColour("#5eaaa8")

        self.restart_btn = wx.Button(self, -1, "Start\nAgain", (350, 50), (65,60), wx.ALIGN_CENTER)
        self.restart_btn.Font = wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, faceName=u"Roboto")
        self.restart_btn.SetForegroundColour("#eff3f6")
        self.restart_btn.SetBackgroundColour("#5eaaa8")
        self.restart_btn.Bind(wx.EVT_BUTTON, self.on_btn_restart)

    def draw_score(self):
        self.score_text.SetLabel(str(self.score))


    def update_row_value(self, row, positive):
            if positive == False:
                row.reverse()
            for pos in range(0,len(row)):
                if row[pos] == 0:
                    continue

                if pos < len(row) - 1:
                    move = pos+1
                    while row[move] == 0:
                        if move == 3:
                            break
                        move += 1
                    if row[pos] == row[move]:
                        row[pos] *= 2
                        row[move] = 0
                        self.score += row[pos]
                
            ans = []
            for pos in range(0,4):
                if row[pos] != 0:
                    ans.append(row[pos])
            while len(ans) < 4:
                ans.append(0)
            if positive == False:
                ans.reverse()
            return ans

    def start_game(self):
        self.tile_values = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        self.score = 0
        try:
            with open("record.txt") as fp:
                self.record = int(fp.read())

        except (IOError, ValueError) as err:
            print("read record error: %s" % err)
            self.record = 0

        self.init_widgets()
        self.init_screen()
        
        self.add_square_random()
        self.add_square_random()
        self.draw_tiles()

    def merge_up(self):
        for pos in range(len(self.tile_values[0])):
            copy_row = []
            for row in range(len(self.tile_values)):
                copy_row.append(self.tile_values[row][pos])
            merged_row = self.update_row_value(copy_row, True)
            for row in range(len(self.tile_values)):
                self.tile_values[row][pos] = merged_row[row]

    def merge_down(self):
        for pos in range(len(self.tile_values[0])):
            copy_row = []
            for row in range(len(self.tile_values)):
                copy_row.append(self.tile_values[row][pos])
            merged_row = self.update_row_value(copy_row, False)
            for row in range(len(self.tile_values)):
                self.tile_values[row][pos] = merged_row[row]

    def merge_left(self):
        for row in range(len(self.tile_values)):
            copy_row = self.tile_values[row][:]
            merged_row = self.update_row_value(copy_row, True)
            self.tile_values[row] = merged_row

    def merge_right(self):
        for row in range(len(self.tile_values)):
            copy_row = self.tile_values[row][:]
            merge_row = self.update_row_value(copy_row, False)
            self.tile_values[row] = merge_row

    def add_square_random(self):
        empty_tiles = [(row, col) for row in range(len(self.tile_values)) for col in range(len(self.tile_values[row]))
                        if self.tile_values[row][col] == 0]
        if len(empty_tiles) != 0:
            row, col = empty_tiles[random.randint(0, len(empty_tiles)-1)]
            self.tile_values[row][col] = 2
            return True
        else:
            return False

    def check_game_over(self):
        row_num = len(self.tile_values)
        row_col = len(self.tile_values[0])
        for i in range(row_num):
            for j in range(row_col):
                if self.tile_values[i][j] == 0 or self.near_exist(i, j):
                    return False
        
        return True

    def near_exist(self, x, y):
        check_num = self.tile_values[x][y]
        left = self.tile_values[x][y-1] if y-1 >= 0 else -1
        right = self.tile_values[x][y+1] if y+1 < 4 else -1
        up = self.tile_values[x-1][y] if x-1 >= 0 else -1
        down = self.tile_values[x+1][y] if x+1 < 4 else -1
        if left == check_num or right == check_num or up == check_num or down == check_num:
            return True
        
        return False

    def game_over(self):
        if self.score > self.record:
            self.record = self.score
            try:
                with open("record.txt", "w") as fp:
                    fp.write(str(self.score))
            except IOError as err:
                print(err)
        

        if wx.MessageBox(u"游戏结束，是否再来一局？", u"Game Over", wx.YES_NO) == wx.YES:
            self.start_game()

    def test_update_tiles(self):
        self.tile_values = [[0,2,4,8],[16,32,64,128],[256,512,1024,2048],[4096,8192,16384,32768]]
        self.draw_tiles()

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame('2048')
        frame.Show(True)
        return True

if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()