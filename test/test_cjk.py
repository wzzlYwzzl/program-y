import sys
import os

sys.path.append('/Users/caoxiaojie/pythonCode/program-y/src')

from programy.dialog.tokenizer.cjk import CjkTokenizer

tokenizer = CjkTokenizer()
tokenizer.texts_to_words("(总市值,function) (大于,operator) (100,number) (股票,sector)")