code = """<div class="pure-u-1 pure-u-md-1-4">
    <div class="h-box">
        
        
            
                <a style="width:100%" href="/watch?v=yGxCQisOL1A">
                    <div class="thumbnail">
                        <img class="thumbnail" src="/vi/yGxCQisOL1A/mqdefault.jpg">
                        

                        
                            <p class="length">4:24</p>
                        
                    </div>
                </a>
            
            <p><a href="/watch?v=yGxCQisOL1A">How to Set JAVA_HOME Environment Variable and Java Path on Windows 10</a></p>
            <p>
                <b>
                    <a style="width:100%" href="/channel/UC1Be9fnFTlcsUlejgfqag0g">Java Guides</a>
                </b>
            </p>

            <h5 class="pure-g">
                
                    <div class="pure-u-2-3">Shared 11 months ago</div>
                

                <div class="pure-u-1-3" style="text-align:right">
                    4.4K views
                </div>
            </h5>
        
    </div>
</div>"""

from bs4 import BeautifulSoup as Soup

soup = Soup(code, 'lxml')
text = soup.text
videoData = []  # [length, title, channel, upload date, views]
for i in text.splitlines():
    i = i.strip()
    if len(i) != 0:
        videoData.append(i)
print(videoData)
print(soup.a.get('href'))
