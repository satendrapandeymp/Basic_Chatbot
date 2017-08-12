import re, os
from update import update, remove, train
from glob import glob
from language import improve
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def preprocessing(user_name):

	# to remove existing files
	remove(user_name)

	# Opening file for reading
	path_mess = 'message/' + user_name + '/messages.htm'
	read_from = open(path_mess,'r')

	# Reading from processed Raw File
	raw = read_from.read()
	read_from.close()

	# Splitting to get useful data
	split = re.split('<p>',raw)

	flag = 0
	temp = ""

	for msg in split:
		if (flag == 0):
			raw_user = re.split('<span class="user">',msg)[1]
			last = re.split('&',raw_user)[0]
			check = re.split(' ',last)
			if (len(check) > 2):
				last = check[0]
			flag = 1
		else:
			messages = re.split('</p>',msg)
			message = messages[0]
			un = re.split('&',message)
			if (message != '' and len(un) ==1):
				# For getting user
				Detail = messages[1]
				raw_user = re.split('<span class="user">',Detail)
				if (len(raw_user)>1):
					raw_user = raw_user[1]
					user = re.split('&',raw_user)[0]
					check = re.split(' ',user)
					if (len(check) > 2):
						user = check[0]
						print last
						doc = "aiml/"+ user_name + "/Temp/" + last + ".aiml"
					else:
						doc = "aiml/"+ user_name + "/Temp/" + last + ".aiml"

					if (user == user_name):
						if (last != user_name):
							output = open(doc,'a')
							message = improve(message)
							output.write("<category> "+'<pattern>'+ message.upper() +'</pattern> ' + "<template>" + temp + "</template>"+"</category>"+"\n")
							output.close()
						else:
							a = 2
					else:
						if (user == last):
							temp = temp + message + "*"
						else:
							temp = message
					last = user
	# to make proper files
	update(user_name)
	train(user_name)
