import re
import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication,QFrame
from PyQt5.uic import loadUi
import language_check


@pyqtSlot()
class Ilets(QFrame):
    #MORFOLOGIK_RULE_EN_US
    first_List=[]
    second_List=[]
    opinion_List=[]
    intro_List=[]
    G_first=0
    L_first=0
    G_second=0
    L_second=0
    G_opinion=0
    L_opinion=0
    G_intro=0
    L_intro=0
    total_Grammar_Score = 0
    total_Lexis_Score = 0
    total_Sectance_conut = 0
    text_General=''
    model=1

    def __init__(self):
        super(Ilets,self).__init__()
       # self.model=hub.load('E:\try\model')
        loadUi("main.ui",self)
        self.setWindowTitle("ILETS Correct")
        self.intro_correct_button.clicked.connect(self.actionButton)
        self.first_correct_button.clicked.connect(self.first_actionButton)
        self.second_correct_button.clicked.connect(self.second_actionButton)
        self.opinion_correct_button.clicked.connect(self.opinion_actionButton)
        self.clear_button.clicked.connect(self.clear_actionButton)
        self.final_Result_button.clicked.connect(self.finalResult_actionButton)

    def actionButton(self):
        text = self.intro_textEdit.toPlainText()
        Quest= self.Quest_textEdit.toPlainText()
        #print(self.intro_textEdit.setText(Back.LIGHTBLACK_EX+text))
        G_Score,L_Score,self.intro_List=self.get_Score(text)
        self.intro_textEdit.clear()
        boldColored=self.getBoldText(self.intro_List,text)
        self.intro_textEdit.clear()
        colorText = self.change_Color(boldColored, Quest)
        self.intro_textEdit.append(colorText)
        self.text_General+=colorText
        self.G_intro+=(9-(G_Score/self.total_Sectance_conut))
        self.L_intro+= (9 - (L_Score / self.total_Sectance_conut))
        self.intro_grammer_lable.setText(str(self.G_intro))
        self.intro_lexis_lable.setText(str(self.L_intro))
        self.intro_correct_button.setEnabled(False)
        print(self.advancedCheck(text))

    def get_Score(self,text):
        Grammer_Score = 0
        Lexis_Score = 0
        lang_tool = language_check.LanguageTool("en-US")
        Mistakes = lang_tool.check(text)
        IndexList=[]

        for mistake in Mistakes:
            smallList = []
            mistakeList=list(mistake)
            smallList.append(mistakeList[1])
            smallList.append(mistakeList[3])
            IndexList.append((smallList))
            if mistake.ruleId != 'MORFOLOGIK_RULE_EN_US':
                Grammer_Score += 1
            else:
                Lexis_Score += 1
        self.total_Grammar_Score+=Grammer_Score
        self.total_Lexis_Score+=Lexis_Score
        return  Grammer_Score,Lexis_Score,IndexList

    def spiltParagraph(self,text):
        sent = re.split(r' *[\.\?!][\'".\)\]]* *', text)
        return sent

    def first_actionButton(self):
        Quest = self.Quest_textEdit.toPlainText()
        text=self.first_textEdit.toPlainText()
        G_Score,L_Score,self.first_List=self.get_Score(text)
        boldColored = self.getBoldText(self.first_List, text)
        self.first_textEdit.clear()
        colorText = self.change_Color(boldColored, Quest)
        self.first_textEdit.append(colorText)
        self.text_General += colorText
        self.G_first += (9 - (G_Score / self.total_Sectance_conut))
        self.L_first += (9 - (L_Score / self.total_Sectance_conut))
        self.first_grammer_lable.setText(str(self.G_first))
        self.first_lexis_lable.setText(str(self.L_first))
        self.first_correct_button.setEnabled(False)

    def finalResult_actionButton(self):
        self.textBrowser_Report.setText(self.text_General)


    def second_actionButton(self):
        Quest = self.Quest_textEdit.toPlainText()
        text = self.second_textEdit.toPlainText()
        G_Score,L_Score,self.second_List=self.get_Score(text)
        self.second_grammer_lable.setText(str(G_Score))
        self.second_lexis_lable.setText(str(L_Score))
        boldColored = self.getBoldText(self.second_List, text)
        self.second_textEdit.clear()
        colorText = self.change_Color(boldColored, Quest)
        self.second_textEdit.append(colorText)
        self.text_General += colorText
        self.second_correct_button.setEnabled(False)

    def opinion_actionButton(self):
        Quest = self.Quest_textEdit.toPlainText()
        text = self.opinion_textEdit.toPlainText()
        G_Score,L_Score,self.opinion_List=self.get_Score(text)
        self.opinion_grammer_lable.setText(str(G_Score))
        self.opinion_lexis_lable.setText(str(L_Score))
        boldColored = self.getBoldText(self.opinion_List, text)
        self.opinion_textEdit.clear()
        colorText = self.change_Color(boldColored, Quest)
        self.opinion_textEdit.append(colorText)
        self.text_General += colorText
        self.opinion_correct_button.setEnabled(False)

    def change_Color(self,text, Quest):
        sentances = self.spiltParagraph(text)
        self.total_Sectance_conut+=len(sentances)
        redText = ''
        simi = .3
        for sent in sentances:
            # simi=self.similarity_measure(sent,Quest)
            if simi < .5:
                simi=.6
                redText += "<span style=\" font-weight:50pt; background-color:#ff0000; \" >"
                redText += sent
                redText += "</span>"
            elif simi < .7 and simi >= .5:
                simi = .8
                redText += "<span style=\" font-weight:50pt; background-color:#ffe000;\" >"
                redText += sent
                redText += "</span>"
            else:
                simi = .2
                redText += "<span style=\" font-weight:50pt; background-color:#C0C0C0;\" >"
                redText += sent
                redText += "</span>"
        return redText

    def similarity_measure(self,word1,word2):
        simi=0
        return simi

    def getBoldText(self,list=[],text=''):
        boldText = ''
        for ele in list:
            old = text[ele[0]:ele[1]]
            boldText += "<span style=\"  font-weight:bold;\" >"
            boldText += old
            boldText += "</span>  "
            text=text.replace(old,boldText,1)
        return text

    def advancedCheck(self,text=''):
        advancedCount=0
        List=['while','when','because','if']
        sentances=self.spiltParagraph(text)
        for sentance in sentances:
            for word in List:
                if  word in sentance:
                    advancedCount+=1
        return advancedCount

    def compositCheck(self,text=''):
        compositeCount = 0
        List = ['while', 'when', 'because', 'if']
        sentances = self.spiltParagraph(text)
        for sentance in sentances:
            for word in List:
                if word in sentance:
                    compositeCount += 1
        return compositeCount



    def clear_actionButton(self):
        self.intro_textEdit.clear()
        self.first_textEdit.clear()
        self.second_textEdit.clear()
        self.opinion_textEdit.clear()
        self.intro_grammer_lable.setText('Score')
        self.intro_lexis_lable.setText('Score')
        self.first_grammer_lable.setText('Score')
        self.second_grammer_lable.setText('Score')
        self.opinion_grammer_lable.setText('Score')
        self.first_lexis_lable.setText('Score')
        self.second_lexis_lable.setText('Score')
        self.opinion_lexis_lable.setText('Score')
        self.intro_correct_button.setEnabled(True)
        self.opinion_correct_button.setEnabled(True)
        self.second_correct_button.setEnabled(True)
        self.first_correct_button.setEnabled(True)
        self.textBrowser_Report.clear()



    
app=QApplication(sys.argv)
widget=Ilets()
widget.show()
sys.exit(app.exec_())
