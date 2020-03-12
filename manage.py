from app import app, db
#from app.models import User, Questions, Answers
from app.models import User

@app.shell_context_processor
def make_shell_context():
    #return {'db': db, 'User': User, 'Questions': Questions, 'Answers': Answers}
    return {'db': db, 'User': User}
