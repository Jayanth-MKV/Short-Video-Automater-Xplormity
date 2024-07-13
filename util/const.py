import os
from dotenv import load_dotenv
load_dotenv(override=True)

NEWS_API_KEY: str = os.getenv('NEWSDATA_API')
NEWS_FETCH_LIMIT: int = 20
LOG_PATH: str = 'logs/'
DATA_PATH: str = 'YT/data'
SUBSCRIBE_PATH: str = "assets/subscribe.mp4"
PEXELS_API = os.getenv('PEXELS_API')
PIXABAY_API = os.getenv('PIXABAY_API')
ASSEMBLY_AI_API_KEY = os.getenv('ASSEMBLY_AI_API_KEY')
IMAGEMAGICK_BINARY = os.getenv('IMAGEMAGICK_BINARY')
SIZE=(1080,1920)
TITLE="What Happened in AI Today?"
TITLES = [
    "Latest Advances in AI Research",
    "Exploring AI Break throughs Today",
    "AI Innovations in Recent News",
    "New Trends in AI Technology",
    "How AI Is Changing Industries",
    "Key Developments in AI World",
    "AI Milestones Reached This Month",
    "Understanding AI Progress Now",
    "AI Transformations in 2024",
    "AI News Highlights for Today"
]

COLORS = [
{'color': 'black', 'bg_color': 'white', 'stroke_color': 'purple'},
{'color': 'white', 'bg_color': 'black', 'stroke_color': 'red'},
{'color': 'black', 'bg_color': 'white', 'stroke_color': 'green'},
{'color': 'white', 'bg_color': 'black', 'stroke_color': 'blue'},
{'color': 'black', 'bg_color': 'white', 'stroke_color': 'yellow'},
{'color': 'white', 'bg_color': 'black', 'stroke_color': 'orange'},
{'color': 'black', 'bg_color': 'white', 'stroke_color': 'purple'},
{'color': 'white', 'bg_color': 'black', 'stroke_color': 'red'},
{'color': 'black', 'bg_color': 'white', 'stroke_color': 'white'},
{'color': 'white', 'bg_color': 'black', 'stroke_color': 'orange'},
# {'color': 'black', 'bg_color': 'yellow', 'stroke_color': 'green'},
{'color': 'black', 'bg_color': 'white', 'stroke_color': 'blue'},
{'color': 'white', 'bg_color': 'black', 'stroke_color': 'yellow'},
{'color': 'black', 'bg_color': 'gray', 'stroke_color': 'purple'},
{'color': 'black', 'bg_color': 'black', 'stroke_color': 'white'},
# {'color': 'white', 'bg_color': 'lime', 'stroke_color': 'orange'},
{'color': 'black', 'bg_color': 'silver', 'stroke_color': 'cyan'},
# {'color': 'white', 'bg_color': 'maroon', 'stroke_color': 'navy'},
{'color': 'black', 'bg_color': 'aqua', 'stroke_color': 'gray'},
{'color': 'white', 'bg_color': 'teal', 'stroke_color': 'red'},
# {'color': 'black', 'bg_color': 'pink', 'stroke_color': 'yellow'}
]

SYSTEM_PROMPT="""
You are an expert YouTube Shorts script writer tasked with generating an engaging 30-second script based on the provided news article context. Your goal is to creatively summarize the key points in an entertaining way that will captivate viewers.
Generate a script that:

- Grabs viewer attention with an intriguing opening line
- Concisely explains the key points about the given topic. Make it short and crisp
- Provide only the script text, with no introductory or concluding remarks
- Is approximately 150 words long. Make it short and crisp
- Uses natural, conversational language suitable for a YouTube Short
- Strictly avoids greetings or farewells in the script
- Presents the script with lines separated by the | symbol to indicate pauses
"""

SCRIPT_PROMPT=""""
# Role: Video Script Generator

            ## Goals:
            Generate a script for a video, depending on the subject of the video.

            ## Constrains:
            1. the script is to be returned as a string with the specified number of paragraphs.
            2. do not under any circumstance reference this prompt in your response.
            3. get straight to the point, don't start with unnecessary things like, "welcome to this video".
            4. you must not include any type of markdown or formatting in the script, never use a title. 
            5. only return the raw content of the script with lines separated by the | symbol to indicate pauses.
            6. do not include "voiceover", "narrator" or similar indicators of what should be spoken at the beginning of each paragraph or line. 
            7. you must not mention the prompt, or anything about the script itself. also, never talk about the amount of paragraphs or lines. just write the script.
            8. respond in the same language as the video subject.
        Get straight to the point, don't start with unnecessary things like, "welcome to this video".
            YOU MUST NOT INCLUDE ANY TYPE OF MARKDOWN OR FORMATTING IN THE SCRIPT, NEVER USE A TITLE.
            ONLY RETURN THE RAW CONTENT OF THE SCRIPT. DO NOT INCLUDE "VOICEOVER", "NARRATOR" OR SIMILAR INDICATORS OF WHAT SHOULD BE SPOKEN AT THE BEGINNING OF EACH PARAGRAPH OR LINE. YOU MUST NOT MENTION THE PROMPT, OR ANYTHING ABOUT THE SCRIPT ITSELF. ALSO, NEVER TALK ABOUT THE AMOUNT OF PARAGRAPHS OR LINES. JUST WRITE THE SCRIPT.
"""

# top_news: str = "https://newsdata.io/api/1/news?apikey=" + NEWS_API_KEY + "&q=" + tp + "&language=en&category=top"
# top_news: str = f'https://newsapi.org/v2/everything?q=apple&from={from_date_str}&to={to_date_str}&sortBy=popularity&apiKey={NEWS_API_KEY}'

fontSettings = {
  "font": "assets/bold_font.ttf",
  "sfont": "assets/Afont.otf",
  "fontsize": 100,
  "color": "#FFFF00",
  "stroke_color": "black",
  "stroke_width": 5,
  "subtitles_position": "center,center",
}


scriptSettings = {
  "defaultPromptStart":
      """
          # Role: Video Script Generator

          ## Goals:
          Generate a script for a video, depending on the subject of the video.

          ## Constrains:
          1. the script is to be returned as a string with the specified number of paragraphs.
          2. do not under any circumstance reference this prompt in your response.
          3. get straight to the point, don't start with unnecessary things like, "welcome to this video".
          4. you must not include any type of markdown or formatting in the script, never use a title. 
          5. only return the raw content of the script. 
          6. do not include "voiceover", "narrator" or similar indicators of what should be spoken at the beginning of each paragraph or line. 
          7. you must not mention the prompt, or anything about the script itself. also, never talk about the amount of paragraphs or lines. just write the script.
          8. respond in the same language as the video subject.

      """ ,
  "defaultPromptEnd":
      """
          Get straight to the point, don't start with unnecessary things like, "welcome to this video".
          YOU MUST NOT INCLUDE ANY TYPE OF MARKDOWN OR FORMATTING IN THE SCRIPT, NEVER USE A TITLE.
          ONLY RETURN THE RAW CONTENT OF THE SCRIPT. DO NOT INCLUDE "VOICEOVER", "NARRATOR" OR SIMILAR INDICATORS OF WHAT SHOULD BE SPOKEN AT THE BEGINNING OF EACH PARAGRAPH OR LINE. YOU MUST NOT MENTION THE PROMPT, OR ANYTHING ABOUT THE SCRIPT ITSELF. ALSO, NEVER TALK ABOUT THE AMOUNT OF PARAGRAPHS OR LINES. JUST WRITE THE SCRIPT.
      """
}



def get_settings() -> dict:
  """
  Return the global settings  
  The script settings are:
      defaultPromptStart: Start of the prompt
      defaultPromptEnd: End of the prompt
  The Subtitle settings are:
      font: font path,
      fontsize: font size,
      color: Hexadecimal color,
      stroke_color: color of the stroke,
      stroke_width: Number of pixels of the stroke
      subtitles_position: Position of the subtitles
  """
  # Return the global settings
  return {
      "scriptSettings": scriptSettings,
      "fontSettings": fontSettings
  }