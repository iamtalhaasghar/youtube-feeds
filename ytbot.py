class YoutubeChannelBot:

    def __init__(self, channelId):
        self.channelId = channelId
        self.channelName = ""

    def __getFirefoxDriver(self):
        from selenium import webdriver
        from selenium.webdriver.firefox.options import Options
        options = Options()
        options.headless = True
        geckoDriver = '/home/talha/Programs/geckodriver'
        browser = webdriver.Firefox(options=options, executable_path=geckoDriver)
        return browser

    def __startScrapingVideos(self, browser):
        videoList = list()
        for i in range(100):
            aTags = browser.find_elements_by_id('video-title')
            del aTags[0: len(videoList)]
            for a in aTags:
                title = a.get_attribute('title')
                href = a.get_attribute('href')
                videoList.append({'title': title, 'href': href})
                print(videoList[-1])
                from selenium.webdriver.common.keys import Keys
                a.send_keys(Keys.ARROW_DOWN)
        return videoList

    def scrap(self):
        browser = self.__getFirefoxDriver()
        channelUrl = 'https://www.youtube.com/channel/%s/videos' % self.channelId
        browser.get(channelUrl)
        self.channelName = browser.find_element_by_id('channel-name').text
        videoList = self.__startScrapingVideos(browser)
        browser.close()
        return videoList

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        channelIds = sys.argv[1:]
        for channel in channelIds:
            ytChannel = YoutubeChannelBot(channel)
            videos = ytChannel.scrap()
            f = open('%s.html' % ytChannel.channelName, 'w', encoding='utf-8')
            f.write('<ol>')
            for v in videos:
                f.write("<li><a href='%s' target=_blank>%s</a></li>\n" % (v['href'], v['title']))
            f.write('</ol>')
            f.close()
    else:
        print('Usage: python ytbot.py [channel1_id[...]]')