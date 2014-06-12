# -*- coding: utf-8 -*-
from string import uppercase, lowercase


StyleData = {
    '123': [str(i) + '.' for i in range(1, 101)],
    '(1)(2)(3)': ['(' + str(i) + ').' for i in range(1, 101)],
    'Q1Q2Q3': ['Q' + str(i) + '.' for i in range(1, 101)],
    'ABC': [i + '.' for i in uppercase],
    'abc': [i + '.' for i in lowercase],
}

defaultQuestionNumStyle = '123'
defaultBranchNumStyle = 'ABC'


class NumStyle:
    def __init__(self, style):
        self.styleData = StyleData[style]

    def getNum(self, ord):
        if ord in range(0, len(self.styleData)):
            return self.styleData[ord]
        else:
            return "?"


