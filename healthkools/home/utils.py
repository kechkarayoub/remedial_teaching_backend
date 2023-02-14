import datetime
import json
import requests
from datetime import timezone
from django.conf import settings
from random import randrange
from .models import FeedsLanguage

feeds_urls = {
    "ar": [
        "https://aawsat.com/feed/health",
        "https://news.un.org/feed/subscribe/ar/news/topic/health/feed/rss.xml",
        "https://www.almaghribtoday.net/health/rss.xml",
        "https://www.casablancatoday.com/health/rss.xml",
        "https://www.moh.gov.bh/News/Rss/ar",
    ],
    "en": [
        "http://rssfeeds.webmd.com/rss/rss.aspx?RSSSource=RSS_PUBLIC",
        "https://blog.myfitnesspal.com/feed/",
        "https://blogs.cisco.com/healthcare/feed",
        "https://feeds.npr.org/103537970/rss.xml",
        "https://www.healthstatus.com/feed/",
        "https://www.mobihealthnews.com/feed",
    ],
    "fr": [
        "https://www.santemagazine.fr/feeds/rss",
        "https://www.santemagazine.fr/feeds/rss/alimentation",
        "https://www.santemagazine.fr/feeds/rss/beaute-forme",
        "https://www.santemagazine.fr/feeds/rss/medecines-alternatives",
        "https://www.santemagazine.fr/feeds/rss/minceur",
        "https://www.santemagazine.fr/feeds/rss/sante",
        "https://www.santemagazine.fr/feeds/rss/traitement",
    ],
    "test_en": [
        "http://rssfeeds.webmd.com/rss/rss.aspx?RSSSource=RSS_PUBLIC",
        "https://blog.myfitnesspal.com/feed/",
    ],
    "test_en_failed": [
        "http://rssfeeds.webkk0md.com/rss/rss.aspx?RSSSource=RSS_PUBLIC",
    ],
}
feeds_urls["test_en"] = [feeds_urls["en"][randrange(len(feeds_urls["en"]))]]


def set_feeds(language):
    """
        :param language: the language of feeds to be got from remote servers and stored
        :return: length of stored feeds
    """
    feeds = []
    # get urls by language
    urls = feeds_urls.get(language) or []
    for url in urls:
        # for each rss url we get items via rss2json api and append them to feeds array
        try:
            response = requests.get('https://api.rss2json.com/v1/api.json?api_key=' + settings.RSS2JSON_API_KEY + '&rss_url=' + url)
            items = json.loads(response.content).get("items")
            feeds += items
        except:
            pass
    if feeds:
        # stringify feeds for store them in databases
        feeds_str = json.dumps(feeds)
        last_update = datetime.datetime.now().replace(tzinfo=timezone.utc)
        # save last date we get feeds
        if FeedsLanguage.objects.filter(language=language).exists():
            FeedsLanguage.objects.filter(language=language).update(feeds=feeds_str, last_update=last_update)
        else:
            FeedsLanguage.objects.create(language=language, feeds=feeds_str, last_update=last_update)
    return len(feeds)

