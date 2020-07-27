import re
import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication,QFrame
from PyQt5.uic import loadUi
import language_check
from colorama import Fore, Back, Style

#redColor = QColor(255, 0, 0)

@pyqtSlot()
class Ilets(QFrame):
    #MORFOLOGIK_RULE_EN_US


    def __init__(self):
        super(Ilets,self).__init__()
        loadUi("main.ui",self)
        self.setWindowTitle("ILETS Correct")
        self.intro_correct_button.clicked.connect(self.actionButton)
        self.first_correct_button.clicked.connect(self.first_actionButton)
        self.second_correct_button.clicked.connect(self.second_actionButton)
        self.opinion_correct_button.clicked.connect(self.opinion_actionButton)

    def actionButton(self):
        text = self.intro_textEdit.toPlainText()
        #print(self.intro_textEdit.setText(Back.LIGHTBLACK_EX+text))
        G_Score,L_Score=self.get_Score(text)
        redText = "<span style=\" font-size:15pt; font-weight:600; background-color:#ff0000;\" >"
        redText += text
        redText += "</span>"
        self.intro_textEdit.clear()
        self.intro_textEdit.append(redText)
        self.intro_grammer_lable.setText(G_Score)
        self.intr_lexis_lable.setText(L_Score)

    def get_Score(self,text):
        Grammer_Score = 0
        Lexis_Score = 0
        lang_tool = language_check.LanguageTool("en-US")
        Mistakes = lang_tool.check(text)
        for mistake in Mistakes:
            if mistake.ruleId != 'MORFOLOGIK_RULE_EN_US':
                Grammer_Score += 1
            else:
                Lexis_Score += 1
        return  str(Grammer_Score),str(Lexis_Score)

    def spiltParagraph(self,text):
        dic={}
        sent = re.split(r' *[\.\?!][\'"\)\]]* *', text)
        for s in sent:
            dic[text.index(s)]=s
        return dic

    def first_actionButton(self):
        text = self.first_textEdit.toPlainText()
        G_Score, L_Score = self.grammerScore(text)
        self.first_grammer_lable.setText(G_Score)
        self.first_lexis_lable.setText(L_Score)

    def second_actionButton(self):
        text = self.second_textEdit.toPlainText()
        G_Score, L_Score = self.grammerScore(text)
        self.second_grammer_lable.setText(G_Score)
        self.scecond_lexis_lable.setText(L_Score)

    def opinion_actionButton(self):
        text = self.opinion_textEdit.toPlainText()
        G_Score, L_Score = self.grammerScore(text)
        self.opinion_grammer_lable.setText(G_Score)
        self.opinion_lexis_lable.setText(L_Score)





    
app=QApplication(sys.argv)
widget=Ilets()
widget.show()
sys.exit(app.exec_())
