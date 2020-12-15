class Database:
    def __init__(self):
        self.databasePath = '/mnt/78464AB8464A76C2/DataBackups/invidious'

    def insertData(self, videoDetails):
        import sqlite3 as sql
        connection = sql.connect(database=self.databasePath)
        query = 'insert into data (video_id, title, views, channel, upload_date, length, scraped_date, channel_id) ' \
                'values(?,?,?,?,?,?,?,?)'
        for v in videoDetails:
            try:
                connection.execute(query, (v['video_id'], v['title'], v['views'], v['channel'],
                                           v['upload_date'], v['length'], v['scraped_date'],
                                           v['channel_id']))
            except Exception as ex:
                print(ex, v)
        connection.commit()
        connection.close()

    def getVideosWithSeenStatusOf(self, channelId, seenStatus):
        import sqlite3 as sql
        connection = sql.connect(database=self.databasePath)
        connection.row_factory = lambda c, r: dict(zip([col[0] for col in c.description], r))
        query = "select * from data where channel_id='%s' and seen=%d" % (channelId, seenStatus)
        videos = connection.execute(query).fetchall()
        connection.close()
        return videos

    def getAllVideosOfChannel(self, channelId):
        import sqlite3 as sql
        connection = sql.connect(database=self.databasePath)
        connection.row_factory = lambda c, r: dict(zip([col[0] for col in c.description], r))
        query = "select * from data where channel_id='%s'" % channelId
        videos = connection.execute(query).fetchall()
        connection.close()
        return videos

    def getChannels(self):
        import sqlite3 as sql
        connection = sql.connect(database=self.databasePath)
        connection.row_factory = lambda c, r: dict(zip([col[0] for col in c.description], r))
        query = "select distinct channel_id from data"
        channels = connection.execute(query).fetchall()
        connection.close()
        return channels

    def getChannelName(self, channelId):
        import sqlite3 as sql
        connection = sql.connect(database=self.databasePath)
        query = "select distinct channel from data where channel_id='%s'" % channelId
        channels = connection.execute(query).fetchone()[0]
        connection.close()
        return channels

    def countVideosWithSeenStatus(self, channelId, seenStatus=None):
        import sqlite3 as sql
        connection = sql.connect(database=self.databasePath)
        query = "select count(video_id) from data where channel_id='%s' %s" % (channelId,
                                                                               'and seen=%d' % seenStatus if seenStatus is not None else '')
        channels = connection.execute(query).fetchone()[0]
        connection.close()
        return channels

    def markVideosAsRead(self, videoList):
        import sqlite3 as sql
        connection = sql.connect(database=self.databasePath)
        query = "update data set seen=1 where video_id = '%s'"
        for i in videoList:
            connection.execute(query % i)
        connection.commit()
        connection.close()
