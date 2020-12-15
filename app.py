from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask import Markup

app = Flask(__name__)


@app.route("/")
def index():
    from database import Database
    db = Database()
    channels = db.getChannels()

    tempText = ''
    for i in channels:
        channelId = i['channel_id']
        row = "<tr><td></td><td><a href='http://c7hqkpkpemu6e7emz5b4vyz7idjgdvgaaa3dyimmeojqbgpea3xqjoid.onion/%s' target='_blank'>%s</a>" \
              "</td><td>%s</td>" \
              "<td>%s</td>" \
              "<td>%s</td>" \
              "<td><a href='/channel/%s/0'>unseen</a></td>" \
              "<td><a href='/channel/%s/1'>seen</a></td>" \
              "<td><a href='/channel/%s/all'>all</a></td>" \
              "</tr>" % (channelId, db.getChannelName(channelId),
                         db.countVideosWithSeenStatus(channelId, 0),
                         db.countVideosWithSeenStatus(channelId, 1),
                         db.countVideosWithSeenStatus(channelId),
                         channelId, channelId, channelId)
        tempText += row

    return render_template('channel-list.html', tbody=Markup(tempText))


@app.route("/channel/<channelId>/<videoType>")
def scrapChannel(channelId, videoType):
    from database import Database
    db = Database()

    if videoType == '0':
        videos = db.getVideosWithSeenStatusOf(channelId, 0)
    elif videoType == '1':
        videos = db.getVideosWithSeenStatusOf(channelId, 1)
    else:
        videos = db.getAllVideosOfChannel(channelId)

    tempText = ''
    for vid in videos:
        row = "<tr><td></td><td><a href='http://c7hqkpkpemu6e7emz5b4vyz7idjgdvgaaa3dyimmeojqbgpea3xqjoid.onion/%s' target='_blank'>%s</a>" \
              "</td><td>%s</td>" \
              "<td>%s</td>" \
              "<td>%s</td>" \
              "<td>%s</td>" \
              "<td>%s</td>" \
              "<td><input name='seen' value='%s' type='checkbox' %s></td>" \
              "</tr>" % (vid['video_id'], vid['title'], vid['upload_date'], vid['length'], vid['views'], vid['channel'],
                         vid['scraped_date'],
                         vid['video_id'],
                         'checked disabled' if vid['seen'] == 1 else '')
        tempText += row

    return render_template('table-responsive.html', tbody=Markup(tempText))


@app.route('/mark-as-seen', methods=['POST', 'GET'])
def markAsSeen():
    videos = request.form.getlist('seen')
    from database import Database
    db = Database()
    db.markVideosAsRead(videos)
    response = "<p>%d videos Marked As Seen!!</p>" % len(videos)

    return response


app.run(debug=True)
