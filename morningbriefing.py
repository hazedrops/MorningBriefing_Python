import requests
from bs4 import BeautifulSoup


def create_soup(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    return soup


def print_news(index, title, link):
    print(str(index+1) + ". " + title)
    print("(Link : {})\n".format(link))


def scrape_weather():
    print("*** Today's Weather ***")
    url = "https://weather.com/weather/today/l/830bfbf6042fe40c41c02552125b5d99d77b9099c083ea06576fc773daf1f139"
    soup = create_soup(url)

    cast = soup.find("div", attrs={"class": "_2xXSr"}
                     ).get_text()  # Weather cast info
    curr_temp = soup.find("span", attrs={"class": "_3KcTQ"}).get_text()
    high_low_temp = soup.find("div", attrs={"class": "A4RQE"}).get_text()

    if(soup.find(
            "div", attrs={"data-testid": "precipPhrase"})):
        rain_per = soup.find(
            "div", attrs={"data-testid": "precipPhrase"}).get_text()
    air_quality_index = soup.find(
        "text", attrs={"data-testid": "DonutChartValue"}).get_text().strip()
    air_quality_cat = soup.find(
        "span", attrs={"data-testid": "AirQualityCategory"}).get_text()

    # Output
    print("It is ", cast)
    print("High / Low : ".strip(), high_low_temp)

    if(soup.find(
            "div", attrs={"data-testid": "precipPhrase"})):
        print(rain_per)
    print("Air Quality Index : {} - {}".format(air_quality_index,
                                               air_quality_cat).strip())
    print()


def scrape_headline_news():
    print("*** Today's Headline News ***")
    url = "https://www.cnn.com/us"
    soup = create_soup(url)

    news_list = soup.find("ul", attrs={
                          "class": "cn cn-list-hierarchical-xs cn--idx-0 cn-coverageContainer_35DB3D2D-AC3D-85A6-F7F3-9694BBCB125F"}).find_all("li", limit=3)
    for index, news in enumerate(news_list):
        news_title = news.find(
            "h3", attrs={"class": "cd__headline"}).get_text()
        news_link = "https://www.cnn.com" + news.find("a")["href"]

        print_news(index, news_title, news_link)


def scrape_tech_news():
    print("*** Today's Tech News ***")
    url = "https://www.cnet.com/news/"
    soup = create_soup(url)

    # with open("tech.html", "w", encoding="utf8") as f:
    #     f.write(soup.prettify())

    news_list = soup.find("section", attrs={
                          "id": "topStories"}).find_all("div", attrs={"class": "content"})

    for index, news in enumerate(news_list):
        news_title = news.find("h3", attrs={"class": "h"}).get_text()
        news_link = "https://www.cnet.com" + news.find("a")["href"]

        print_news(index, news_title, news_link)


def scrape_word_of_the_day():
    print("*** Today's Word ***")
    url = "https://www.merriam-webster.com/word-of-the-day"
    soup = create_soup(url)

    word = soup.find(
        "div", attrs={"class": "word-and-pronunciation"}).find("h1").get_text()
    definition = soup.find(
        "div", attrs={"class": "wod-definition-container"}).find("p").get_text()

    print(word + " " + definition + "\n")

    examples = soup.find(
        "div", attrs={"class": "wotd-examples"}).find_all("p")

    # print(examples)
    # print(type(examples), len(examples))

    for index, example in enumerate(examples):
        ex = example.get_text()
        # print(ex)
        print("Ex{}. {}\n".format(index+1, ex))


if(__name__ == "__main__"):
    scrape_weather()  # Today's weather
    scrape_headline_news()  # Headline News
    scrape_tech_news()  # Tech News
    scrape_word_of_the_day()
