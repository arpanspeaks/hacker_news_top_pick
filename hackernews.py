import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = 'https://news.ycombinator.com/news?p='

def scrape():
    l = []
    for i in range(1, 6):
        url = base_url + str(i)
        print(url)
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        links = soup.select('.storylink')
        subtext = soup.select('.subtext')

        for index, item in enumerate(links):
            news = {}
            title = item.text
            href = item.get('href', None)

            if href[:8] == 'item?id=':
                href = base_url[:-7] + href

            vote = subtext[index].select('.score')

            if len(vote):
                points = int(vote[0].text.replace(' points', ''))

                if points > 99:
                    news['Title'] = title
                    news['Link'] = href
                    news['Votes'] = points
                    l.append(news)

    l = sorted(l, key=lambda x : x['Votes'], reverse=True)                
    df = pd.DataFrame(l)
    df.to_csv('hackernews.csv', index=False)

if __name__ == '__main__':
    scrape()
    print('Data processed and saved to "hackernews.csv"!')