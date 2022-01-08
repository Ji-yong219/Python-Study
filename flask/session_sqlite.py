import os
import errno
import sqlite3
from uuid import uuid4
from pickle import dumps, loads
from collections import MutableMapping

from flask.sessions import SessionInterface, SessionMixin
from flask import Flask, session


class SqliteSession(MutableMapping, SessionMixin):
    
    _create_sql = (
        "CREATE TABLE IF NOT EXISTS session"
        "("
        "   key TEXT PRIMARY KEY,"
        "   val BLOB"
        ")"
    )
    _get_sql = "SELECT val FROM session WHERE key = ?"
    _set_sql = "REPLACE INTO session (key, val) VALUES (?, ?)"
    _del_sql = "DELETE FROM session WHERE key = ?"
    _ite_sql = "SELECT key FROM session"
    _len_sql = "SELECT COUT(*) FROM session"

    def __init__(self, directory, sid, *args, **kwargs):
        self.path = os.path.join(directory, sid)
        self.directory = directory
        self.sid = sid
        self.modified = False
        self.conn = None
        if not os.path.exists(self.path):
            with self._get_conn() as conn:
                conn.execute(self._create_sql)
                self.new = True

    def __getitem__(self, key):
        key = dumps(key, 0)
        rv = None
        with self._get_conn() as conn:
            for row in conn.execute(self._get_sql, (key,)):
                rv = loads(row[0])
                break
        if rv is None:
            raise KeyError("Key not in this session")
        return rv
    
    def __setitem__(self, key, value):
        key = dumps(key, 0)
        value = dumps(value, 2)
        with self._get_conn() as conn:
            conn.execute(self._set_sql, (key, value))
        self.modified = True

    def __delitem__(self, key):
        key = dumps(key, 0)
        with self._get_conn() as conn:
            conn.execute(self._del_sql, (key,))
        self.modified = True

    def __iter__(self):
        with self._get_conn() as conn:
            for row in conn.execute(self._ite_sql):
                yield loads(row[0])

    def __len__(self):
        with self._get_conn() as conn:
            for row in conn.execute(self._len_sql):
                return row[0]

    def _get_conn(self):
        if not self.conn:
            self.conn = sqlite3.Connection(self.path)
        return self.conn

    
    class CallableAttributeProxy(object):
        def __init__(self, session, key, obj, attr):
            self.session = session
            self.key = key
            self.obj = obj
            self.attr = attr

        def __call__(self, *args, **kwargs):
            rv = self.attr(*args, **kwargs)
            self.session[self.key] = self.obj
            return rv


    class PersistedObjectProxy(object):
        def __init__(self, session, key, obj):
            self.session = session
            self.key = key
            self.obj = obj

        def __getattr__(self, name):
            attr = getattr(self.obj, name)
            if callable(attr):
                return SqliteSession.CallableAttributeProxy(
                    self.session, self.key, self.obj, attr
                )
            return attr

    def setdefault(self, key, value):
        if key not in self:
            self[key] = value
            self.modified = True
        return SqliteSession.PersistedObjectProxy(
            self, key, self[key]
        )


class SqliteSessionInterface(SessionInterface):

    def __init__(self, directory):
        directory = os.path.abspath(directory)
        if not os.path.exists(directory):
            os.mkdir(directory)
        self.directory = directory

    def open_session(self, app, request):
        sid = request.cookies.get(app.session_cookie_name)
        if not sid:
            sid = str(uuid4())
        rv = SqliteSession(self.directory, sid)
        return rv

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        if not session:
            try:
                os.unlink(session.path)
            except OSError as e:
                if e.errno != errno.ENOENT:
                    raise
            if session.modified:
                response.delete_cookie(
                    app.session_cookie_name,
                    domain=domain
                )
            return

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
path = "/tmp/app_session"

if not os.path.exists(path):
    os.mkdir(path)
    os.chmod(path, int("700", 8))

app.session_interface = SqliteSessionInterface(path)
app.config.update(
    SECRET_KEY = "F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT",
    SESSION_COOKIE_NAME = "jpub_flask_session"
)

@app.route("/session_in")
def session_signin():
    session["test"] = "abc"

    return "Session SIgnin"

@app.route("/session_out")
def session_signout():
    session.clear()
    return "Session Signout"

@app.route("/session_stat")
def session_stat():
    print(session.get("test", "Empty Data"))
    return "Session Stat Print to Console"

app.run()