import json
import os
import random
from topics.ai import AI
from topics.audio import generate_subtitles
from topics.news import NEWS
from topics.stock import search_for_stock_videos
from topics.voice import tts
from util.const import DATA_PATH, NEWS_API_KEY, PEXELS_API,SCRIPT_PROMPT
from util.files import load_json, load_txt, make_dir, save_txt, save_video
from moviepy.audio.io.AudioFileClip import AudioFileClip
from topics.search import generate_metadata
from util.files import load_txt,save_metajson
from topics.youtube import upload_video
import re
def replace_AI_with_spaces(text):
    return re.sub(r'\bAI\b', 'Artificial Intelligence', text, flags=re.IGNORECASE)

def get_and_save_news_data(tp,save_to,logger):
  logger.info(f"current top topic's processing: '{tp}'")
  top_news: str = f"https://newsdata.io/api/1/news?apikey={NEWS_API_KEY}&q={tp} news&country=in,us&language=en&category=technology,education,science"

  logger.info(f"top news url: {top_news}")
  logger.info("-----------------------------")
  news = NEWS(top_news)
  logger.info(f"current top topic's processing: '{tp}'")
  news.getnews()
  logger.info(f"Obtained Response, Saving to {save_to}")
  news.logNews(save_to)
  logger.info(f"Saved to {save_to}")


def load_and_get_item(path,logger):
  logger.info(f"Loading Data From JSON at {path}")
  data = load_json(path)["result"]
  return data

def get_current_item(data,logger):
  logger.info("Current Data")
  current_data = data[2]
  for i in range(len(current_data)):
      d = data[i]
      if not d["keywords"] or "gadgets" in d["keywords"]:
          continue
      else:
          current_data = d
          break
  return current_data


def get_and_save_transcript(current_data,save_text_to,logger):
    logger.info("Generating AI Transcript For 1")
    llama = AI()
    ai_response = llama.ask_g4f(SCRIPT_PROMPT+"The context is as follows:"+json.dumps({
        "title":current_data["title"],
        "description":current_data["description"],
        "paragraphs":5
    }))
    ai_response = replace_AI_with_spaces(ai_response)
    save_txt(save_text_to,ai_response)
    logger.info(f"Generated AI Transcript, Saved at {save_text_to}")

def load_and_get_audio(transcript_path,save_audio_to,logger):
    logger.info(f"Loading script From txt at {transcript_path}")
    script = load_txt(transcript_path)
    logger.info("Generating Voice For script")
    tts(script, "en_uk_001", save_audio_to)
    logger.info(f"Saved Voice to {save_audio_to}")
    logger.info(f"Checking Voice duration")
    if not os.path.exists(save_audio_to):
        return False

    duration =  AudioFileClip(save_audio_to).duration
    while duration>56:
      print("[-] Final audio is too long. Trimming...")
      sc = "|".join(script.split("|")[:-1])
      tts(sc, "en_uk_001", save_audio_to)
      duration =  AudioFileClip(save_audio_to).duration
      logger.info(f"Updated Voice duration to {duration}")
    return True

      


def get_and_save_subtitles(logger,audio_path,save_subtitles_to):
    logger.info("Generating Subtitles For Audio")
    generate_subtitles(audio_path, "en",save_subtitles_to)
    logger.info(f"Subtitles Saved to {save_subtitles_to}")


def get_and_save_videos(logger,queries,save_videos_to):
    os.makedirs(save_videos_to, exist_ok=True)
    # queries.append("ai")
    
    for query in queries:
        logger.info(f"Getting Stock Videos for {query}")
        video_urls = search_for_stock_videos(query,PEXELS_API,5,10)
        logger.info(f"Got {len(video_urls)} Videos")
        
        # Save first video in urls to file system
        if len(video_urls)==0:
            logger.info("No Videos Found")
            break

        numbers = list(range(0,len(video_urls)))
        k=random.randint(1,2)
        selected_elements = random.sample(numbers, k)

        for index in selected_elements:
            video_url = video_urls[index]
            ext = video_url.split(".")[-1]
            save_video_to = f"{save_videos_to}/video_{query}_{index}.{ext}"
            logger.info(f"saving video url - {video_url}")
            save_video(logger,video_url,save_video_to)

    if len(os.listdir(save_videos_to))<3:
        return False

    return True


def get_and_save_metadata(logger,save_text_to,current_data,save_metadata_to):
    logger.info(f"Getting Video Metadata")
    script = load_txt(save_text_to)
    logger.info(f"Saving Metadata JSON")

    metadata = generate_metadata(current_data["description"],script)
    logger.info(f"Video Metadata: {metadata}")

    meta_json = {
        "title": metadata[0],
        "description": metadata[1],
        "keywords": metadata[2]
    }
    save_metajson(save_metadata_to,meta_json)
    logger.info(f"Saved Video Metadata")

def upload_data_to_youtube(logger,save_final_video_to,save_metadata_to,save_upload_to):
    logger.info(f"Loading metadata")
    metadata = load_json(save_metadata_to)
    logger.info(f"Video Uploading To Youtube")
    res = upload_video(save_final_video_to, title=metadata["title"], description=metadata["description"], category="22", keywords=metadata["keywords"], privacyStatus="private")
    logger.info(f"result saved To Youtube {save_upload_to}")
    save_metajson(save_upload_to,res)
    logger.info(f"Video Uploaded To Youtube {res}")