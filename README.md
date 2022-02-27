# london_ticket_scraper
Fetch data on websites and tell me prices of good ones


## What this does
1. Go onto various websites such as [todaytix](https://www.todaytix.com) and collect information (price, venue, etc)
2. Write these to the folder `data/`
3. `run.py` then opens the known data files (currently in `.csv` format) and notifies via telegram the ones that hit the threshold 

> My current setting for this is musicals less than £15, or plays less than £10 at the globe theatre. 

## Installation 
1. Create the folders for scraper output:

```bash
mkdir data
```

2. Obtain Telegram API token via [the botfather](https://core.telegram.org/bots)

3. Install the python packages

4. `python3 run.py`