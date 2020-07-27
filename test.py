import re
import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication,QFrame
from PyQt5.uic import loadUi
import language_check


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
        Quest= self.Quest_textEdit.toPlainText()
        #print(self.intro_textEdit.setText(Back.LIGHTBLACK_EX+text))
        G_Score,L_Score=self.get_Score(text)
        colorText=self.change_Color(text,Quest)
        self.intro_textEdit.clear()
        self.intro_textEdit.append(colorText)
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
        sent = re.split(r' *[\.\?!][\'"\)\]]* *', text)
        return sent

    def first_actionButton(self):
        text=self.first_textEdit.toPlainText()
        G_Score,L_Score=self.get_Score(text)
        self.first_grammer_lable.setText(G_Score)
        self.first_lexis_lable.setText(L_Score)

    def second_actionButton(self):
        text = self.second_textEdit.toPlainText()
        G_Score,L_Score=self.get_Score(text)
        self.second_grammer_lable.setText(G_Score)
        self.scecond_lexis_lable.setText(L_Score)

    def opinion_actionButton(self):
        text = self.opinion_textEdit.toPlainText()
        G_Score,L_Score=self.get_Score(text)
        self.opinion_grammer_lable.setText(G_Score)
        self.opinion_lexis_lable.setText(L_Score)

    def change_Color(self,text, Quest):
        sentances = self.spiltParagraph(text)
        redText = ''
        simi = .3
        for sent in sentances:
            # simi=self.similarity_measure(sent,Quest)
            if simi < .5:
                simi=.6
                redText += "<span style=\" font-size:15pt; font-weight:600; background-color:#ff0000;\" >"
                redText += sent
                redText += "</span>"
            elif simi < .7 and simi >= .5:
                simi = .8
                redText += "<span style=\" font-size:15pt; font-weight:600; background-color:#ffe000;\" >"
                redText += sent
                redText += "</span>"
            else:
                simi = .2
                redText += "<span style=\" font-size:15pt; font-weight:600; background-color:#ffe1f0;\" >"
                redText += sent
                redText += "</span>"
        return redText

    def similarity_measure(self,word1,word2):
        simi=0
        return simi






    
app=QApplication(sys.argv)
widget=Ilets()
widget.show()
sys.exit(app.exec_())
