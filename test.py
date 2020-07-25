import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import  QApplication,QFrame
from PyQt5.uic import loadUi
import language_check


lang_tool = language_check.LanguageTool("en-US")
global Grammer_Score
global Lexis_Score

@pyqtSlot()
class Ilets(QFrame) :

    #MORFOLOGIK_RULE_EN_US
    Grammer_Score=0
    Lexis_Score=0

    def __init__(self):
        super(Ilets,self).__init__()
        loadUi("main.ui",self)
        self.setWindowTitle("ILETS Correct")
        self.intro_correct_button.clicked.connect(self.actionButton)

    def actionButton(self):
        text = self.intro_textEdit.toPlainText()
        self.grammerScore(text)
        self.intro_grammer_lable.setText(Grammer_Score)
        self.intr_lexis_lable.setText(Lexis_Score)


    def grammerScore(Text=''):
        Mistakes = lang_tool.check(Text)
        for mistake in Mistakes:
            if mistake.ruleId != 'MORFOLOGIK_RULE_EN_US':
                Grammer_Score += 1
            else:
                Lexis_Score += 1


    
app=QApplication(sys.argv)
widget=Ilets()
widget.show()
sys.exit(app.exec_())
