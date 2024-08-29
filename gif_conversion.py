"""
Handles most of the logic for converting a GIF to a series of frames for the Arduino Uno R4 Wifi LED matrix.
"""

import cv2
import os
import shutil

def extract_frames(input_video: str, output_folder: str):
    """
Extracts the frames from the gif and puts them in a temporary folder.
    """
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
    """
Gets all the names of the files in the given folder. Used to get all the gif frames.
    """
    gifFrames = os.listdir(folder)
    return gifFrames

def create_frame_array(frames: list):
    """
Automatically generates a C++ array of frames generated by the program.
    """
    arrayBeginning = "\nconst uint32_t* frames[] = {"
    frameArray = arrayBeginning
    frameArray += ", ".join(frames)
    return frameArray + "};"

def delete_folder(folder: str):
    """
Deletes the given folder. Used to remove the temporary folder from the file tree.
    """
    try:
        shutil.rmtree(folder)
    except OSError as error:
        print(f"Error: {error.filename} - {error.strerror}")
