import streamlit as st
import time
import os
import requests
from newsapi import NewsApiClient
import openai
import json
from bs4 import BeautifulSoup

from elevenlabs import play, save
from elevenlabs import ElevenLabs
from pydub import AudioSegment
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

CACHED_PODCAST_SCRIPT = [
    {"type": "script", "value": "Hey everyone, welcome to the show!"},
    
    {"type": "sound-effect", "value": "Audience applause."},
        
    {"type": "script", "value": "AI is doing EVERYTHING!  Even job applications are AI now. You submit your resume, an AI scans it, another AI interviews you, and then an AI tells you, 'Unfortunately, we've decided to move forward with another AI.'"},
    
    {"type": "sound-effect", "value": "Dramatic 'wah-wah-wah' failure sound."},
    
    {"type": "script", "value": "And don’t even get me started on AI in dating apps. My friend’s AI chatbot matched with another AI chatbot, and now they're in a happier relationship than most humans!"},
    
    {"type": "sound-effect", "value": "Audience bursts into laughter with some clapping."},
    
    {"type": "script", "value": "AI assistants are even in our homes. I asked Alexa to set a reminder, and she hit me with, 'Maybe try remembering things yourself for once?'"},
    
    {"type": "sound-effect", "value": "Robotic voice saying 'Oooo, burn!' followed by laughter."},
    
    {"type": "script", "value": "The future is crazy, man. One day, we’ll wake up and AI will be running for president. And honestly? At this point, I might vote for it!"},
    
    {"type": "sound-effect", "value": "Audience cheering and clapping as outro music fades in."}
]

CACHED_PODCAST_SCRIPT_FROMLINK = [
    {"type": "script", "value": "Hey everyone, welcome to the show!"},
    
    {"type": "sound-effect", "value": "Audience applause."},
        
    {"type": "script", "value": "AI is doing EVERYTHING!  Even job applications are AI now. You submit your resume, an AI scans it, another AI interviews you, and then an AI tells you, 'Unfortunately, we've decided to move forward with another AI.'"},
    
    {"type": "sound-effect", "value": "Dramatic 'wah-wah-wah' failure sound."},
    
    {"type": "script", "value": "And don’t even get me started on AI in dating apps. My friend’s AI chatbot matched with another AI chatbot, and now they're in a happier relationship than most humans!"},
    
    {"type": "sound-effect", "value": "Audience bursts into laughter with some clapping."},
    
    {"type": "script", "value": "AI assistants are even in our homes. I asked Alexa to set a reminder, and she hit me with, 'Maybe try remembering things yourself for once?'"},
    
    {"type": "sound-effect", "value": "Robotic voice saying 'Oooo, burn!' followed by laughter."},
    
    {"type": "script", "value": "The future is crazy, man. One day, we’ll wake up and AI will be running for president. And honestly? At this point, I might vote for it!"},
    
    {"type": "sound-effect", "value": "Audience cheering and clapping as outro music fades in."}
]



client = ElevenLabs(
  api_key=os.getenv("ELEVENLABS_API_KEY"),  # Replace with your actual API key
)

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
IS_DEMO = os.getenv("IS_DEMO")

def clean_text(text):
  text = re.sub(r'\s+', ' ', text).strip()
  return text

def scrape_news(url):
  try:
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
      return "Error!"
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    paragraphs = soup.find_all('p')
    news_content = " ".join([clean_text(p.get_text()) for p in paragraphs if p.get_text()])
    
    return news_content if news_content else "Hardcoded content"
  
  except Exception as e:
    return f"Error"


def gen_podcast_overall(topic, news):
  """
  Simulate backend processing. Replace this with your actual backend logic
  that generates an audio file named 'output.mp3'.
  """
  news_stories = None
  if news:
    print(news)
    news_stories = [{"title": '', "content": news}]
  else:
    if IS_DEMO == "true":
      news_stories = [{"title": 'test', "content": 'test'}]
    else:
      news_stories = get_specific_us_news(topic, NEWS_API_KEY, 1)
  
  scripts = []
  for story in news_stories:
    if IS_DEMO == "true":
      if news:
        script = CACHED_PODCAST_SCRIPT_FROMLINK
      else:
        script = CACHED_PODCAST_SCRIPT
    else:
      script = generate_comedy_script(story, OPENAI_API_KEY)
    scripts.append(script)

  if not scripts:
    return None
  curr_script = scripts[0]
  sound_index = 0
  script_index = 0
  ordered_files = []
  for item in curr_script:
    if item['type'] == 'sound-effect':
      generate_sound_effect(item['value'], f"sound_{sound_index}.mp3")
      ordered_files.append(f"sound_{sound_index}.mp3")
      sound_index += 1
    else:
      generate_audio(item['value'], f"script_{script_index}.mp3")
      ordered_files.append(f"script_{script_index}.mp3")
      script_index += 1
  
  combined = AudioSegment.empty()

  for filename in ordered_files:
    try:
      # Handle potential format issues by forcing mp3
      sound = AudioSegment.from_file(filename)
      combined += sound
      print(f"Added: {filename}")
    except Exception as e:
      print(f"Error processing {filename}: {e}")

  output_filename = "result.mp3"

  # Step 5: Export and download
  combined.export(output_filename, format="mp3")
  print(f"\nCombined audio saved as {output_filename}")

  first_audio = AudioSegment.from_file("result.mp3")
  first_audio = first_audio._spawn(first_audio.raw_data, overrides={"frame_rate": int(first_audio.frame_rate * 1.2)})
  first_audio = first_audio.set_frame_rate(first_audio.frame_rate)

  second_audio = AudioSegment.from_file("Standup_comedy.mp3")

  if len(first_audio) < len(second_audio):
    second_audio = second_audio[:len(first_audio)]
  else:
    repeated_audio = second_audio
    while len(repeated_audio) < len(first_audio):
      repeated_audio += second_audio  
    second_audio = repeated_audio[:len(first_audio)]  # Trim to match first_audio length

  # Step 6: Overlay the audio files
  print("\nOverlaying audio files...")
  overlaid_audio = first_audio.overlay(second_audio)

  # Step 7: Save the result
  name = "background-result.mp3"
  overlaid_audio.export(name, format="mp3")
  return name

def get_specific_us_news(topic, api_key, num_articles=1):
  newsapi = NewsApiClient(api_key=api_key)

  top_headlines = newsapi.get_everything(q=topic, page_size=num_articles)

  # Extract and format the results
  news_stories = []

  if top_headlines['status'] == 'ok':
    for article in top_headlines['articles'][:num_articles]:
      news_stories.append({
        'title': article.get('title', 'No title available'),
        'content': article.get('content') or article.get('description', 'No content available'),
        'url': article.get('url', '')
      })
  else:
    print(f"Error: {top_headlines.get('message', 'Unknown error')}")

  return news_stories

def get_top_us_news(api_key, num_articles=5):
    """
    Get the top US news stories using NewsAPI.

    Args:
        api_key (str): Your NewsAPI API key
        num_articles (int): Number of articles to fetch (default: 5)

    Returns:
        list: List of dictionaries containing news title and content
    """
    # Initialize the client
    newsapi = NewsApiClient(api_key=api_key)

    # Fetch top headlines from US
    top_headlines = newsapi.get_top_headlines(
        country='us',
        language='en',
        page_size=num_articles
    )

    # Extract and format the results
    news_stories = []

    if top_headlines['status'] == 'ok':
        for article in top_headlines['articles'][:num_articles]:
            news_stories.append({
                'title': article.get('title', 'No title available'),
                'content': article.get('content') or article.get('description', 'No content available'),
                'url': article.get('url', '')
            })
    else:
        print(f"Error: {top_headlines.get('message', 'Unknown error')}")

    return news_stories

def generate_comedy_script(article, openai_api_key):
    """
    Generate a short comedy standup script based on a news article using OpenAI API.

    Args:
        article (dict): Dictionary containing article title and content
        openai_api_key (str): Your OpenAI API key

    Returns:
        str: Comedy script
    """
    # Set up OpenAI client
    client = openai.OpenAI(api_key=openai_api_key)

    # Create a prompt for the OpenAI model
    prompt = f"""
    Write a short, really fun standup comedy podcast script (about 5-7 lines) based on this news article:

    Title: {article['title']}
    Content: {article['content']}

    The script should be irreverent, witty, and include at least one joke with a punchline.
    Make it sound like a real comedian on stage. Don't use offensive humor. Also in between the script, sometimes you need to describe
    sound effects to make the standup comedy lively. We will use the script to generate audio, so make sure you use the proper grammer and punctuation for the text to speed engine to work.

    You need to return output in this EXACT json format: a list of objects, where each dictionary has
    a field of type (either sound-effect or script), and a field of value (which is string either text of script or description of sound effect needed).

    The list elements would be sequential and would be later combined into a single podcast. Make sure that there are not adjacent script elements since they can be combined into 1 string.
    Basically, your list should alternate between elements with type script and sound-effect.
    Also make sure to describe the sound effect really well, and describe that it should be loud.

    Make sure to just return this json format and nothing else.
    """

    try:
        # Call the OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # You can use a different model if preferred
            messages=[
                {"role": "system", "content": "You are a witty standup comedian who creates short, funny scripts about current news events."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        # Extract and return the generated script
        res = response.choices[0].message.content.strip()
        print(res)
        resjson = json.loads(res)
        return resjson

    except Exception as e:
        return f"Error generating comedy script: {str(e)}"

def generate_sound_effect(text: str, output_path: str):
  print("Generating sound effects...")
  result = client.text_to_sound_effects.convert(
      text=text,
      duration_seconds=3,  # Optional, if not provided will automatically determine the correct length
      prompt_influence=0.3,  # Optional, if not provided will use the default value of 0.3
  )
  with open(output_path, "wb") as f:
      for chunk in result:
          f.write(chunk)
  print(f"Audio saved to {output_path}")

def generate_audio(text: str, filename: str):
  audio = client.text_to_speech.convert(
      text=text,
      voice_id="NOpBlnGInO9m6vDvFkFC",
      model_id="eleven_multilingual_v2",
      output_format="mp3_44100_128",
  )
  save(audio, filename)

st.title("Trending Laughs")

option = st.radio("Choose input type:", ("Topic", "News Article URL"))

topic = None
news = None

if option == "Topic":
  topic = st.text_input("Enter a topic for the news article:")
  news = None
else:
  news_url = st.text_input("Enter the URL of the news article:")
  if IS_DEMO == "true":
    news = "Hardcoded content"
  else:
    news = scrape_news(news_url)
  topic = None
# topic = st.text_input("Enter a topic for the news article or the link to the news article:")

if st.button("Submit"):
  if (topic and topic.strip()) or news:
    st.write("Generating audio... Please wait.")
    filename = gen_podcast_overall(topic, news)
    if not filename:
      st.error("Audio generation failed. Please try again.")
    
    if os.path.exists(filename):
      st.audio(filename, format="audio/mp3", start_time=0)
    else:
      st.error("Audio generation failed. Please try again.")
  else:
    st.warning("Please enter a topic before submitting.")
