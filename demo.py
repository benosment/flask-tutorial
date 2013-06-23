import flask, flask.views
import os
import functools


app = flask.Flask(__name__)
app.secret_key = 'demo'

users = {'ben':'pass'}

class Main(flask.views.MethodView):
  def get(self):
    return flask.render_template('index.html')

  def post(self):
    if 'logout' in flask.request.form:
      flask.session.pop('username', None)
      return flask.redirect(flask.url_for('index'))
    required = ['username', 'password']
    for r in required:
      if r not in flask.request.form:
        flask.flash("Error: {0} is required.".format(r))
        return flask.redirect(flask.url_for('index'))
    username = flask.request.form['username']
    password = flask.request.form['password']
    if username in users and users[username] == password:
      flask.session['username'] = username
    else:
      flask.flash("Username does not exist or incorrect password")
    return flask.redirect(flask.url_for('index'))

def login_required(f):
  @functools.wraps(f)
  def wrapper(*args, **kwargs):
    if 'username' in flask.session:
      return f(*args, **kwargs)
    else:
      flask.flash("A login is required to see this page!")
      return flask.redirect(flask.url_for('index'))
  return wrapper

class Remote(flask.views.MethodView):
  @login_required
  def get(self):
    return flask.render_template('remote.html')

  @login_required
  def post(self):
    result = eval(flask.request.form['expression'])  # from html name of field in form
    flask.flash(result)
    return flask.redirect(flask.url_for('remote'))

class Music(flask.views.MethodView):
  @login_required
  def get(self):
    songs = os.listdir('static/music')
    return flask.render_template('music.html', songs=songs)


app.add_url_rule('/',
                 view_func=Main.as_view('index'),
                 methods=['GET', 'POST'])

app.add_url_rule('/remote/',
                 view_func=Remote.as_view('remote'),
                 methods=['GET', 'POST'])

app.add_url_rule('/music/',
                 view_func=Music.as_view('music'),
                 methods=['GET'])

app.debug = True
app.run()
