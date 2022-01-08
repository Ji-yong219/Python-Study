from sqlalchemy import Column, Integer, String, BLOB
from database import Base, db_session

class FlaskSession(Base):
    __tablename__ = "flask_session"

    sid = Column(String, primary_key=True)
    value = Column(BLOB)

    @classmethod
    def change(cls, sid, value):
        rec = db_session.query(cls).filter(cls.sid == sid).first()
        if not rec:
            rec = cls()
            rec.sid = sid
        rec.value = value

        return rec
