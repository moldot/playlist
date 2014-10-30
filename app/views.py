from app import app, models, db
from flask import render_template, redirect, url_for, flash, g
from flask.ext.login import login_user, logout_user, current_user
from forms import *
from utils import *
import random

@app.before_request
def before_request():
    g.playlist = current_user

@app.route('/')
@app.route('/index')
def index():
    playlists = models.Playlist.query.all()
    return render_template('index.html', playlists=playlists)

@app.route('/play/<playlist_id>', methods=['GET', 'POST'])
@app.route('/play/<playlist_id>/<ytid>', methods=['GET', 'POST'])
def play(playlist_id, ytid=None):
    playlist = models.Playlist.query.filter_by(id=playlist_id).first()
    if playlist is None:
        flash('Playlist ' + str(playlist_id) + ' does not exist')
        return redirect(url_for('index'))

    videos = models.Video.query.filter_by(playlist_id=playlist_id).all()
    if ytid is None:
        if len(videos) > 0:
            video = random.choice(videos)
        else:
            video = None
    else:
        video = models.Video.query.filter_by(ytid=ytid, playlist_id=playlist_id).first()
        if video is None:
            video = {'ytid': ytid, 'data': get_video_data(ytid)}

    if False and not g.playlist.is_authenticated():
        loginForm = FormLogin(playlist)

        if loginForm.validate_on_submit():
            login_user(playlist)
            flash('Log in successfully. You can now edit ' + playlist_id + ' playlist')
            return redirect(url_for('play', playlist_id=playlist_id, ytid=ytid))
        else:
             return render_template('play.html', video=video, videos=videos, playlist=playlist, form=loginForm)
    else:
        addVideoForm = FormAddVideo(playlist)

        if addVideoForm.validate_on_submit():
            new_ytid = extract_ytid(str(addVideoForm.url))
            data = get_video_data(new_ytid)
            if data is None:
                flash('Invalid link')
                return redirect(url_for('play', playlist_id=playlist_id, ytid=ytid))
            else:
                new_video = models.Video(ytid=new_ytid, playlist_id=playlist_id)
                db.session.add(new_video)
                db.session.commit()
                flash('New vieo added to ' + str(playlist_id))
                return redirect(url_for('play', playlist_id=playlist_id, ytid=new_ytid))
        else: return render_template('play.html', video=video, videos=videos, playlist=playlist, form=addVideoForm)

@app.route('/remove_video/<playlist_id>/<ytid>')
def remove_video(playlist_id, ytid):
    playlist = models.Playlist.query.filter_by(id=playlist_id).first()
    if playlist is None:
        flash('Playlist ' + str(playlist_id) + ' does not exist')
        return redirect(url_for('index'))
    video = models.Video.query.filter_by(ytid=ytid, playlist_id=playlist_id).first()
    if video is None:
        flash('Video does not exist')
        return redirect(url_for('play', playlist_id=playlist_id))
    db.session.delete(video)
    db.session.commit()
    flash('Video removed successfully')
    return redirect(url_for('play', playlist_id=playlist_id))

