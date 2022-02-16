from celery import Celery
import subprocess

celery_app = Celery('tasks', broker='redis://localhost:6379/0',
                    backend='redis://localhost:6379/0')


@celery_app.task
def take_thumbnail(video_input_path: str, img_output_path: str) -> None:
    try:
        proc = subprocess.Popen(['ffmpeg', '-i', video_input_path, '-ss', '00:00:00.000', '-vframes', '1', img_output_path],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.wait()
        (stdout, stderr) = proc.communicate()
    except subprocess.CalledProcessError as err:
        raise Exception(f'take_thumbnail: failed {str(err)}')


@celery_app.task
def video_manipulation_done(*args, **kwargs):
    # check for next video manipulation in db
    # next_video_manipulation.apply_async('arg1', 'arg2', link=done.s())
    print('ok')
