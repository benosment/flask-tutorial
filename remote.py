import flask, flask.views
import os
from util import login_required

class Remote(flask.views.MethodView):
  @login_required
  def get(self):
    return flask.render_template('remote.html')

  @login_required
  def post(self):
    result = eval(flask.request.form['expression'])  # from html name of field in form
    flask.flash(result)
    return flask.redirect(flask.url_for('remote'))
