import flask, flask.views
import os
from util import login_required

class Music(flask.views.MethodView):
  @login_required
  def get(self):
    songs = os.listdir('static/music')
    return flask.render_template('music.html', songs=songs)


