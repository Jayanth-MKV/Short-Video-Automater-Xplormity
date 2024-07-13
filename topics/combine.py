from moviepy.video.fx.all import crop
from moviepy.editor import VideoFileClip, concatenate_videoclips



def combine_videos(video_paths: list[str], max_duration: int, max_clip_duration: int,combined_video_path:str, threads: int):
  """
  Combines a list of videos into one video and returns the path to the combined video.

  Args:
      video_paths (List): A list of paths to the videos to combine.
      max_duration (int): The maximum duration of the combined video.
      max_clip_duration (int): The maximum duration of each clip.
      threads (int): The number of threads to use for the video processing.

  Returns:
      str: The path to the combined video.
  """


  # Required duration of each clip
  req_dur = max_duration / len(video_paths)

  print("[+] Combining videos...")
  print(f"[+] Each clip will be maximum {req_dur} seconds long.")

  clips = []
  tot_dur = 0
  # Add downloaded clips over and over until the duration of the audio (max_duration) has been reached
  while tot_dur < max_duration:
      for video_path in video_paths:
          clip = VideoFileClip(video_path)
          clip = clip.without_audio()
          # Check if clip is longer than the remaining audio
          if (max_duration - tot_dur) < clip.duration:
              clip = clip.subclip(0, (max_duration - tot_dur))
          # Only shorten clips if the calculated clip length (req_dur) is shorter than the actual clip to prevent still image
          elif req_dur < clip.duration:
              clip = clip.subclip(0, req_dur)
          # clip = clip.set_fps(30)

          # Not all videos are same size,
          # so we need to resize them
          if round((clip.w/clip.h), 4) < 0.5625:
              clip = crop(clip, width=clip.w, height=round(clip.w/0.5625), \
                          x_center=clip.w / 2, \
                          y_center=clip.h / 2)
          else:
              clip = crop(clip, width=round(0.5625*clip.h), height=clip.h, \
                          x_center=clip.w / 2, \
                          y_center=clip.h / 2)
          clip = clip.resize((1080, 1920))

          if clip.duration > max_clip_duration:
              clip = clip.subclip(0, max_clip_duration)

          clips.append(clip)
          tot_dur += clip.duration

  print("[+] Videos combined.")
  # Debug what is in clips
  print(clips)
  final_clip = concatenate_videoclips(clips)
  final_clip = final_clip.set_fps(30)
  print("[+] Set clip.")
  final_clip.write_videofile(combined_video_path, threads=8)

  print("[+] Final video created.")