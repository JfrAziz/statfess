import time

import config
from bots.TwitterBot import TwitterBot

if __name__ == "__main__":
  bots = TwitterBot()
  while True:
    bots.run()
    print("Waiting...")
    time.sleep(config.TIME_SLEEP)
  

