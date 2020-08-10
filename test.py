import re
import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication,QFrame
from PyQt5.uic import loadUi
import language_check


@pyqtSlot()
class Ilets(QFrame):
    #the lists of error indexe in each part of paragraph
    first_List,second_List ,opinion_List,intro_List=[],[],[],[]
    #the text of each part of paragraph
    firstText , introText, secondText, opinionText= '', '', '', ''
    total_Advanced_Count , total_Composite_Count = 0 , 0
    # the grammar and Lexis of each part of paragraph
    G_first , L_first = 9 , 9
    G_second , L_second = 9 , 9
    G_opinion , L_opinion = 9 , 9
    G_intro , L_intro = 9 , 9
    # the total scores of program
    total_Grammar_Score = 0
    total_Lexis_Score = 0
    total_Sentance_Score = 0
    overAll_Score = 0
    #the count of sentance of each part of paragraph
    total_Sentance_conut0 , total_Sentance_conut1 ,total_Sentance_conut2 ,total_Sentance_conut3 = 0,0,0,0


    text_General=''
    model=1

    def __init__(self):
        super(Ilets,self).__init__()
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
        self.introText=text
        Quest= self.Quest_textEdit.toPlainText()
        G_Score,L_Score,self.intro_List=self.get_Score(text)
        self.intro_textEdit.clear()
        boldColored=self.getBoldText(self.intro_List,text)
        colorText ,self.total_Sentance_conut0= self.change_Color(boldColored, Quest)
        self.intro_textEdit.append(colorText)
        self.text_General+=colorText
        self.G_intro = (9 - (G_Score / self.total_Sentance_conut0))
        self.L_intro = (9 - (L_Score / self.total_Sentance_conut0))
        self.intro_grammer_lable.setText(str(self.G_intro))
        self.intro_lexis_lable.setText(str(self.L_intro))
        self.intro_correct_button.setEnabled(False)


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
        self.firstText=text
        G_Score,L_Score,self.first_List=self.get_Score(text)
        boldColored = self.getBoldText(self.first_List, text)
        self.first_textEdit.clear()
        colorText,self.total_Sentance_conut1 = self.change_Color(boldColored, Quest)
        self.first_textEdit.append(colorText)
        self.text_General += colorText
        self.G_first = (9 - (G_Score / self.total_Sentance_conut1))
        self.L_first = (9 - (L_Score / self.total_Sentance_conut1))
        self.first_grammer_lable.setText(str(self.G_first))
        self.first_lexis_lable.setText(str(self.L_first))
        self.first_correct_button.setEnabled(False)

    def finalResult_actionButton(self):
        self.textBrowser_Report.setText(self.text_General)
        self.getOverAll_Score()
        self.final_Resulat_Coherence.setText(str(self.total_Sentance_Score))
        self.final_Result_Lexis.setText(str(self.total_Lexis_Score))
        self.final_Result_Grammer.setText(str(self.total_Grammar_Score))
        self.final_Result_OverallScore.setText(str(self.overAll_Score))

    def second_actionButton(self):
        Quest = self.Quest_textEdit.toPlainText()
        text = self.second_textEdit.toPlainText()
        self.secondText=text
        G_Score,L_Score,self.second_List=self.get_Score(text)
        boldColored = self.getBoldText(self.second_List, text)
        self.second_textEdit.clear()
        colorText,self.total_Sentance_conut2 = self.change_Color(boldColored, Quest)
        self.second_textEdit.append(colorText)
        self.text_General += colorText
        self.G_second = (9 - (G_Score / self.total_Sentance_conut2))
        self.L_second = (9 - (L_Score / self.total_Sentance_conut2))
        self.second_grammer_lable.setText(str(self.G_second))
        self.second_lexis_lable.setText(str(self.L_second))
        self.second_correct_button.setEnabled(False)

    def opinion_actionButton(self):
        Quest = self.Quest_textEdit.toPlainText()
        text = self.opinion_textEdit.toPlainText()
        self.opinionText=text
        G_Score,L_Score,self.opinion_List=self.get_Score(text)
        self.opinion_grammer_lable.setText(str(G_Score))
        self.opinion_lexis_lable.setText(str(L_Score))
        boldColored = self.getBoldText(self.opinion_List, text)
        self.opinion_textEdit.clear()
        colorText,self.total_Sentance_conut3 = self.change_Color(boldColored, Quest)
        self.opinion_textEdit.append(colorText)
        self.text_General += colorText
        self.G_opinion = (9 - (G_Score / self.total_Sentance_conut3))
        self.L_opinion = (9 - (L_Score / self.total_Sentance_conut3))
        self.opinion_grammer_lable.setText(str(self.G_opinion))
        self.opinion_lexis_lable.setText(str(self.L_opinion))
        self.opinion_correct_button.setEnabled(False)

    def change_Color(self,text, Quest):
        sentances = self.spiltParagraph(text)
        redText = ''
        simi = .3
        for sent in sentances:
            # simi=self.similarity_measure(sent,Quest)
            if simi < .5:
                simi=.6
                redText += "<span style=\"  background-color:#ff0000; \" >"
                redText += sent
                redText += "</span>"
            elif simi < .7 and simi >= .5:
                simi = .8
                redText += "<span style=\"  background-color:#ffe000;\" >"
                redText += sent
                redText += "</span>"
            else:
                simi = .2
                redText += "<span style=\"  background-color:#C0C0C0;\" >"
                redText += sent
                redText += "</span>"
        return redText ,len(sentances)

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
        self.total_Advanced_Count+=advancedCount
        return advancedCount

    def compositeCheck(self, text=''):
        compositeCount = 0
        List = ['while', 'when', 'because', 'if']
        sentances = self.spiltParagraph(text)
        for sentance in sentances:
            for word in List:
                if word in sentance:
                    compositeCount += 1
        self.total_Composite_Count+=compositeCount
        return compositeCount

    def getOverAll_Score(self):
        text=self.introText+self.firstText+self.secondText+self.opinionText
        self.compositeCheck(text)
        self.advancedCheck(text)
        if self.total_Advanced_Count!=0 and self.total_Composite_Count!=0:
            self.total_Sentance_Score=9
        elif self.total_Advanced_Count == 0 and self.total_Composite_Count != 0:
            self.total_Sentance_Score = 7
        elif self.total_Advanced_Count != 0 and self.total_Composite_Count == 0:
            self.total_Sentance_Score = 7
        else:
            self.total_Sentance_Score=5
        allGrammar_Score=self.G_first+self.G_intro+self.G_second+self.G_opinion
        allSentanc_Count=self.total_Sentance_conut0+self.total_Sentance_conut1+self.total_Sentance_conut2+self.total_Sentance_conut3
        allLaxis_Score= self.L_first + self.L_intro + self.L_second + self.L_opinion
        self.total_Grammar_Score=allGrammar_Score/4
        self.total_Lexis_Score = allLaxis_Score / 4
        self.overAll_Score=(self.total_Lexis_Score+self.total_Grammar_Score+self.total_Sentance_Score)/3


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
        self.final_Resulat_Coherence.clear()
        self.final_Result_Lexis.clear()
        self.final_Result_Grammer.clear()
        self.final_Result_OverallScore.clear()
        self.first_List, self.second_List, self.opinion_List, self.intro_List = [], [], [], []
        self.total_Sentance_conut0, self.total_Sentance_conut1, self.total_Sentance_conut2, self.total_Sentance_conut3 = 0, 0, 0, 0
        self.G_first,self.L_first = 9, 9
        self.G_second, self.L_second = 9, 9
        self.G_opinion, self.L_opinion = 9, 9
        self.G_intro, self.L_intro = 9, 9
        self.firstText, self.introText, self.secondText, self.opinionText = '', '', '', ''
        self.total_Advanced_Count, self.total_Composite_Count = 0, 0
        self.total_Grammar_Score = 0
        self.total_Lexis_Score = 0
        self.total_Sentance_Score = 0
        self.text_General=''
        self.overAll_Score=0


app=QApplication(sys.argv)
widget=Ilets()
widget.show()
sys.exit(app.exec_())
