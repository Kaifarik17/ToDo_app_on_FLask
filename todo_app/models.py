from flask_login import UserMixin

import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, \
    check_password_hash
from typing import Optional
from datetime import datetime, timezone

from todo_app import db, login_manager


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    email: so.Mapped[int] = so.mapped_column(sa.String(64), index=True, 
                                            unique=True, nullable=False)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(256),
                                                    nullable=False,
                                                    index=True)
    
    tasks: so.WriteOnlyMapped['Task'] = so.relationship(back_populates='author')

    
    def __repr__(self):
        return f'<User: id={self.id}; email={self.email}'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class Task(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                             nullable=False)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256),
                                                             index=True)
    created_at: so.Mapped[datetime] = so.mapped_column(index=True,
                                default=lambda: datetime.now(timezone.utc))
    completed: so.Mapped[bool] = so.mapped_column(default=False)

    user_id: so.Mapped[User] = so.mapped_column(sa.ForeignKey(User.id),
                                                index=True)
    
    author: so.Mapped['User'] = so.relationship(back_populates='tasks')


    def __repr__(self):
        return f'Post: id={self.id}; title={self.title}'