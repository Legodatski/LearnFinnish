class Word:
    def __init__(self, finnish, english, sentance, answer_sentance, slide):
        self.finnish = finnish
        self.english = english
        self.sentance = sentance
        self.answer_sentance = answer_sentance
        self.slide = slide

    def lenght(self):
        output = 0

        if(self.finnish != "-" and self.finnish != None):
            output+=1

        if(self.english != "" and self.english != None):
            output+=1

        if(self.sentance != "" and self.sentance != None):
            output+=1

        if(self.answer_sentance != "" and self.answer_sentance != None):
            output+=1

        return output