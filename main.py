import datetime
import os
import random

from moviepy.video.io.VideoFileClip import VideoFileClip

from common.func import get_and_save_news_data, get_and_save_subtitles, get_and_save_transcript, get_and_save_videos, get_current_item, load_and_get_audio, load_and_get_item,get_and_save_metadata,upload_data_to_youtube
from topics.video import CombineVideos
from topics.search import get_search_terms
from util.const import DATA_PATH, LOG_PATH,BRANDS, SONGS_PATH, CREDITS, PIXABAY_API
from util.logger import MultiLogger
from util.files import load_txt

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
from_date_str = yesterday.strftime('%Y-%m-%d')
to_date_str = today.strftime('%Y-%m-%d')
print(to_date_str)

os.makedirs(DATA_PATH, exist_ok=True)
os.makedirs(LOG_PATH, exist_ok=True)

logger = MultiLogger("AutoYT", LOG_PATH+"main.log").get_logger()

top_topics = ["ai"]
for tp in top_topics:
    folder = f"{DATA_PATH}/{to_date_str}_{tp}"
    
    if os.path.exists(folder) and len(os.listdir(folder))>6:
        logger.info(f"Videos Already Generated At {folder}")
        break

    save_to=f"{folder}/news_data.json"
    os.makedirs(folder,exist_ok=True)
    logger.info(os.listdir(folder))
    if not os.path.exists(save_to):
        get_and_save_news_data(tp,save_to,logger)
    
    data = load_and_get_item(save_to,logger)
    data_length = len(data)
    selected_elements = set()
    max_iterations = 10
    iteration_count = 0

    while len(selected_elements) < 5 and iteration_count < max_iterations:
        index = random.randint(0, data_length - 1)
        # index=22
        logger.info(f"selected index: {index}")
        if index not in selected_elements:
            current_data = data[index]
            title = current_data["title"]
            if any(brand.lower() in title.lower() for brand in BRANDS):
                continue
            selected_elements.add(index)

        iteration_count += 1
        index_folder=f"{folder}/{index}_{title.split()[0]}"

        logger.info(f"selected index folder: {index_folder}")
        
        if os.path.exists(f"{index_folder}") and len(os.listdir(index_folder))>6:
            print(os.listdir(index_folder))
            logger.info(f"Index Folder {index_folder} already exists")
            continue
        os.makedirs(f"{index_folder}", exist_ok=True)
        
        # current_data = get_current_item(data,logger)
        
        save_text_to=f"{index_folder}/text_{tp}.txt"

        if not os.path.exists(save_text_to):
            try:
                get_and_save_transcript(current_data,save_text_to,logger)
            except:
                logger.info("Error Obtaining Transcript")
                break
        
        save_videos_to=f"{index_folder}/videos"
        
        if not os.path.exists(save_videos_to):
            script = load_txt(save_text_to)
            st = get_search_terms(current_data["title"],3,script)
            retries = 1

            query = st            
            logger.info(f"Query: {query}")
            while retries <= 3 and not get_and_save_videos(logger,query,save_videos_to):
                logger.info("Failed to get videos, trying again...")
                st = get_search_terms(current_data["title"],3,script)
                query = st
                retries +=1

        save_audio_to=f"{index_folder}/audio_{tp}.mp3"
        if not os.path.exists(save_audio_to):
            if not load_and_get_audio(save_text_to,save_audio_to,logger):
                logger.info(f"Audio Not Saved at {save_audio_to}")
                break


        files = os.listdir(save_videos_to)
        video_urls = [f"{save_videos_to}/{f}" for f in files if f.endswith(".mp4")]
        logger.info(f"Found {len(video_urls)} videos")        
        
        # get srt
        save_subtitles_to=f"{index_folder}/subtitles_{tp}.srt"
        
        if not os.path.exists(save_subtitles_to):
            get_and_save_subtitles(logger,save_audio_to,save_subtitles_to)

        # combine video and audio
        save_combined_video_to=f"{index_folder}/combined_{tp}.mp4"
        save_final_video_to=f"{index_folder}/final_{tp}.mp4"

        bg_music_list = os.listdir(SONGS_PATH)
        bg_music = random.choice(bg_music_list)
        print(bg_music)
        bg_name = bg_music.split('.')[0].lower()
        credits = CREDITS.get(bg_name," ")
        bg_music_path = os.path.join(SONGS_PATH,bg_music)

        if not os.path.exists(save_final_video_to):
            CombineVideos(save_audio_to,save_subtitles_to,video_urls,save_combined_video_to,save_final_video_to,bg_music_path)

        # get metadata
        save_metadata_to=f"{index_folder}/metadata_{tp}.json"
        if not os.path.exists(save_metadata_to):
            get_and_save_metadata(logger,save_text_to,current_data,save_metadata_to,credits)
        
        logger.info(f"Got Video Metadata")
        break
       


    # save_upload_to=f"{index_folder}/upload_{tp}.json"
    # if not os.path.exists(save_upload_to):
    #     upload_data_to_youtube(logger,save_final_video_to,save_metadata_to,save_upload_to)
    # logger.info("Video Uploaded")


    