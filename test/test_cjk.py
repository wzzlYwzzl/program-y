import sys
import os

sys.path.append('/Users/caoxiaojie/pythonCode/program-y/src')

from programy.dialog.tokenizer.cjk import CjkTokenizer

tokenizer = CjkTokenizer()
words = tokenizer.texts_to_words("(*,func*)(*,operator)(*,number)(*,sector)")
print(words)