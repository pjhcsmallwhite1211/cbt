import sys,ui,lib
from PyQt5.QtWidgets import QApplication, QMainWindow,QLabel,QFrame,QHBoxLayout
from PyQt5.QtCore import QTimer
from PyQt5 import QtGui
class UserWindow(object):
    def __init__(self,Queue,queueReceive):

        self.app=QApplication(sys.argv)
        self.main=QMainWindow()
        self.ui = ui.Ui_MainWindow()
        self.ui.setupUi(self.main)
        self.main.show()
        self.queue=Queue
        self.queueReceive=queueReceive
        self.main.closeEvent=lambda a=0: self.queue.put('exit')
        self.main.setStyleSheet(lib.read_qss_file('./css.qss'))
        self.setupEvent()
        self.timer=QTimer()
        self.timer.timeout.connect(self.receive)
        self.timer.start(1)
        self.tabs=[[],[]]
        
    def receive(self):

        if self.queueReceive.empty()==False:

            result=self.queueReceive.get()
            
            index=self.ui.tabWidget.currentIndex()
            print(index)
            scrollArea=[self.ui.scrollAreaWidgetContents,self.ui.scrollAreaWidgetContents_2][index]
            verticalLayout=[self.ui.verticalLayout,self.ui.verticalLayout_2][index]

            frame = QFrame(scrollArea)
            frame.setFrameShape(QFrame.StyledPanel)
            frame.setFrameShadow(QFrame.Raised)
            frame.setObjectName(f"frame__{len(self.tabs[index])}")
            horizontalLayout = QHBoxLayout(frame)
            horizontalLayout.setObjectName(f"horizontalLayout__{len(self.tabs[index])}")
            label = QLabel(frame)
            label.setFrameShape(QFrame.NoFrame)
            label.setFrameShadow(QFrame.Plain)
            label.setText("")
            label.setPixmap(QtGui.QPixmap(":/icon/res/amethyst_shard.png"))
            label.setScaledContents(True)
            label.setWordWrap(False)
            label.setOpenExternalLinks(False)
            label.setObjectName(f"labelIcon__{len(self.tabs[index])}")
            horizontalLayout.addWidget(label)
            labelText = QLabel(frame)
            labelText.setObjectName(f"label__{len(self.tabs[index])}")
            labelText.setText(f"{result}")
            labelText.setWordWrap(True)
            horizontalLayout.addWidget(labelText)
            horizontalLayout.setStretch(0, 1)
            horizontalLayout.setStretch(1, 9)
            verticalLayout.addWidget(frame)

            self.tabs[index].append({'frame':frame,'label':label,'TextLabel':labelText,'horizontalLayout':horizontalLayout})
            print('lpsa')
    def send(self,textEdit):
        print('send start')
        text = textEdit.toPlainText()
        self.queue.put(f'speak/{text}')
        print('put !')
        index=self.ui.tabWidget.currentIndex()
        print(index)
        scrollArea=[self.ui.scrollAreaWidgetContents,self.ui.scrollAreaWidgetContents_2][index]
        verticalLayout=[self.ui.verticalLayout,self.ui.verticalLayout_2][index]
        label=QLabel(scrollArea)
        label.setObjectName(f"{index},{len(self.tabs[index])},user")
        label.setText(text)
        label.setWordWrap(True)
        verticalLayout.addWidget(label)
        self.tabs[index].append(label)

        textEdit.setText('')
        print('send end')
    def setupEvent(self):
        self.ui.send.clicked.connect(lambda: self.send(self.ui.textEdit))
        self.ui.send_2.clicked.connect(lambda: self.send(self.ui.textEdit_2))
        self.queue.put("start")
    def run(self):
        sys.exit(self.app.exec_())
