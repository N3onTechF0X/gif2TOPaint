from PIL import Image, ImageSequence
import json
import math


def main(path):
    image = Image.open(path)
    frame_width, frame_height = 128, 128
    frames = [
        frame.resize((frame_width, frame_height), Image.LANCZOS).convert("RGB")
        for i, frame in enumerate(ImageSequence.Iterator(image))
        if i % 1 == 0
    ]
    num_frames = len(frames)
    durations = [frame.info.get('duration') for frame in ImageSequence.Iterator(image)]
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
