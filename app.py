from sqlalchemy.orm import sessionmaker
from flask import Flask, render_template
from models import Template, db_connect
from settings import DATABASE

app = Flask(__name__)
app.secret_key = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE

engine = db_connect()
Session = sessionmaker(bind=engine)
session = Session()


@app.route('/')
def index():
    templates = session.query(Template).all()
    return render_template('data.html', templates=templates)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7778, debug=True)
