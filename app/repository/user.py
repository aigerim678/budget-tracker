from typing import List

from app.database import Session
from app.models import User

def get_all_users(session: Session) -> List[User]:
    return session.query(User).all()

db = Session()
try:
    users = get_all_users(db)
    print(users)
finally:
    db.close()




