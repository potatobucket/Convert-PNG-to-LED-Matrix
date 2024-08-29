import cv2
import os
import shutil

def extract_frames(input_video: str, output_folder: str):
    cap = cv2.VideoCapture(input_video)
    frame_count = 0

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    fps = int(cap.get(cv2.CAP_PROP_FPS))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        frame_filename = os.path.join(output_folder, f"frame_{frame_count:04d}.png")
        cv2.imwrite(frame_filename, frame)
        print(f"Frame {frame_count} extracted!")

    cap.release()
    cv2.destroyAllWindows()

    return frame_count, fps

def get_files(folder: str):
    gifFrames = os.listdir(folder)
    return gifFrames

def delete_folder(folder: str):
    try:
        shutil.rmtree(folder)
    except OSError as error:
        print(f"Error: {error.filename} - {error.strerror}")
