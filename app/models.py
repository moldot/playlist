from app import db
from datetime import datetime
from utils import get_video_data

class Playlist(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(50))
    videos = db.relationship('Video', backref='playlist', lazy='dynamic')

    def is_authenticated(self):
        return True

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ytid = db.Column(db.String(15), index=True)
    date_added = db.Column(db.DateTime)
    data = db.Column(db.PickleType)

    playlist_id = db.Column(db.String(50), db.ForeignKey('playlist.id'))
    #playlist = db.relationship('Playlist', backref='video', lazy='dynamic')

    def __init__(self, ytid, playlist_id, date_added=None):
        self.ytid = ytid
        if date_added is None:
            date_added = datetime.utcnow()
        self.date_added = date_added
        self.playlist_id = playlist_id
        self.data = get_video_data(ytid)

    def __repr__(self):
        return self.data['title']
