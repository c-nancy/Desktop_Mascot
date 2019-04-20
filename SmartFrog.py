import sys
# from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
# from PyQt5.QtWidgets import QWidget, QApplication
# from PyQt5.QtGui import QPixmap, QPainter, QBitmap, QCursor, QMouseEvent
import PyQt5.QtCore as QtCore



class MyWindow(QWidget):  # 不规则窗体
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)

        # 设置蒙版图片，调节大小
        self.pix = QBitmap('frog_shape.png')  # 蒙版图片
        self.resize(self.pix.size())
        self.setMask(self.pix)  # 设置蒙版

        # 设置无边框和置顶窗口样式
        self.setWindowFlags(Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

        # 菜单栏
        self.menuDialog = MyDialog()

        self.isDialogShown = False
        self.dialogDist = QPoint(100, 100)

        # 接收对话框传来的信号
        self.menuDialog.mySignal.connect(self.getDialogSignal)

        self.initUI()


    def initUI(self):
        # 窗体尺寸
        qr = self.frameGeometry()

        # 窗体中心点
        m_w = qr.width() // 2
        m_h = qr.height() // 2

        # 桌面左下角
        bp = QDesktopWidget().availableGeometry().bottom()
        rp = QDesktopWidget().availableGeometry().left()

        # 窗体中心应当放置到的点
        origin_point = QPoint(rp + m_w, bp - m_h)

        # 移动窗体中心
        qr.moveCenter(origin_point)
        self.move(qr.topLeft())

        # 确定对话框与窗体的相对距离
        dialogSize = self.menuDialog.geometry()
        self.dialogDist = QPoint(dialogSize.width() // 2 + m_w, dialogSize.height() // 2 - m_h)
        self.menuDialog.moveDialog(self.pos() + self.dialogDist)
        self.menuDialog.setVisible(False)

    def getDialogSignal(self, connect):
        if connect == "close":
            self.close()
        elif connect == "shutup":
            self.isDialogShown = False


    def paintEvent(self, QPaintEvent):  # 绘制窗口
        paint = QPainter(self)
        paint.drawPixmap(0, 0, self.pix.width(), self.pix.height(), QPixmap('frog.png'))

    def mouseMoveEvent(self, e: QMouseEvent):  # 重写移动事件，只允许沿x轴移动
        self._endPos = QPoint(e.pos().x() - self._startPos.x(), 0)
        self.move(self.pos() + self._endPos)
        # self.menuDialog.moveDialog(self.pos())
        self.menuDialog.moveDialog(self.pos() + self.dialogDist)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None

    def mouseDoubleClickEvent(self, event):
        if not self.isDialogShown:
            self.menuDialog.setVisible(True)
            self.menuDialog.initText()
            self.isDialogShown = True
        else:
            self.menuDialog.setVisible(False)
            self.isDialogShown = False


# ================================以下为对话框================================


class MyDialog(QDialog):

    # 自定义信号
    mySignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        # 设置蒙版图片，调节大小
        self.pix = QBitmap('dialogbox_shape.png')  # 蒙版图片
        self.resize(self.pix.size())
        self.setMask(self.pix)  # 设置蒙版

        self.setWindowFlags(Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

        self.guess = 250
        self.top = 501
        self.down = 0
        self.direction = True

        self.text = QPlainTextEdit()

        self.guessText = QLineEdit()

        self.font = QtGui.QFont()

        # 添加按钮
        self.exitButton = QPushButton("No!")
        self.talkButton = QPushButton("Of course not")
        self.okButton = QPushButton("OK, cool")
        self.highButton = QPushButton("Higher")
        self.lowButton = QPushButton("Lower")
        self.correctButton = QPushButton("Correct")
        self.closeButton = QPushButton("(Ignore)")

        self.initUI()

    def initUI(self):
        # OK键的状态。0是游戏未开始，1是猜测未开始，2是游戏已结束
        self.states = [0, 1, 2]
        self.playState = self.states[0]

        self.font.setFamily("Arial")
        self.font.setPointSize(9)

        # 添加文字
        self.text.setReadOnly(True)
        self.text.setStyleSheet("background:transparent;border-width:0;border-style:outset")
        size = self.text.size()

        # 猜测文字
        self.guessText.setReadOnly(True)
        self.guessText.setStyleSheet("background:transparent;border-width:0;border-style:outset")
        self.guessText.setText("")

        self.text.setFont(self.font)
        self.guessText.setFont(self.font)

        # 按钮背景透明
        self.exitButton.setStyleSheet("QPushButton{background: transparent;}")
        self.talkButton.setStyleSheet("QPushButton{background: transparent;}")
        self.okButton.setStyleSheet("QPushButton{background: transparent;}")
        self.highButton.setStyleSheet("QPushButton{background: transparent;}")
        self.lowButton.setStyleSheet("QPushButton{background: transparent;}")
        self.correctButton.setStyleSheet("QPushButton{background: transparent;}")
        self.closeButton.setStyleSheet("QPushButton{background: transparent;}")

        # 按钮点击事件
        self.exitButton.clicked.connect(self.clickExit)
        self.talkButton.clicked.connect(self.clickTalk)
        self.okButton.clicked.connect(self.clickOK)
        self.highButton.clicked.connect(self.clickHigher)
        self.lowButton.clicked.connect(self.clickLower)
        self.correctButton.clicked.connect(self.clickCorrect)
        self.closeButton.clicked.connect(self.clickClose)

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.text)
        layout.addWidget(self.guessText)
        layout.addStretch()

        # 按钮布局
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.exitButton)
        buttonLayout.addWidget(self.talkButton)
        buttonLayout.addWidget(self.okButton)
        buttonLayout.addWidget(self.lowButton)
        buttonLayout.addWidget(self.highButton)
        buttonLayout.addWidget(self.correctButton)
        buttonLayout.addWidget(self.closeButton)
        buttonLayout.addStretch()

        # 隐藏暂时不需要的按钮
        self.okButton.hide()
        self.lowButton.hide()
        self.highButton.hide()
        self.correctButton.hide()
        self.closeButton.hide()

        self.exitButton.hide()
        self.talkButton.hide()

        layout.addLayout(buttonLayout)
        # margins四个参数分别为：左，上，右，下
        layout.setContentsMargins(50,50,50,150)
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
        self.closeButton.hide()


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
        self.closeButton.show()

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
        self.text.appendPlainText("You should trust an honest frog!")
        self.text.appendPlainText("......")
        self.text.appendPlainText("OK, let's play a game.")
        self.okButton.show()
        self.closeButton.show()

    # 游戏过程
    def gamePlaying(self):
        self.hideAll()
        self.text.setPlainText("Think of a number between 0 and 500.")
        self.text.appendPlainText("And I'll guess it.")
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

    # 关闭对话框
    def clickClose(self):
        self.setVisible(False)
        self.mySignal.emit("shutup")






if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())
