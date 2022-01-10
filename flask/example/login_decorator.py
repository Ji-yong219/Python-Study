from functools import wraps
from flask import session, request, redirect, url_for, render_template

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user", None) is None:
            return redirect(url_for("login", next-request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/member")
@login_required
def member_page():
    return render_template("/member_page.html")
