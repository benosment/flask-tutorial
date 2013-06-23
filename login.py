import flask, flask.views

users = {'ben':'pass'}

class Login(flask.views.MethodView):
  def get(self):
    return flask.render_template('login.html')

  def post(self):
    if 'logout' in flask.request.form:
      flask.session.pop('username', None)
      return flask.redirect(flask.url_for('login'))
    required = ['username', 'password']
    for r in required:
      if r not in flask.request.form:
        flask.flash("Error: {0} is required.".format(r))
        return flask.redirect(flask.url_for('login'))
    username = flask.request.form['username']
    password = flask.request.form['password']
    if username in users and users[username] == password:
      flask.session['username'] = username
    else:
      flask.flash("Username does not exist or incorrect password")
    return flask.redirect(flask.url_for('login'))

