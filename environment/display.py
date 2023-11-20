import env
import test_game
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QMessageBox

#game = test_game.DivinizingGame(10, (610,10,610,10,10),0,1,1,1)

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.game = test_game.DivinizingGame(10, (610,10,610,10,10),0,1,1,1)
        # 设置窗口标题
        self.setWindowTitle('化神模拟器')
        self.setGeometry(100, 100, 1100, 700)
        # 创建一个 QPushButton 实例
        b0 = QPushButton('结束回合', self)
        b1 = QPushButton('金', self)
        b2 = QPushButton('木', self)
        b3 = QPushButton('水', self)
        b4 = QPushButton('火', self)
        b5 = QPushButton('土', self)
        b6 = QPushButton('使用灵气', self)
        b7 = QPushButton('消散灵气', self)
        b8 = QPushButton('化神', self)
        b9 = QPushButton('化凡', self)
        b10 = QPushButton('淬体法', self)
        b11 = QPushButton('塑魂法', self)
        b12 = QPushButton('感应法', self)
        b13 = QPushButton('涌泉法', self)
        b14 = QPushButton('意守法', self)
        b15 = QPushButton('定元咒', self)
        b16 = QPushButton('忘凡咒', self)
        b17 = QPushButton('九龙', self)
        self.text = QLabel(self)
        self.text2 = QLabel(self)
        # 将按钮设置为窗口的中心部件
        b0.setGeometry(650, 440+100, 100, 50)
        b1.setGeometry(425, 440+100, 70, 50)
        b2.setGeometry(460, 540+100, 70, 50)
        b3.setGeometry(480, 490+100, 70, 50)
        b4.setGeometry(390, 540+100, 70, 50)
        b5.setGeometry(370, 490+100, 70, 50)
        b6.setGeometry(650, 490+100, 100, 50)
        b7.setGeometry(650, 540+100, 100, 50)
        b8.setGeometry(20, 450+20+100, 70, 50)
        b9.setGeometry(80, 450+20+100, 70, 50)
        b10.setGeometry(140, 450+20+100, 70, 50)
        b11.setGeometry(200, 450+20+100, 70, 50)
        b12.setGeometry(260, 450+20+100, 70, 50)
        b13.setGeometry(20, 500+20+100, 70, 50)
        b14.setGeometry(80, 500+20+100, 70, 50)
        b15.setGeometry(140, 500+20+100, 70, 50)
        b16.setGeometry(200, 500+20+100, 70, 50)
        b17.setGeometry(260, 500+20+100, 70, 50)
        self.text.setGeometry(20, 20, 500, 400)
        self.text2.setGeometry(350, 20, 700, 500)
        t = '''
        技能表:
            化神:(3)【后继无力】【凡体】状态下方可使用.【仙性】+1并进入仙胎状态;每有【塑魂】*10,则【仙性】额外+1
            化凡:(2)【后继无力】【仙胎】状态下方可使用。进入凡体状态，每有【淬体】*10,则吸收一点灵气
            淬体法:(5)【淬体】+5。若处于【凡体】状态,则【淬体】额外+1
            塑魂法:(5)【塑魂】+5。若处于【仙胎】状态,则【塑魂】额外+2
            感应法:(3+1)【仙性】+3,若在【仙胎】状态下释放,则【仙性】额外+2
            涌泉法:(2+2)【后继无力】下回合开始时,吸收4点灵气。若在【仙胎】状态下释放,则【凡性】-3
            意守法:(3+2)【后继无力】下回合开始时若处于【仙胎】状态，则每有【仙性】*10,吸收一点灵气
            定元咒:(3+1)【后继无力】【凡体】状态下方可使用.下一次进入【仙胎】状态时,吸收4点灵气
            忘凡咒:(1+1)【后继无力】【仙胎】状态下方可使用.本回合结束时，若仍处于【仙胎】状态,
                  则【凡性】-4.首次释放此技能时,效果翻倍.
            九龙天雷火:(2+1)使用相生的灵气释放时,【淬体】+3; 使用相克的灵气释放时,【塑魂】+3.

        游戏机制: 
            1.胜利条件: 当凡性达到100时,游戏失败;当仙性达到100时,游戏成功,淬体和塑魂越高越好。凡性先于仙性结算。
            2.【凡体】回合结束时，如果你处于【凡体】状态，【凡性】+4;回合开始时,
               如果你处于【凡体】状态,获得随机8点灵气
            3.【仙胎】回合开始时，如果你处于【仙胎】状态，【仙性】+4;跳过吸收灵气阶段.
            4.第n回合结束时,【凡性】增加n
            5.混元仙体丹:初始仙性+4
            6.天命淬体丹:每次淬体效果+1
            7.澄心塑魂丹:每次塑魂效果+1
            8.相生灵气:金-水, 水-木, 木-火, 火-土, 土-金
            9.相克灵气:金-木, 水-火, 木-土, 火-金, 土-水
            10.游戏从第1回合开始计算,处于【凡体】,初始拥有8点灵气
            11.灵气上限为6点,回合结束时若有多余的灵气需要消散到灵气上限
            12.灵气获取按照灵根分布概率抽取
            13.默认五行化神,每回合额外吸收一点相应灵气
            14.【后继无力】每回合只能使用一次
        '''
        self.text2.setText(t)
        # 将按钮的点击信号与槽函数 on_button_click 进行绑定
        b0.clicked.connect(self.on_b0)
        b1.clicked.connect(self.on_b1)
        b2.clicked.connect(self.on_b2)
        b3.clicked.connect(self.on_b3)
        b4.clicked.connect(self.on_b4)
        b5.clicked.connect(self.on_b5)
        b6.clicked.connect(self.on_b6)
        b7.clicked.connect(self.on_b7)
        b8.clicked.connect(self.on_b8)
        b9.clicked.connect(self.on_b9)
        b10.clicked.connect(self.on_b10)
        b11.clicked.connect(self.on_b11)
        b12.clicked.connect(self.on_b12)
        b13.clicked.connect(self.on_b13)
        b14.clicked.connect(self.on_b14)
        b15.clicked.connect(self.on_b15)
        b16.clicked.connect(self.on_b16)
        b17.clicked.connect(self.on_b17)

        b8.setToolTip('化神:(3)【后继无力】【凡体】状态下方可使用.\n【仙性】+1并进入仙胎状态;每有【塑魂】*10,则【仙性】额外+1')
        b9.setToolTip('化凡:(2)【后继无力】【仙胎】状态下方可使用。\n进入凡体状态, 每有【淬体】*10,则吸收一点灵气')
        b10.setToolTip('淬体法:(5)\n【淬体】+5。若处于【凡体】状态,则【淬体】额外+1')
        b11.setToolTip('塑魂法:(5)\n【塑魂】+5。若处于【仙胎】状态,则【塑魂】额外+2')
        b12.setToolTip('感应法:(3+1)\n【仙性】+3,若在【仙胎】状态下释放,则【仙性】额外+2')
        b13.setToolTip('涌泉法:(2+2)【后继无力】\n下回合开始时,吸收4点灵气。若在【仙胎】状态下释放,则【凡性】-3')
        b14.setToolTip('意守法:(3+2)【后继无力】\n下回合开始时若处于【仙胎】状态, 则每有【仙性】*10,吸收一点灵气')
        b15.setToolTip('定元咒:(3+1)【后继无力】【凡体】状态下方可使用.\n下一次进入【仙胎】状态时,吸收4点灵气')
        b16.setToolTip('忘凡咒:(1+1)【后继无力】【仙胎】状态下方可使用.\n本回合结束时, 若仍处于【仙胎】状态,则【凡性】-4.首次释放此技能时,效果翻倍.')
        b17.setToolTip('九龙天雷火:(2+1)\n使用相生的灵气释放时,【淬体】+3; 使用相克的灵气释放时,【塑魂】+3.')

        self.action_buttons = [b0,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15,b16,b17]
        self.update_enabled()
        self.update_text()

    def update_text(self):
        skill_dict = {0:"无",8:"化神",9:"化凡",10:"淬体法",11:"塑魂法",12:"感应法",13:"涌泉法",14:"意守法",15:"定元咒",16:"忘凡咒",17:"九龙天雷火"}
        state = self.game.state
        t = '''
            当前行动状态:{}\n\
            当前仙凡状态:{}\n\
            当前灵根权重:金:{} 木:{} 水:{} 火:{} 土:{}\n\
            五行化神:{}\n\
            仙体丹:{} 淬体丹:{} 塑魂丹:{}\n\
            当前回合数:{}\n\
            当前灵气数:金:{} 木:{} 水:{} 火:{} 土:{}\n\
            当前凡性:{}\n\
            当前仙性:{}\n\
            当前淬体:{}\n\
            当前塑魂:{}\n\
            定远咒层数:{}\n\
            涌泉法层数:{}\n\
            当前释放技能:{}\n\
            当前总共需要灵气:{}\n\
            当前选择灵气:金:{} 木:{} 水:{} 火:{} 土:{}\n\
            总灵气数:{}\
            '''.format(['出牌','消散灵气','消耗灵气'][state[0]],\
                    ['凡体','仙胎'][state[1]],\
                    state[2][0],state[2][1],state[2][2],state[2][3],state[2][4],\
                    ['金','木', '水', '火', '土'][state[3]],\
                    state[4],state[5],state[6],\
                    state[7],\
                    state[8][0], state[8][1],state[8][2],state[8][3],state[8][4],\
                    state[9],state[10],state[11],state[12],state[13],state[14],\
                    skill_dict[state[22]],state[23],\
                    state[24][0],state[24][1],state[24][2],state[24][3],state[24][4],\
                    sum(state[8]))
        #print(t)
        self.text.setText(t)
        self.action_buttons[1].setText('金({})'.format(state[8][0]))
        self.action_buttons[2].setText('木({})'.format(state[8][1]))
        self.action_buttons[3].setText('水({})'.format(state[8][2]))
        self.action_buttons[4].setText('火({})'.format(state[8][3]))
        self.action_buttons[5].setText('土({})'.format(state[8][4]))
        pass
    
    def update_enabled(self):
        action_list = self.game.get_action_list()
        for i in range(18):
            if i in action_list:
                self.action_buttons[i].setEnabled(True)
            else:
                self.action_buttons[i].setEnabled(False)
        if self.game.is_finished() != 0:
            for i in range(18):
                self.action_buttons[i].setEnabled(False)
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle('提示')
            if self.game.is_finished() == 1:
                msg_box.setText('化神成功!淬体:{},塑魂:{}'.format(self.game.state[11],self.game.state[12]))
                msg_box.exec_()
            else:
                msg_box.setText('化神失败!')
                msg_box.exec_()

    def on_b0(self):
        self.game.step(0)
        self.update_text()
        self.update_enabled()
    def on_b1(self):
        self.game.step(1)
        self.update_text()
        self.update_enabled()
    def on_b2(self):
        self.game.step(2)
        self.update_text()
        self.update_enabled()
    def on_b3(self):
        self.game.step(3)
        self.update_text()
        self.update_enabled()
    def on_b4(self):
        self.game.step(4)
        self.update_text()
        self.update_enabled()
    def on_b5(self):
        self.game.step(5)
        self.update_text()
        self.update_enabled()
    def on_b6(self):
        self.game.step(6)
        self.update_text()
        self.update_enabled()
    def on_b7(self):
        self.game.step(7)
        self.update_text()
        self.update_enabled()
    def on_b8(self):
        self.game.step(8)
        self.update_text()
        self.update_enabled()
    def on_b9(self):
        self.game.step(9)
        self.update_text()
        self.update_enabled()
    def on_b10(self):
        self.game.step(10)
        self.update_text()
        self.update_enabled()
    def on_b11(self):
        self.game.step(11)
        self.update_text()
        self.update_enabled()
    def on_b12(self):
        self.game.step(12)
        self.update_text()
        self.update_enabled()
    def on_b13(self):
        self.game.step(13)
        self.update_text()
        self.update_enabled()
    def on_b14(self):
        self.game.step(14)
        self.update_text()
        self.update_enabled()
    def on_b15(self):
        self.game.step(15)
        self.update_text()
        self.update_enabled()
    def on_b16(self):
        self.game.step(16)
        self.update_text()
        self.update_enabled()
    def on_b17(self):
        self.game.step(17)
        self.update_text()
        self.update_enabled()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 创建一个 MyWindow 实例
    window = MyWindow()

    # 显示窗口
    window.show()

    # 进入程序事件循环
    sys.exit(app.exec_())