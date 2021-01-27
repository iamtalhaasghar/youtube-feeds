class InvidiousBot:

    def __init__(self):
        pass

    def scrapVideosOfChannel(self, channelId, alreadyScrapedVideoList=None):
        from bs4 import BeautifulSoup as Soup
        from urllib.request import urlopen, Request
        from datetime import date

        channelUrl = 'https://www.youtube.com/feeds/videos.xml?channel_id=%s' % channelId
        site = urlopen(Request(channelUrl, headers={'User-Agent': 'Mozilla'}))

        soup = Soup(site.read(), 'xml')
        entries = soup.find_all('entry')
        scrapedVideos = list()
        for (index, i) in enumerate(entries):
            videoTitle = i.title.text
            channelName = i.find('author').find('name').text
            uploadDate = i.published.text
            views = i.find('media:statistics').get('views')
            videoId = i.find('yt:videoId').text
            channelId = i.find('yt:channelId').text

            videoData = {
                'length': '-',
                'title': videoTitle,
                'channel': channelName,
                'upload_date': uploadDate,
                'views': views,
                'video_id': videoId,
                'channel_id': channelId,
                'scraped_date': str(date.today())
            }
            print(index, videoData['title'])
            if alreadyScrapedVideoList is not None and videoData['video_id'] in alreadyScrapedVideoList:
                print('Already Scraped')
            else:
                scrapedVideos.append(videoData)
                print('Saved')

        return scrapedVideos

    def scrapAllChannels(self, channelId):
        videoList = self.scrapVideosOfChannel(channelId)
        return videoList


if __name__ == "__main__":
    import sys
    from database import Database

    db = Database(2)
    allChannels = db.getChannels()
    allChannels = [i['channel_id'] for i in allChannels]
    if len(sys.argv) > 1:
        channelIds = sys.argv[1:]
    else:
        channelIds = allChannels

    for channel in channelIds:
        print('Scraping: ', channel)
        videos = db.getAllVideosOfChannel(channel)
        videos = [i['video_id'] for i in videos]
        ytChannel = InvidiousBot()
        videos = ytChannel.scrapVideosOfChannel(channel, videos)
        db.insertData(videos)
        print('videos added')


