from nltk.corpus import stopwords
from nltk import pos_tag
from nltk.tokenize import word_tokenize
import re

def improve(mess):

    # To remove Emoji    
    for lol in [':p', ';p' , '<3', ':D', ':O', ';)', ':]', ':[' , ':)', ':(' ]:
        mess = mess.replace(lol.upper(),"")
	mess = mess.replace(lol.lower(),"")

    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(mess)
    message = ""
    if len(mess.split(" ")) == 1:
        message = mess

    flag = 0

    pos = pos_tag(word_tokens)

    for w in pos:
        if w[1] in ['PRP$','VBP','IN','RB'] or w[0] == '?':
            if flag == 0:
                message = message + "* "
            flag = 1
        else:
            flag = 0
            message = message + w[0] + " "
    if message == "* ":
        message = mess
    return message
