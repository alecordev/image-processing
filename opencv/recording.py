import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import cv2

def create_recordings_dir(base_dir="recordings"):
    date_str = datetime.now().strftime('%Y%m%d')
    dir_path = Path(base_dir) / date_str
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path

def record_video(resolution=(640, 480), format="avi", codec="XVID", threshold=500, duration_no_movement=60, output_dir="recordings"):
    cap = cv2.VideoCapture(0)
    cap.set(3, resolution[0])
    cap.set(4, resolution[1])
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    frame_size = (frame_width, frame_height)
    fourcc = cv2.VideoWriter_fourcc(*codec)
    movement_detected = False
    last_movement_time = 0
    recording = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (21, 21), 0)
        if 'prev_frame' in locals():
            diff = cv2.absdiff(prev_frame, blurred)
            _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
            movement_detected = cv2.countNonZero(thresh) > threshold

        prev_frame = blurred

        if movement_detected:
            last_movement_time = time.time()
            if not recording:
                dir_path = create_recordings_dir(output_dir)
                output_path = dir_path / f"{datetime.now().strftime('%H%M%S')}.{format}"
                out = cv2.VideoWriter(str(output_path), fourcc, 20.0, frame_size)
                recording = True

        if recording:
            out.write(frame)
            if time.time() - last_movement_time > duration_no_movement:
                out.release()
                recording = False

        cv2.imshow('Camera', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    if recording:
        out.release()
    cap.release()
    cv2.destroyAllWindows()

def take_screenshots(interval=5, duration=60, resolution=(640, 480), output_dir="recordings"):
    cap = cv2.VideoCapture(0)
    cap.set(3, resolution[0])
    cap.set(4, resolution[1])
    end_time = time.time() + duration

    while time.time() < end_time:
        ret, frame = cap.read()
        if not ret:
            break
        dir_path = create_recordings_dir(output_dir)
        file_path = dir_path / f"screenshot_{datetime.now().strftime('%H%M%S')}.jpg"
        cv2.imwrite(str(file_path), frame)
        time.sleep(interval)

    cap.release()

def apply_filters(frame, filters=[]):
    for filter_func in filters:
        frame = filter_func(frame)
    return frame


def low_light_photo(file_path="low_light.jpg", frames_quantity=30):
    cap = cv2.VideoCapture(0)

    max_width, max_height = 1920, 1080
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, max_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, max_height)

    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(f"Set resolution: {width}x{height}")

    frames = []
    for _ in range(frames_quantity):
        ret, frame = cap.read()
        if ret:
            frames.append(frame)

    if frames:
        avg_frame = np.mean(frames, axis=0).astype(np.uint8)  # Average frames for better image
        cv2.imwrite(str(file_path), avg_frame)

    cap.release()


def simple_record(output_dir="recordings", resolution=(1920, 1080), format="mp4", codec="mp4v", fps=60.0, duration=60):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])

    if True:
        cap.set(cv2.CAP_PROP_GAIN, 5)
        cap.set(cv2.CAP_PROP_FPS, 10)

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*codec)  # For example: 'XVID', 'mp4v', 'MJPG'
    dir_path = Path(output_dir) / datetime.now().strftime('%Y%m%d')
    dir_path.mkdir(parents=True, exist_ok=True)

    output_path = dir_path / f"{datetime.now(timezone.utc).strftime('%H%M%S')}.{format}"
    out = cv2.VideoWriter(str(output_path), fourcc, fps, (frame_width, frame_height))
    start_time = datetime.now()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Write the frame to the video file
        if True:
            pass
            # frame = cv2.fastNlMeansDenoising(frame, None, 30, 7, 21)
            # frame = cv2.GaussianBlur(frame, (5, 5), 0)
            # frame = cv2.convertScaleAbs(frame, alpha=1.5, beta=50)

        out.write(frame)

        # Display the frame
        cv2.imshow('Recording', frame)

        # Stop recording after the specified duration
        if (datetime.now() - start_time).seconds >= duration:
            break

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # record_video(resolution=(1280, 720), format="mp4", codec="mp4v", threshold=1000, duration_no_movement=120)
    # take_screenshots(interval=10, duration=120, resolution=(1280, 720))
    low_light_photo()
    simple_record()
