from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, current_user
from flask_migrate import Migrate
from models import db, User, Video
from services.ffmpeg import create_hls_and_thumbnail
import os
import threading
app = Flask(name)
app.config.from_object('config.Config')
db.init_app(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
with app.app_context():
db.create_all()
@login.user_loader
def load_user(user_id):
return User.query.get(int(user_id))
@app.route('/register', methods=['GET', 'POST'])
def register():
if request.method == 'POST':
u = User(username=request.form['username'],
password=generate_password_hash(request.form['password']))
db.session.add(u)
db.session.commit()
flash('Registered!')
return redirect(url_for('login'))
return render_template('login.html', mode='register')
@app.route('/login', methods=['GET', 'POST'])
def login():
if request.method == 'POST':
u = User.query.filter_by(username=request.form['username']).first()
if u and check_password_hash(u.password, request.form['password']):
login_user(u)
return redirect(url_for('dashboard'))
flash('Invalid credentials')
return render_template('login.html', mode='login')
@app.route('/dashboard')
@login_required
def dashboard():
return render_template('dashboard.html', videos=current_user.videos)
@app.route('/upload', methods=['POST'])
@login_required
def upload():
f = request.files['video']
if not f:
flash('No file selected')
return redirect(url_for('dashboard'))
os.makedirs('uploads', exist_ok=True)
tmp_path = os.path.join('uploads', f.filename)
f.save(tmp_path)

v = Video(title=request.form['title'],
          description=request.form['description'],
          filename=f.filename,
          owner=current_user,
          status='processing')
db.session.add(v)
db.session.commit()

def background():
    try:
        folder = create_hls_and_thumbnail(tmp_path, v.title)
        v.s3_key = folder
        v.status = 'ready'
        v.thumbnail = f"{folder}/thumb.jpg"
        db.session.commit()
    except Exception as e:
        v.status = 'failed'
        db.session.commit()
        raise e
    finally:
        os.remove(tmp_path)

threading.Thread(target=background).start()
flash('Upload queued!')
return redirect(url_for('dashboard'))
@app.route('/watch/int:video_id')
@login_required
def watch(video_id):
v = Video.query.get_or_404(video_id)
from services.s3 import generate_presigned_url
playlist_url = generate_presigned_url(f"{v.s3_key}/playlist.m3u8")
thumb_url    = generate_presigned_url(v.thumbnail)
return render_template('player.html', video=v, playlist_url=playlist_url, thumb_url=thumb_url)
if name == 'main':
app.run(debug=True)
