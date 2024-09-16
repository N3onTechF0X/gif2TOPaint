from PIL import Image, ImageSequence
import json
import math
import os
import cv2


def process_image_frames(path, frame_width, frame_height):
    image = Image.open(path)
    frames = [
        frame.resize((frame_width, frame_height), Image.LANCZOS).convert("RGB")
        for i, frame in enumerate(ImageSequence.Iterator(image))
        if i % 1 == 0
    ]
    durations = [frame.info.get('duration') for frame in ImageSequence.Iterator(image)]
    return frames, durations


def process_video_frames(path, frame_width, frame_height):
    cap = cv2.VideoCapture(path)
    frames = []
    fps = cap.get(cv2.CAP_PROP_FPS)
    while True:
        ret, frame = cap.read()
        if not ret: break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(frame).resize((frame_width, frame_height), Image.LANCZOS)
        frames.append(frame)
    cap.release()
    return frames, [1000 // fps] * len(frames)


def main(path):
    frame_width, frame_height = 128, 128
    file_ext = os.path.splitext(path)[1].lower()

    if file_ext in ['.gif', '.webp']:
        frames, durations = process_image_frames(path, frame_width, frame_height)
    elif file_ext == '.mp4':
        frames, durations = process_video_frames(path, frame_width, frame_height)
    else:
        raise ValueError("Unsupported file format")

    num_frames = len(frames)
    fps = 1000 // (sum(durations) / len(durations)) if durations else 30
    side_length = math.ceil(math.sqrt(num_frames))
    image_width = frame_width * side_length
    image_height = frame_height * side_length

    stitched_image = Image.new("RGB", (image_width, image_height), color="black")
    for i, frame in enumerate(frames):
        x = (i % side_length) * frame_width
        y = (i // side_length) * frame_height
        stitched_image.paste(frame, (x, y))

    stitched_image.save("image.png", format="png", optimize=True)

    json_data = {
        "fps": fps,
        "frameHeight": frame_height,
        "frameWidth": frame_width,
        "imageHeight": image_height,
        "imageWidth": image_width,
        "numFrames": num_frames
    }

    with open("frame.json", 'w') as json_file:
        json.dump(json_data, json_file)


main(input("file: "))
