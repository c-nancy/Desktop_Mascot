import sys

from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QDialog, QLabel
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *




class MyDialog(QDialog):

    # 自定义信号
    mySignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        # 设置蒙版图片，调节大小
        self.pix = QBitmap('dialogbox_shape.png')  # 蒙版图片
        self.resize(self.pix.size())
        self.setMask(self.pix)  # 设置蒙版

        self.guess = 250
        self.top = 501
        self.down = 0
        self.direction = True

        self.text = QPlainTextEdit()

        self.guessText = QLineEdit()

        # 添加按钮
        self.exitButton = QPushButton("No!")
        self.talkButton = QPushButton("Of course not")
        self.okButton = QPushButton("OK, cool")
        self.highButton = QPushButton("Higher")
        self.lowButton = QPushButton("Lower")
        self.correctButton = QPushButton("Correct")

        self.initUI()

    def initUI(self):
        # OK键的状态。0是游戏未开始，1是猜测未开始，2是游戏已结束
        self.states = [0, 1, 2]
        self.playState = self.states[0]

        # 添加文字
        self.text.setReadOnly(True)
        self.text.setStyleSheet("background:transparent;border-width:0;border-style:outset")
        size = self.text.size()

        # 猜测文字
        self.guessText.setReadOnly(True)
        self.guessText.setStyleSheet("background:transparent;border-width:0;border-style:outset")
        self.guessText.setText("")



        # 按钮背景透明
        self.exitButton.setStyleSheet("QPushButton{background: transparent;}")
        self.talkButton.setStyleSheet("QPushButton{background: transparent;}")
        self.okButton.setStyleSheet("QPushButton{background: transparent;}")
        self.highButton.setStyleSheet("QPushButton{background: transparent;}")
        self.lowButton.setStyleSheet("QPushButton{background: transparent;}")
        self.correctButton.setStyleSheet("QPushButton{background: transparent;}")

        # 按钮点击事件
        self.exitButton.clicked.connect(self.clickExit)
        self.talkButton.clicked.connect(self.clickTalk)
        self.okButton.clicked.connect(self.clickOK)
        self.highButton.clicked.connect(self.clickHigher)
        self.lowButton.clicked.connect(self.clickLower)
        self.correctButton.clicked.connect(self.clickCorrect)


        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.text)
        layout.addWidget(self.guessText)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.exitButton)
        buttonLayout.addWidget(self.talkButton)
        buttonLayout.addWidget(self.okButton)
        buttonLayout.addWidget(self.lowButton)
        buttonLayout.addWidget(self.highButton)
        buttonLayout.addWidget(self.correctButton)

        # 隐藏暂时不需要的按钮
        self.okButton.hide()
        self.lowButton.hide()
        self.highButton.hide()
        self.correctButton.hide()

        self.exitButton.hide()
        self.talkButton.hide()

        layout.addLayout(buttonLayout)
        # margins四个参数分别为：左，上，右，下
        layout.setContentsMargins(50,50,50,80)
        self.setLayout(layout)
        self.initText()

        self.show()

    # 移动对话框位置
    def moveDialog(self, point):
        self.move(point)

    # 隐藏所有
    def hideAll(self):
        self.text.clear()
        self.guessText.clear()
        self.okButton.hide()
        self.lowButton.hide()
        self.highButton.hide()
        self.correctButton.hide()
        self.exitButton.hide()
        self.talkButton.hide()


    # 对话框背景
    def paintEvent(self, QPaintEvent):
        paint = QPainter(self)
        paint.drawPixmap(0, 0, self.pix.width(), self.pix.height(), QPixmap('dialogbox.png'))

    # 初始菜单
    def initText(self):
        self.hideAll()
        self.text.setPlainText("The frog knows EVERYTHING.")
        self.text.appendPlainText("Do you believe it?")
        self.exitButton.show()
        self.talkButton.show()

    # 退出键
    def clickExit(self):
        self.mySignal.emit("close")
        self.close()

    # 开始游戏键
    def clickTalk(self):
        self.mySignal.emit("talk")
        self.exitButton.hide()
        self.talkButton.hide()
        self.gameText()

    # OK键
    def clickOK(self):
        if self.playState == 0:
            self.gamePlaying()
            self.playState = 1
        elif self.playState == 1:
            self.gameWin()
            self.playState = 2
        elif self.playState == 2:
            self.initText()
            self.playState = 0

    # 开始游戏界面
    def gameText(self):
        self.hideAll()
        self.text.setPlainText("What?!")
        self.text.appendPlainText("You should believe an honest frog!")
        self.text.appendPlainText("......")
        self.text.appendPlainText("OK, let's play a game.")
        self.okButton.show()

    # 游戏过程
    def gamePlaying(self):
        self.hideAll()
        self.text.setPlainText("Think of a number between 0 and 500.")
        self.text.appendPlainText("And I'll guess it.")
        self.text.appendPlainText("")
        self.text.appendPlainText("Your number maybe...")
        self.guess = 250
        self.guessText.setText(str(self.guess))
        self.lowButton.show()
        self.highButton.show()
        self.correctButton.show()
        self.top = 501
        self.down = 0
        self.direction = True


    # 猜数字。方向正表示向右，负表示向左
    def guessNumber(self, down, top, now, direction):
        if direction:
            down = now
        else:
            top = now
        now = (top + down) // 2
        return top, down, now

    # 数字比猜测更高
    def clickHigher(self):
        self.down = self.guess
        self.guess = (self.top + self.down) // 2
        self.guessText.setText(str(self.guess))

    # 数字比猜测更低
    def clickLower(self):
        self.top = self.guess
        self.guess = (self.top + self.down) // 2
        self.guessText.setText(str(self.guess))

    # 猜对
    def clickCorrect(self):
        self.playState = 2
        self.hideAll()
        self.text.setPlainText("See? I've told you already.")
        self.text.appendPlainText("A frog knows everything.")
        self.okButton.show()



