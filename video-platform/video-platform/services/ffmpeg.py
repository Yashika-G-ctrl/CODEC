import os
import subprocess
import uuid
from .s3 import upload_file
def create_hls_and_thumbnail(local_path, title):
base = str(uuid.uuid4())
out_dir = os.path.join('uploads', base)
os.makedirs(out_dir, exist_ok=True)
# Thumbnail
thumb_path = os.path.join(out_dir, 'thumb.jpg')
subprocess.run([
    'ffmpeg', '-i', local_path,
    '-ss', '00:00:01.000', '-vframes', '1', thumb_path
], check=True)
upload_file(thumb_path, f"{base}/thumb.jpg",
            extra={'ContentType': 'image/jpeg'})

# Multi-resolution HLS
playlist_path = os.path.join(out_dir, 'playlist.m3u8')
subprocess.run([
    'ffmpeg', '-i', local_path,
    '-profile:v', 'main', '-preset', 'fast',
    '-bf', '1', '-keyint_min', '120', '-g', '120',
    '-sc_threshold', '0',
    '-b:v:0', '800k',  '-s:v:0', '854x480',
    '-b:v:1', '1400k', '-s:v:1', '1280x720',
    '-b:v:2', '2800k', '-s:v:2', '1920x1080',
    '-map', '0:v', '-map', '0:a',
    '-var_stream_map', 'v:0,a:0 v:1,a:0 v:2,a:0',
    '-master_pl_name', 'playlist.m3u8',
    '-f', 'hls', '-hls_time', '4', '-hls_playlist_type', 'vod',
    '-hls_segment_filename', os.path.join(out_dir, 'v%v_%03d.ts'),
    playlist_path
], check=True)

# Upload everything to S3
for f in os.listdir(out_dir):
    local = os.path.join(out_dir, f)
    key = f"{base}/{f}"
    ctype = 'application/x-mpegURL' if f.endswith('.m3u8') else \
            'video/mp2t' if f.endswith('.ts') else 'image/jpeg'
    upload_file(local, key, extra={'ContentType': ctype})

return base   # folder key (UUID)
