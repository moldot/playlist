from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Length, URL
from models import Playlist, Video
from utils import extract_ytid
from app import models

class FormCreatePlaylist(Form):
    id = StringField('id', validators=[DataRequired(), Length(min=6, max=50)])
    password = StringField('password', validators=[Length(max=50)])

    def validate(self):
        if not Form.validate(self):
            return False
        if models.Playlist.query.filter_by(id=id) != None:
            self.id.errors.append('Playlist id already in use')
            return False
        return True

class FormLogin(Form):
    password = StringField('password', validators=[Length(max=50)])

    def __init__(self, playlist):
        Form.__init__(self)
        self.playlist = playlist

    def validate(self):
        if not Form.validate(self):
            return False
        if self.password != self.playlist.password:
            self.password.errors.append('Password invalid')
            return False
        return True

class FormAddVideo(Form):
    url = StringField('url', validators=[URL()])

    def __init__(self, playlist):
        Form.__init__(self)
        self.playlist = playlist

    def validate(self):  # Cannot check if video exist on youtube
        if not Form.validate(self):
            return False
        if models.Video.query.filter_by(ytid=extract_ytid(str(self.url)), playlist_id=self.playlist.id).all():
            self.url.errors.append('Video already in the playlist')
            return False
        return True
