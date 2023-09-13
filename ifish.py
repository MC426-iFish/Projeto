from flask import Flask

app = Flask(__name__)

@app.route("/login")
def login():
    return "<h1>Tela de Login</h1>"

if __name__ == "__main__":
    app.run()