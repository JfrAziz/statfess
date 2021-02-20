from config import create_api, TRIGER_WORD
from bots.TwitterBot import TwitterBot

if __name__ == "__main__":
  api = create_api()
  bots = TwitterBot(api, TRIGER_WORD)
  bots.run()
  

