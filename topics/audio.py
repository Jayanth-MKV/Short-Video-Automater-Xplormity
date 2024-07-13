import assemblyai as aai
from moviepy.editor import AudioFileClip, VideoFileClip, concatenate_videoclips

from util.const import ASSEMBLY_AI_API_KEY


def generate_subtitles(audio_path: str, voice: str,output_path:str):
  """
  Generates subtitles from a given audio file and returns the path to the subtitles.
  """

  # Save subtitles
  subtitles_path = output_path

  if ASSEMBLY_AI_API_KEY is not None and ASSEMBLY_AI_API_KEY != "":
      print("[+] Creating subtitles using AssemblyAI")
      subtitles = __generate_subtitles_assemblyai(audio_path, voice)
  else:
      return "AssemblyAI API key not found"

  with open(subtitles_path, "w") as file:
      file.write(subtitles)


  print("[+] Subtitles generated.")



def __generate_subtitles_assemblyai(audio_path: str, voice: str) -> str:
  """
  Generates subtitles from a given audio file and returns the path to the subtitles.

  Args:
      audio_path (str): The path to the audio file to generate subtitles from.

  Returns:
      str: The generated subtitles
  """

  language_mapping = {
      "br": "pt",
      "id": "en", #AssemblyAI doesn't have Indonesian 
      "jp": "ja",
      "kr": "ko",
  }

  lang_code = language_mapping.get(voice, voice)
  aai.settings.api_key = ASSEMBLY_AI_API_KEY
  config = aai.TranscriptionConfig(language_code=lang_code)
  transcriber = aai.Transcriber(config=config)
  transcript = transcriber.transcribe(audio_path)
  try:
    subtitles = transcript.export_subtitles_srt(chars_per_caption=32)
  except Exception as e:
    subtitles = transcript.export_subtitles_srt()
    print(f"[-] Error generating subtitles: {e}")
    
  return subtitles


def match_video_to_audio(video_path, audio_path, output_path):
    # Load video and audio clips
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)

    # Get durations
    video_duration = video_clip.duration
    audio_duration = audio_clip.duration

    # Calculate how many times we need to repeat the video
    repeat_count = int(audio_duration // video_duration) + 1

    # Create a list of video clips to concatenate
    video_clips = [video_clip] * repeat_count

    # Concatenate the video clips
    final_video = concatenate_videoclips(video_clips)

    # Trim the final video to match the audio duration
    final_video = final_video.subclip(0, audio_duration)

    # Set the audio of the final video
    final_video = final_video.set_audio(audio_clip)

    # Write the output video file
    final_video.write_videofile(output_path, codec='libx264', audio_codec='aac')

# Example usage
# video_path = "input_video.mp4"
# audio_path = "input_audio.mp3"
# output_path = "output_video.mp4"

# match_video_to_audio(video_path, audio_path, output_path)
