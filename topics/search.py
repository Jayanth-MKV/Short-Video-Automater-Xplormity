from topics.ai import AI
import json
import re

def get_search_terms(video_subject: str, amount: int, script: str) -> list[str]:
    """
    Generate a JSON-Array of search terms for stock videos,
    depending on the subject of a video.

    Args:
        video_subject (str): The subject of the video.
        amount (int): The amount of search terms to generate.
        script (str): The script of the video.
        ai_model (str): The AI model to use for generation.

    Returns:
        List[str]: The search terms for the video subject.
    """

    # Build prompt
    prompt = f"""
    # Role: Video Search Terms Generator
    ## Goals:
    Generate {amount} search terms for stock videos, depending on the subject of a video.

    ## Constrains:
    1. the search terms are to be returned as a json-array of strings.
    2. each search term should consist of 1-3 words, always add the main subject of the video.
    3. you must only return the json-array of strings. you must not return anything else. you must not return the script.
    4. the search terms must be related to the subject of the video.
    5. reply with english search terms only.

    ## Output Example:
    ["search term 1", "search term 2", "search term 3","search term 4","search term 5"]
    
    ## Context:
    ### Video Subject
    {video_subject}

    ### Video Script
    {script}

    Please note that you must use English for generating video search terms; Chinese is not accepted.
    """.strip()


    # Let user know
    print(f"Generating {amount} search terms for {video_subject}...")
    g4f = AI()
    # Generate search terms
    response = g4f.ask_g4f(prompt)

    # Let user know
    print(f"Response: {response}")
    # Parse response into a list of search terms
    search_terms = []
    
    try:
        search_terms = json.loads(response)
        if not isinstance(search_terms, list) or not all(isinstance(term, str) for term in search_terms):
            raise ValueError("Response is not a list of strings.")

    except (json.JSONDecodeError, ValueError):
        print("[*] GPT returned an unformatted response. Attempting to clean...")

        # Attempt to extract list-like string and convert to list
        match = re.search(r'\["(?:[^"\\]|\\.)*"(?:,\s*"[^"\\]*")*\]', response)
        if match:
            try:
                search_terms = json.loads(match.group())
            except json.JSONDecodeError:
                print("[-] Could not parse response.")
                return []



    # Let user know
    print(f"\nGenerated {len(search_terms)} search terms: {', '.join(search_terms)}")

    # Return search terms
    return search_terms



def generate_metadata(video_subject: str, script: str) -> tuple[str, str, list[str]]:  
    """  
    Generate metadata for a YouTube video, including the title, description, and keywords.  
  
    Args:  
        video_subject (str): The subject of the video.  
        script (str): The script of the video.  
        ai_model (str): The AI model to use for generation.  
  
    Returns:  
        Tuple[str, str, List[str]]: The title, description, and keywords for the video.  
    """  

    g4f = AI()
  
    # Build prompt for title  
    title_prompt = f"""  
    Generate a catchy and SEO-friendly English title for a YouTube shorts video about {video_subject}.
    STRICTLY GIVE THE CATCHY TITLE WITHOUT ANY MARKDOWN. JUST GIVE THE TEXT  
    """  
  
    # Generate title  
    title = g4f.ask_g4f(title_prompt).strip().strip("\"")+" #youtubeshorts #youtube #shorts #viral #trending #ai #news #viralnewstoday #viralshorts"  
    
    # Build prompt for description  
    description_prompt = f"""  
    Write a brief and engaging English description for a YouTube shorts video about {video_subject}.  
    The video is based on the following script:  
    {script}  
    STRICTLY GIVE JUST THE DESCRIPTION WITHOUT ANY MARKDOWN. JUST GIVE THE TEXT
    """  
  
    # Generate description  
    description = g4f.ask_g4f(description_prompt).strip()  
  
    # Generate keywords  
    keywords = get_search_terms(video_subject, 6, script)  

    return title, description, keywords  