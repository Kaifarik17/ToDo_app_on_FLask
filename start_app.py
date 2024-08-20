import sqlalchemy as sa

from todo_app import create_app, db
from todo_app.models import User, Task


app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'db': db, 'User': User, 'Task': Task}