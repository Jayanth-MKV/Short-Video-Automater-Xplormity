import requests


def search_for_stock_videos(query: str, api_key: str, it: int, min_dur: int) -> list[str]:
    """
    Searches for stock videos based on a query.

    Args:
        query (str): The query to search for.
        api_key (str): The API key to use.

    Returns:
        list[str]: A list of stock videos.
    """

    # Build headers
    headers = {
        "Authorization": api_key
    }

    # Build URL
    qurl = f"https://api.pexels.com/videos/search?query={query}&per_page={it}&orientation=portrait"
    # Send the request
    r = requests.get(qurl, headers=headers)

    # log response
    print(f"Response: {r.status_code}")

    # Parse the response
    response = r.json()
    print([response["videos"][i]["duration"] for i in range(len(response["videos"]))])

    # Parse each video
    raw_urls = []
    video_url = []
    try:
        # loop through each video in the result
        for i in range(it):
            video_res = 0
            #check if video has desired minimum duration
            if response["videos"][i]["duration"] < min_dur:
                continue
            raw_urls = response["videos"][i]["video_files"]

            temp_video_url = ""

            # loop through each url to determine the best quality
            for video in raw_urls:
                # Check if video has a valid download link
                if ".com" in video["link"]:
                    # Only save the URL with the largest resolution
                    if (video["width"]*video["height"]) > video_res:
                        temp_video_url = video["link"]
                        video_res = video["width"]*video["height"]

            # add the url to the return list if it's not empty
            if temp_video_url != "":
                video_url.append(temp_video_url)

    except Exception as e:
        print("[-] No Videos found.")
        print(e)

    # Let user know
    print(f"\t=> \"{query}\" found {len(video_url)} Videos")

    # Return the video url
    return video_url