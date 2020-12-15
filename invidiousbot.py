class InvidiousBot:

    def __init__(self):
        pass

    def __getFirefoxDriver(self):
        from selenium import webdriver
        from selenium.webdriver.firefox.options import Options

        options = Options()
        options.headless = True
        geckoDriver = '/home/talha/Programs/geckodriver'
        browser = webdriver.Firefox(options=options, executable_path=geckoDriver)
        return browser

    def scrapVideosOfChannel(self, channelId, alreadyScrapedVideoList=None):
        from bs4 import BeautifulSoup as Soup
        from datetime import date
        browser = self.__getFirefoxDriver()
        channelUrl = 'https://vid.mint.lgbt/channel/%s' % channelId
        isThereNextPage = True
        alreadyScraped = False
        pageNumber = 1
        scrapedVideos = list()
        while not alreadyScraped and isThereNextPage:
            browser.get('%s?page=%d' % (channelUrl, pageNumber))
            videoDivs = browser.find_elements_by_xpath('//h5/parent::div')
            index = 0
            while not alreadyScraped and index < len(videoDivs):
                div = videoDivs[index]
                index += 1
                divHtml = div.get_attribute('innerHTML')
                soup = Soup(divHtml, 'lxml')
                text = soup.text
                href = soup.a.get('href')
                videoId = href.split('=')[1]
                tempData = []  # [length, title, channel, date, views]
                for i in text.splitlines():
                    i = i.strip()
                    if len(i) != 0:
                        tempData.append(i)

                videoData = {
                    'length': tempData[0],
                    'title': tempData[1],
                    'channel': tempData[2],
                    'upload_date': tempData[3],
                    'views': tempData[4],
                    'video_id': videoId,
                    'channel_id': channelId,
                    'scraped_date': str(date.today())
                }
                print(videoData)
                if alreadyScrapedVideoList is not None and videoData['video_id'] in alreadyScrapedVideoList:
                    alreadyScraped = True
                else:
                    scrapedVideos.append(videoData)

            if not alreadyScraped:
                try:
                    browser.find_element_by_link_text('Next page')
                    pageNumber += 1
                except Exception as ex:
                    isThereNextPage = False
        browser.close()
        return scrapedVideos

    def scrapAllChannels(self, channelId):
        videoList = self.scrapVideosOfChannel(channelId)
        return videoList


if __name__ == "__main__":
    import sys
    from database import Database

    db = Database()
    allChannels = db.getChannels()
    allChannels = [i['channel_id'] for i in allChannels]
    if len(sys.argv) > 1:
        channelIds = sys.argv[1:]
    else:
        channelIds = allChannels

    for channel in channelIds:
        print(channel)
        videos = db.getAllVideosOfChannel(channel)
        videos = [i['video_id'] for i in videos]
        ytChannel = InvidiousBot()
        videos = ytChannel.scrapVideosOfChannel(channel, videos)
        db.insertData(videos)


