from bs4 import BeautifulSoup as Soup
from urllib.request import urlopen

url = 'https://www.youtube.com/feeds/videos.xml?channel_id=UCFsDXM40vHfbNEBt9YdayVg'
site = urlopen(url)

soup = Soup(site.read(), 'xml')
entries = soup.find_all('entry')
for i in entries:

    # videoData = {
    #     'length': tempData[0],
    #     'title': tempData[1],
    #     'channel': tempData[2],
    #     'upload_date': tempData[3],
    #     'views': tempData[4],
    #     'video_id': videoId,
    #     'channel_id': channelId,
    #     'scraped_date': str(date.today())
    # }
