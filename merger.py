from moviepy.editor import VideoFileClip, AudioFileClip

video = VideoFileClip("output_video.mp4")
audio = AudioFileClip("mri_summary.mp3").subclip(0, video.duration)

final = video.set_audio(audio)

final.write_videofile("merged_output.mp4", codec="libx264", audio_codec="aac", fps=24)
