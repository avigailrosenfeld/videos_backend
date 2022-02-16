from celery import Celery
import subprocess

celery_app = Celery('tasks', broker='redis://localhost:6379/0')


@celery_app.task
def take_thumbnail(video_input_path: str, img_output_path: str) -> None:
    try:
        proc = subprocess.Popen(['ffmpeg', '-i', video_input_path, '-ss', '00:00:00.000', '-vframes', '1', img_output_path],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess_flags)
        proc.wait()
        (stdout, stderr) = proc.communicate()
    except calledProcessError as err:
        raise Exception("take_thumbnail: Error ocurred: " + err.stderr)
