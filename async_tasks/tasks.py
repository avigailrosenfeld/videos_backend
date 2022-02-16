from celery import Celery
import subprocess

celery_app = Celery('tasks', broker='redis://localhost:6379/0')


@celery_app.task
def take_thumbnail(video_input_path: str, img_output_path: str) -> None:
    try:
        subprocess.call(['ffmpeg', '-i', video_input_path, '-ss', '00:00:00.000', '-vframes', '1', img_output_path])
    except Exception:
        raise Exception('Take thumbnail failed')
