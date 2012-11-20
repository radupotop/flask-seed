#!/usr/bin/python2.7

# http://flask.pocoo.org/docs/quickstart/
# http://flask.pocoo.org/docs/api/

from flask import Flask, request, json, jsonify, Response, abort, redirect, url_for
from flaskext.sqlalchemy import SQLAlchemy


# define app & config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/test'
db = SQLAlchemy(app)


# define our model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self,username,email):
        self.username = username
        self.email = email
        
    def __repr__(self):
        return '<User %r>' % self.username


# create
def create_db():
    db.create_all()
    db.session.commit()

def create_users():
    admin = User('admin', 'admin@example.org')
    guest = User('guest', 'guest@example.org')
    db.session.add(admin)
    db.session.add(guest)
    db.session.commit()


# define routes
@app.route('/')
def index():
    """API Help"""
    d = {
        'view':  {
            'uri': '/hello/<name>',
            'methods': ['GET']
        },
        'create': {
            'uri': '/create',
            'params': ['name', 'email'],
            'methods': ['POST']
        },
        'delete': {
            'uri': '/delete/<name>',
            'methods': ['DELETE', 'POST']
        }
    }
    return jsonify(d)
    
@app.route('/create', methods=['POST'])
def create():
    """Create user"""
    user = request.form['name']
    email = request.form['email']
    
    try:
        db.session.add(User(user, email))
        db.session.commit()
        d={'name': user, 'email': email}
    except:
        d={'error':'user exists'}
    
    return jsonify(d)
    
@app.route('/hello/<name>')
def hello(name):
    """Greet user"""
    try:
        user = User.query.filter_by(username=name).first()
        d = {
            'id': user.id,
            'user': user.username,
            'email': user.email
        }
    except:
        d={'error': 'user does not exist'}
    
    return jsonify(d)
    
@app.route('/delete/<name>', methods=['DELETE', 'POST'])
def delete(name):
    
    if request.method == 'POST':
        resp = {'status': 'Using POST'}
    else:
        resp = {'status': 'Using DELETE'}
    
    searchword = request.args.get('key', '')
    
    """Delete user"""
    #~db.session.delete(User).filter_by(username=name)
    #~db.session.commit()
    return jsonify(resp)
    
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    
    if request.method == 'POST':
        f = request.files['file']
        f.save('/tmp/newfile')
    
    return jsonify({'status':'uploaded'})
    
@app.route('/redirect', methods=['GET'])
def redirect_to():
    redirect(url_for('index'))


if __name__ == '__main__':
    app.debug = True
    app.run()
