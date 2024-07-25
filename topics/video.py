import os
import random

from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.io.VideoFileClip import VideoFileClip

from topics.combine import combine_videos
from util.const import get_settings
from util.const import TITLES,SIZE,COLORS,SUBSCRIBE_PATH
from util.text import format_text

from PIL import Image, ImageDraw
import numpy as np
from moviepy.video.fx.speedx import speedx
from moviepy.audio.fx.volumex import volumex


def generate_video(combined_video_path: str, tts_path: str, subtitles_path: str, threads: int, subtitles_position: str,final_video_path:str,bg_music_path:str):
  """
  This function creates the final video, with subtitles and audio.
  Returns:
      str: The path to the final video.
  """

  # PRINT STATE
  print("[+] Starting video generation...")
  globalSettings = get_settings()
  title = random.choice(TITLES)
  t=format_text(title, 20)
  wrapped_title = "\n".join(t)
  print(wrapped_title)
  size = (SIZE[0],SIZE[1]*0.15)

  comb = random.choice(COLORS)

  txt_clip = TextClip(wrapped_title,size=size,font=globalSettings["fontSettings"]["font"], fontsize = 100, color = comb['color'], bg_color=comb["bg_color"],stroke_color=comb["stroke_color"],stroke_width=5)
  # Get the Settings
  print("[+] Global Settings Obtained...",globalSettings["fontSettings"])
  # Make a generator that returns a TextClip when called with consecutive
  # generator = lambda txt: TextClip(txt,size=(800,None),font=globalSettings["fontSettings"]["font"], fontsize=globalSettings["fontSettings"]["fontsize"], color=globalSettings["fontSettings"]["color"], stroke_color=globalSettings["fontSettings"]["stroke_color"], stroke_width=globalSettings["fontSettings"]["stroke_width"])

  def generator(txt): 
    print(txt)
    t=format_text(txt, 16)
    title = "\n".join(t)
    return TextClip(title,size=(size[0]*0.8,SIZE[1]),font=globalSettings["fontSettings"]["sfont"], color=globalSettings["fontSettings"]["color"], stroke_color=globalSettings["fontSettings"]["stroke_color"], stroke_width=globalSettings["fontSettings"]["stroke_width"])

  # Split the subtitles position into horizontal and vertical
  horizontal_subtitles_position, vertical_subtitles_position = globalSettings["fontSettings"]["subtitles_position"].split(",")

  # if subtitle position is not the same as the setting and is not empty we override
  # if subtitles_position != globalSettings["fontSettings"]["subtitles_position"] and subtitles_position != "":
  # horizontal_subtitles_position, vertical_subtitles_position = subtitles_position.split(",")
  print("[+] Subtitles Position",subtitles_position)

  video_clip = VideoFileClip(combined_video_path)
  duration = video_clip.duration
  print("[+] Duration:",duration)



  # Burn the subtitles into the video
  subtitles = SubtitlesClip(subtitles_path, generator)
  txt_clip = txt_clip.set_position(("center","top")).set_duration(duration)
    
  subscribeMid = VideoFileClip("assets/subscribe.mp4")

  t = VideoFileClip("assets/talk.mp4").without_audio()
  talk = t.resize(width=300,height=300)


  # Create the rounded corner mask
  mask_size = (talk.w, talk.h)
  mask_radius = 100
  rounded_mask = create_rounded_rectangle_mask(mask_size, mask_radius)
  mask_clip = ImageClip(np.array(rounded_mask), ismask=True).set_duration(duration)  
  

  bg_audio = AudioFileClip(bg_music_path).fx(volumex,0.4)


  result = CompositeVideoClip([
      video_clip,
    #   txt_clip,
      talk.set_mask(mask_clip).set_position(("right","bottom")).set_duration(duration),
      subtitles.set_position((horizontal_subtitles_position, vertical_subtitles_position)),
      subscribeMid.set_position(("center","center")).set_start(duration),
  ])

  print("[+] Adding audio...")
  # Add the audio
  audio1 = AudioFileClip(tts_path)
  audio = CompositeAudioClip([
      audio1.fx(volumex,2),
      bg_audio.set_duration(duration),
  ])  
  
  result = result.set_audio(audio)
  
  if result.duration>60:
      print("[-] Final video is too long. Trimming...")
    #   result = result.set_duration(0, 60)
      result = speedx(result, 1.2)

  print("[+] Audio Done...")

  print("[+] Writing video...")
  video_name =final_video_path
  result.write_videofile(video_name, threads=8)



def CombineVideos(audio_path:str,subtitles_path:str,video_urls:list[str],combined_video_path:str,final_video_path:str,bg_music_path:str):
    temp_audio = AudioFileClip(audio_path)
    n_threads = 2

    if not os.path.exists(combined_video_path):
        combine_videos(video_urls, temp_audio.duration, 10,combined_video_path, n_threads or 2)

    print(f"[-] Next step: {combined_video_path}")
    # Put everything together
    subtitles_position="center"
    try:
        generate_video(combined_video_path, audio_path, subtitles_path, n_threads or 2, subtitles_position,final_video_path,bg_music_path)
    except Exception as e:
        print(f"[-] Error generating final video: {e}")



# Function to create a rounded corner mask
def create_rounded_rectangle_mask(size, radius):
    width, height = size
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([0, 0, width, height], radius=radius, fill=255)
    mask = np.array(mask) / 255.0
    return mask