from flask import Flask, session
from uuid import uuid4
import pickle
from models import FlaskSession
from werkzeug.datastructures import CallbackDict
from flask.sessions import SessionInterface, SessionMixin
from database import db_session


class SQLAlchemySession(CallbackDict, SessionMixin):

    def __init__(self, initial=None, sid=None, new=False):
        def on_update(self):
            self.modified = True
        CallbackDict.__init__(self, initial, on_update)
        self.sid = sid
        self.new = new
        self.modified = False



class SQLAlchemySessionInterface(SessionInterface):
    session_class = SQLAlchemySession
    serializer = pickle

    def generate_sid(self):
        return str(uuid4())

    def open_session(self, app, request):
        sid = request.cookies.get(app.session_cookie_name)
        if not sid:
            sid = self.generate_sid()
            return self.session_class(sid=sid, new=True)
        rec = db_session.query(FlaskSession) \
                        .filter(FlaskSession.sid == sid).first()
        
        if rec is not None:
            data = self.serializer.loads(rec.value)
            return self.session_class(data, sid=sid)
        return self.session_calss(sid=sid, new=True)


    def save_session(self, app, sesion, response):
        domain = self.get_cookie_domain(app)
        if not session:
            rec = db_session\
                .query(FlaskSession)\
                .filter(FlaskSession.sid == session.sid)\
                .first()
            db_session.delete(rec)
            db_session.commit()
            if session.modified:
                response.delete_cookie(
                    app.session_cookie_name,
                    domain=domain
                )

            return
        val = self.serializer.dumps(dict(session))
        session_db = FlaskSession.change(session.sid, val)
        db_session.add(session_db)
        db_session.commit()

        httponly = self.get_cookie_httponly(app)
        secure = self.get_cookie_secure(app)
        expires = self.get_expiration_time(app, session)

        response.set_cookie(
            app.session_cookie_name,
            session.sid,
            expires=expires,
            httponly=httponly,
            domain=domain,
            secure=secure
        )

    
app = Flask(__name__)
app.session_interface = SQLAlchemySessionInterface()
app.config.update(
    SECRET_KEY="F12Zr47j\3yX R~X@HijmM]Lwf/m?KT",
    SESSION_COOKIE_NAME="jpub_flask_session"
)

@app.route("/session_in")
def session_signin():
    session["test"] = "abc"
    
    return "session Signin"

@app.route("/session_out")
def session_signout():
    session.clear()
    return "Session Signout"

@app.route("/session_stat")
def session_stat():
    print(session.get("test", "Empty Data"))
    return "Session Stat Print to Console"

app.run()
