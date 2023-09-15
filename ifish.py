from flask import Flask, render_template, redirect, url_for, request, session, flash

app = Flask(__name__)
app.secret_key = "MC426ifish"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        userEmail = request.form["loginEmail"]
        session["userEmail"] = userEmail
        return redirect(url_for("user"))
    else:
        return render_template("login.html")

@app.route("/user")
def user():
    if "userEmail" in session:
        userEmail = session["userEmail"]
        return f"<h1>{userEmail}</h1>"
    else:
        return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)