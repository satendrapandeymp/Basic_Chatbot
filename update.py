import re, os, aiml
from glob import glob

kernel = aiml.Kernel()

# Starting and ending common lines
start = '<?xml version="1.0" encoding="ISO-8859-1"?> \n <aiml version="1.0"> \n <!-- This program is open source code released under --> \n <!-- the terms of the GNU General Public License --> \n <!-- as published by the Free Software Foundation. --> \n <meta name="author" content="Satyendra Pandey"/> \n <meta name="language" content="en"/> \n'
middle = "<category> <pattern>*</pattern> <template> <random> <li>What's your favorite car? <br/> What kind of car do you drive?</li> <li>Do you get a lot of parking tickets? <br/> My favorite car is one with a driver.</li> </random> </template> </category>\n"
end = "\n"+"</aiml>"+"\n"

start1 = '<aiml version="1.0"> \n <!-- This category works with the standard AIML Set --> \n <category> \n <pattern>LOAD AIML B</pattern>  \n <template> \n <learn>'
end1 ='</learn> \n </template> </category> \n </aiml>'

# to format in proper json
def update(user_name):
    files = glob("aiml/" + user_name + "/Temp/*.*")
    for txtfile in files:
    	output = open(txtfile,'r')
    	raw = output.read()
    	output.close()
    	output = open("temp.txt",'w')
    	output.write(start)
        #output.write(middle)
    	output.write(raw)
    	output.write(end)
    	output.close()
    	os.rename("temp.txt", txtfile)
    	filename = re.split('/',txtfile)[3]
    	username = filename.split('.')[0]
        print username
    	name = "aiml/" + user_name + "/XMLS/" + username + '.xml'
    	output = open(name,'w')
    	output.write(start1)
    	output.write(txtfile)
    	output.write(end1)
    	output.close()

def remove(name):
    # Removing any file in temp folder
    files = glob("aiml/" + name + "/Temp/*.*")
    for txtfile in files:
    	os.remove(txtfile)

def train(name):
    files = glob("aiml/" + name + "/XMLS/*.*")
    for txtfile in files:
        kernel.bootstrap(learnFiles = os.path.abspath(txtfile), commands = "load aiml b")
        filename = re.split('/',txtfile)[3]
    	username = filename.split('.')[0]
        kernel.saveBrain("aiml/" + name + "/brain/" + username + ".brn" )
