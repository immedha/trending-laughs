# trending-laughs
> [!IMPORTANT]  
> 🎉 This project won Microsoft Reactor Redmond's [OSS4AI Hackathon #15 - AI Agents](https://lu.ma/9bx3hw3v?tk=l6UyJ0)! 🎉
> 
> View our project demo & slides [here](https://docs.google.com/presentation/d/1cwD9oKjCE9u7PvtyLCnRfM5Ng2LwUXxg2PtRzc-A7_Y/edit?usp=sharing)


Steps to run this repo:

1. Clone the repo
2. Do `cd https://github.com/immedha/trending-laughs`
3. Create a `.env` with environment variables `NEWS_API_KEY`,`OPENAI_API_KEY`, `ELEVENLABS_API_KEY`. Also add a variable of `IS_DEMO` and set it to "true" or "false" depending on if you are doing the hackathon demo.
4. Create a `venv` by doing `python -m venv` and activate it: `source venv/bin/activate`
4. Install everything by doing `pip install -r requirements.txt`
5. Do `brew install ffmpeg`
5. Run app by doing `streamlit run main.py`

6. You can get News_API_KEY from https://newsapi.org/docs/client-libraries/python
7. Presentation slides https://docs.google.com/presentation/d/1cwD9oKjCE9u7PvtyLCnRfM5Ng2LwUXxg2PtRzc-A7_Y/edit?usp=sharing
