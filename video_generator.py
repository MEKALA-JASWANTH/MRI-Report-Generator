from PIL import Image, UnidentifiedImageError
import numpy as np
import os
import imageio_ffmpeg as ffmpeg

# Set FFmpeg environment variable before importing moviepy
os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg.get_ffmpeg_exe()

from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
from moviepy.config import change_settings

# Also set it via moviepy config
change_settings({"FFMPEG_BINARY": ffmpeg.get_ffmpeg_exe()})

def generate_video():
    images_folder = 'images'
    audio_file = 'static/summary.mp3'

    image_files = sorted([
        os.path.join(images_folder, img)
        for img in os.listdir(images_folder)
        if img.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))
    ])

    num_images = len(image_files)
    if num_images == 0:
        raise Exception("No images found in the folder.")

    print(f"\nFound {num_images} images to process...")

    audio = AudioFileClip(audio_file)
    audio_duration = audio.duration

    valid_clips = []
    image_duration = audio_duration / num_images

    print(f"Audio duration: {audio_duration:.2f}s, Each image: {image_duration:.2f}s\n")

    for img_path in image_files:
        try:
            # Open and convert image to RGB
            img_pil = Image.open(img_path).convert('RGB')

            # Resize to 1280x720 - USE LANCZOS (not ANTIALIAS)
            img_pil = img_pil.resize((1280, 720), Image.Resampling.LANCZOS)

            # Convert to numpy array
            img_np = np.array(img_pil)

            # Create clip with duration
            clip = ImageClip(img_np).set_duration(image_duration)
            valid_clips.append(clip)
            print(f"✓ Added: {os.path.basename(img_path)}")
            
        except UnidentifiedImageError:
            print(f"✗ Skipped invalid image: {img_path}")
        except AttributeError:
            # Fallback for even older Pillow versions
            try:
                img_pil = Image.open(img_path).convert('RGB')
                img_pil = img_pil.resize((1280, 720))
                img_np = np.array(img_pil)
                clip = ImageClip(img_np).set_duration(image_duration)
                valid_clips.append(clip)
                print(f"✓ Added (fallback): {os.path.basename(img_path)}")
            except Exception as e:
                print(f"✗ Error: {img_path}: {e}")
        except Exception as e:
            print(f"✗ Error: {img_path}: {e}")

    if not valid_clips:
        raise Exception("No valid images found to create a video.")

    print(f"\n✓ Successfully processed {len(valid_clips)} images")
    print("Concatenating clips...")
    
    video = concatenate_videoclips(valid_clips, method="compose")

    # Attach audio
    print("Attaching audio...")
    video = video.set_audio(audio)
    video = video.set_duration(audio.duration)

    # Write video file
    output_path = "static/output_video.mp4"
    print(f"Writing video to {output_path}...")

    video.write_videofile(
        output_path,
        fps=24,
        codec='libx264',
        audio_codec='aac',
        verbose=True,
        logger='bar'
    )

    print(f"\n✅ Video created successfully: {output_path}")

    # Clean up images folder
    print("Cleaning up images folder...")
    folder = 'images'
    if os.path.exists(folder):
        for f in os.listdir(folder):
            file_path = os.path.join(folder, f)
            if os.path.isfile(file_path):
                os.remove(file_path)

    return output_path
