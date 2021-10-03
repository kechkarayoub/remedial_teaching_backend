import datetime

from django.conf import settings
import json, requests
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
}


def set_feeds(language, items_test_str=None):
    feeds = []
    if items_test_str:
        items = json.loads(items_test_str)
        feeds = [*feeds, *items]
    else:
        urls = feeds_urls.get(language) or []
        for url in urls:
            try:
                response = requests.get('https://api.rss2json.com/v1/api.json?api_key=' + settings.RSS2JSON_API_KEY + '&rss_url=' + url)
                items = json.loads(response.content).get("items")
                feeds = [*feeds, *items]
            except:
                pass
    if feeds:
        feeds_str = json.dumps(feeds)
        last_update = datetime.datetime.now()
        if FeedsLanguage.objects.filter(language=language).exists():
            FeedsLanguage.objects.filter(language=language).update(feeds=feeds_str, last_update=last_update)
        else:
            FeedsLanguage.objects.create(language=language, feeds=feeds_str, last_update=last_update)
    return len(feeds)

