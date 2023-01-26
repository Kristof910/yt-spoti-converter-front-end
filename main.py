from flask import Flask, request, redirect, render_template, session
import requests
import json
import threading

import setup

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def main():
    try:
        if(setup.spoti_client_id == "" or setup.spoti_client_secret == ""):
            raise Exception("setup.py is not filled")
        return render_template('index.html')
    except Exception as e:
        print(f"Ops, something gone wrong in main: {e}")
        return render_template('error.html')    

@app.route("/connect")
def connect():
    try:
        auth_url = f'https://accounts.spotify.com/authorize?client_id={setup.spoti_client_id}&response_type=code&redirect_uri=http://localhost:9874/callback&scope=playlist-modify-public user-read-private user-library-read'
        return redirect(auth_url)
    except Exception as e:
        print(f"Ops, something gone wrong in connect: {e}")
        return render_template('error.html')      

@app.route("/callback")
def callback():
    try:
        code = request.args.get('code')

        token_url = 'https://accounts.spotify.com/api/token'
        data = {'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': 'http://localhost:9874/callback'}
        auth = (setup.spoti_client_id, setup.spoti_client_secret)
        response = requests.post(token_url, data=data, auth=auth)
        access_token = response.json()['access_token']

        session['access_token'] = access_token
        return redirect('/nextstep')
    except Exception as e:
        print(f"Ops, something gone wrong in callback: {e}")
        return render_template('error.html')      

@app.route("/nextstep")
def nextstep():
    try:
        return render_template("nextstep.html")
    except Exception as e:
        print(f"Ops, something gone wrong in nextstep: {e}")
        return render_template('error.html')      

@app.route("/nextstep", methods=["POST"])
def yt_link():
    try:
        text = request.form['yt_link']
        
        processed_link = ""
        index = 0
        if (text[0] == ("h" or "H")) and (text[8] == ("y" or "Y")):
            index = 34
        elif text[0] == ("h" or "H"):
            index = 38
        elif text[0] == ("w" or "W"):
            index = 30
        elif text[0] == ("y" or "Y"):
            index = 26        
        while index < len(text):
            processed_link += text[index]
            index += 1

        session["yt_link"] = processed_link
        return redirect("/finalstep")
    except Exception as e:
        print(f"Ops, something gone wrong in yt_link: {e}")
        return render_template('error.html')      

@app.route("/finalstep")
def finalstep():
    try:
        headers = {
            "Authorization": "Bearer " + session["access_token"]
        }
        response = requests.get("https://api.spotify.com/v1/me", headers=headers)
        user_id = json.loads(response.text)["id"]

        info = {
            "yt_playlist" : session["yt_link"], 
            "spoti_token" : session["access_token"], 
            "spoti_user_id" : user_id
        }
        
        thread = threading.Thread(target=requests.post, args=("http://localhost:9873/endpoint",), kwargs={"json":info})
        thread.start()
        return render_template("finalstep.html")
        
    except Exception as e:
        print(f"Ops, something gone wrong in finalstep: {e}")
        return render_template('error.html')   

if __name__ == '__main__':
    app.run(host='localhost', port=9874)