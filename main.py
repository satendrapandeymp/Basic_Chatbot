from flask import Flask, render_template, request, jsonify, redirect, session
import aiml, os
from werkzeug import secure_filename
from pre import preprocessing as process
from auth import login_required, login, logout, register

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = 'message/'
app.secret_key = "weubfyiwobyfuw;elfuvyw;vy56243i38v8;evwf8fvywelu"

kernel = aiml.Kernel()

@app.route("/")
@login_required
def hello():
    return render_template('chat.html', user= session['user'])

@app.route("/train", methods=['GET','POST'])
@login_required
def train():
    if request.method == "POST":
        file = request.files['file']
        name = session['user']
        mess_folder = 'message/' + name
        if not os.path.exists(mess_folder):
            os.makedirs(mess_folder)
        path = "aiml/" + name + "/Temp"
        if not os.path.exists(path):
            os.makedirs(path)
        path1 = "aiml/" + name + "/XMLS"
        if not os.path.exists(path1):
            os.makedirs(path1)
        path2 = "aiml/" + name + "/brain"
        if not os.path.exists(path2):
            os.makedirs(path2)
        filename = secure_filename(file.filename)
        if filename == "messages.htm":
            app.config['UPLOAD_FOLDER'] = 'message/' + name + '/'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            process(name)
            return redirect('/')
        else:
            return ("Bad kind of filename, Kindly Upload your message.htm")
    else:
        return render_template('Train.html', user= session['user'])

@login_required
@app.route("/ask/<path:name>", methods=['POST'])
def ask(name):

    message = str(request.form['messageText'])

    user = session['user']

    if not os.path.isdir("aiml/"+  user):
        return jsonify({'status':'OK','answer': 'you need to train first'})
    filename = "aiml/"+  user +"/brain/" + name + ".brn"

    if os.path.isfile(filename):
        kernel.bootstrap(brainFile = filename)
    else:
        res = 'unknown user' + name
        return jsonify({'status':'OK','answer': res})

    if message == "quit":
        bot_response = "See you later " + name
    else:
        bot_response = kernel.respond(message)

    return jsonify({'status':'OK','answer':bot_response})

@app.route('/register', methods=['GET', 'POST'])
def do_register():
    return register()

@app.route('/login', methods=['GET', 'POST'])
def do_login():
    return login()

@app.route('/logout')
@login_required
def do_logout():
	return logout()

if __name__ == "__main__":
    app.run(debug=True)
