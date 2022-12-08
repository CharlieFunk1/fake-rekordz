from app import app, db
from app.models import User, Contact, Submit

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Contact': Contact, 'Submit': Submit}

