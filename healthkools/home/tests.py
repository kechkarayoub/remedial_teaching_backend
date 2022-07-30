# -*- coding: utf-8 -*-

from .models import *
from.utils import set_feeds
from django.test import TestCase
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from unittest.mock import patch
import json, datetime
from datetime import timezone


class FeedsLanguageModelTests(TestCase):
    feeds_str = '[{"description": "\\n<img width=\\"1024\\" height=\\"643\\" src=\\"https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-scaled-1024x643.jpg\\" class=\\"attachment-large size-large wp-post-image\\" alt=\\"How the Pandemic Inspired Mike to Lose 245 pounds\\" loading=\\"lazy\\" srcset=\\"https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-scaled-1024x643.jpg 1024w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-scaled-300x188.jpg 300w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-768x482.jpg 768w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-1536x964.jpg 1536w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-2048x1286.jpg 2048w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-500x315.jpg 500w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-752x472.jpg 752w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-269x169.jpg 269w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-444x280.jpg 444w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-299x188.jpg 299w\\" sizes=\\"(max-width: 1024px) 100vw, 1024px\\"><p>Mike went to bed every night thinking he was going to have a heart attack. Watch his inspiring story of weight loss and grit.</p>\\n<p>The post <a rel=\\"nofollow\\" href=\\"https://blog.myfitnesspal.com/watch/how-the-pandemic-inspired-mike-to-lose-245-pounds/\\">How the Pandemic Inspired Mike to Lose 245 pounds</a> appeared first on <a rel=\\"nofollow\\" href=\\"https://blog.myfitnesspal.com/\\">MyFitnessPal Blog</a>.</p>\\n", "pubDate": "2021-09-27 20:00:52", "author": "Amy Hoehn", "title": "How the Pandemic Inspired Mike to Lose 245 pounds", "enclosure": {"link": "https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-scaled.jpg"}, "content": "\\n<img width=\\"1024\\" height=\\"643\\" src=\\"https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-scaled-1024x643.jpg\\" class=\\"attachment-large size-large wp-post-image\\" alt=\\"How the Pandemic Inspired Mike to Lose 245 pounds\\" loading=\\"lazy\\" srcset=\\"https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-scaled-1024x643.jpg 1024w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-scaled-300x188.jpg 300w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-768x482.jpg 768w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-1536x964.jpg 1536w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-2048x1286.jpg 2048w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-500x315.jpg 500w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-752x472.jpg 752w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-269x169.jpg 269w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-444x280.jpg 444w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-299x188.jpg 299w\\" sizes=\\"(max-width: 1024px) 100vw, 1024px\\"><p>Mike went to bed every night thinking he was going to have a heart attack. Watch his inspiring story of weight loss and grit.</p>\\n<p>The post <a rel=\\"nofollow\\" href=\\"https://blog.myfitnesspal.com/watch/how-the-pandemic-inspired-mike-to-lose-245-pounds/\\">How the Pandemic Inspired Mike to Lose 245 pounds</a> appeared first on <a rel=\\"nofollow\\" href=\\"https://blog.myfitnesspal.com/\\">MyFitnessPal Blog</a>.</p>\\n", "link": "https://blog.myfitnesspal.com/watch/how-the-pandemic-inspired-mike-to-lose-245-pounds/", "guid": "https://blog.myfitnesspal.com/?post_type=video_hub&amp;p=50944", "thumbnail": "https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-scaled-1024x643.jpg", "categories": []}, {"description": "\\n<img width=\\"1024\\" height=\\"643\\" src=\\"https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-scaled-1024x643.jpg\\" class=\\"attachment-large size-large wp-post-image\\" alt=\\"How Cam\\u2019s Weight Loss and Fitness Journey Saved His Son\\u2019s Life\\" loading=\\"lazy\\" srcset=\\"https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-scaled-1024x643.jpg 1024w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-scaled-300x188.jpg 300w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-768x482.jpg 768w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-scaled-1536x964.jpg 1536w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-scaled-2048x1286.jpg 2048w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-500x315.jpg 500w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-scaled-752x472.jpg 752w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-269x169.jpg 269w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-444x280.jpg 444w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-299x188.jpg 299w\\" sizes=\\"(max-width: 1024px) 100vw, 1024px\\"><p>When Cam Summerson\\u2019s son needed his help, the only way he could give it was by losing weight.</p>\\n<p>The post <a rel=\\"nofollow\\" href=\\"https://blog.myfitnesspal.com/watch/how-cams-weight-loss-and-fitness-journey-saved-his-sons-life/\\">How Cam\\u2019s Weight Loss and Fitness Journey Saved His Son\\u2019s Life</a> appeared first on <a rel=\\"nofollow\\" href=\\"https://blog.myfitnesspal.com/\\">MyFitnessPal Blog</a>.</p>\\n", "pubDate": "2021-09-23 16:00:03", "author": "Amy Hoehn", "title": "How Cam\\u2019s Weight Loss and Fitness Journey Saved His Son\\u2019s Life", "enclosure": {"link": "https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-scaled.jpg"}, "content": "\\n<img width=\\"1024\\" height=\\"643\\" src=\\"https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-scaled-1024x643.jpg\\" class=\\"attachment-large size-large wp-post-image\\" alt=\\"How Cam\\u2019s Weight Loss and Fitness Journey Saved His Son\\u2019s Life\\" loading=\\"lazy\\" srcset=\\"https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-scaled-1024x643.jpg 1024w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-scaled-300x188.jpg 300w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-768x482.jpg 768w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-scaled-1536x964.jpg 1536w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-scaled-2048x1286.jpg 2048w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-500x315.jpg 500w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-scaled-752x472.jpg 752w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-269x169.jpg 269w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-444x280.jpg 444w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-299x188.jpg 299w\\" sizes=\\"(max-width: 1024px) 100vw, 1024px\\"><p>When Cam Summerson\\u2019s son needed his help, the only way he could give it was by losing weight.</p>\\n<p>The post <a rel=\\"nofollow\\" href=\\"https://blog.myfitnesspal.com/watch/how-cams-weight-loss-and-fitness-journey-saved-his-sons-life/\\">How Cam\\u2019s Weight Loss and Fitness Journey Saved His Son\\u2019s Life</a> appeared first on <a rel=\\"nofollow\\" href=\\"https://blog.myfitnesspal.com/\\">MyFitnessPal Blog</a>.</p>\\n", "link": "https://blog.myfitnesspal.com/watch/how-cams-weight-loss-and-fitness-journey-saved-his-sons-life/", "guid": "https://blog.myfitnesspal.com/?post_type=video_hub&amp;p=51015", "thumbnail": "https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-scaled-1024x643.jpg", "categories": []}, {"description": "\\n<img width=\\"1024\\" height=\\"643\\" src=\\"https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-scaled-1024x643.jpg\\" class=\\"attachment-large size-large wp-post-image\\" alt=\\"Can Intermittent Fasting Help Me Lose Weight?\\" loading=\\"lazy\\" srcset=\\"https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-scaled-1024x643.jpg 1024w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-scaled-300x188.jpg 300w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-768x482.jpg 768w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-scaled-1536x964.jpg 1536w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-scaled-2048x1286.jpg 2048w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-500x315.jpg 500w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-scaled-752x472.jpg 752w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-269x169.jpg 269w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-444x280.jpg 444w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-299x188.jpg 299w\\" sizes=\\"(max-width: 1024px) 100vw, 1024px\\"><p>Wondering if you should try intermittent fasting to lose weight? Registered Dietitian Whitney English explains that the claim that intermittent fasting can help you lose weight is only partially true.</p>\\n<p>The post <a rel=\\"nofollow\\" href=\\"https://blog.myfitnesspal.com/watch/can-intermittent-fasting-help-me-lose-weight/\\">Can Intermittent Fasting Help Me Lose Weight?</a> appeared first on <a rel=\\"nofollow\\" href=\\"https://blog.myfitnesspal.com/\\">MyFitnessPal Blog</a>.</p>\\n", "pubDate": "2021-09-22 16:00:16", "author": "Amy Hoehn", "title": "Can Intermittent Fasting Help Me Lose Weight?", "enclosure": {"link": "https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-scaled.jpg"}, "content": "\\n<img width=\\"1024\\" height=\\"643\\" src=\\"https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-scaled-1024x643.jpg\\" class=\\"attachment-large size-large wp-post-image\\" alt=\\"Can Intermittent Fasting Help Me Lose Weight?\\" loading=\\"lazy\\" srcset=\\"https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-scaled-1024x643.jpg 1024w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-scaled-300x188.jpg 300w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-768x482.jpg 768w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-scaled-1536x964.jpg 1536w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-scaled-2048x1286.jpg 2048w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-500x315.jpg 500w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-scaled-752x472.jpg 752w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-269x169.jpg 269w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-444x280.jpg 444w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-299x188.jpg 299w\\" sizes=\\"(max-width: 1024px) 100vw, 1024px\\"><p>Wondering if you should try intermittent fasting to lose weight? Registered Dietitian Whitney English explains that the claim that intermittent fasting can help you lose weight is only partially true.</p>\\n<p>The post <a rel=\\"nofollow\\" href=\\"https://blog.myfitnesspal.com/watch/can-intermittent-fasting-help-me-lose-weight/\\">Can Intermittent Fasting Help Me Lose Weight?</a> appeared first on <a rel=\\"nofollow\\" href=\\"https://blog.myfitnesspal.com/\\">MyFitnessPal Blog</a>.</p>\\n", "link": "https://blog.myfitnesspal.com/watch/can-intermittent-fasting-help-me-lose-weight/", "guid": "https://blog.myfitnesspal.com/?post_type=video_hub&amp;p=51019", "thumbnail": "https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-scaled-1024x643.jpg", "categories": []}]'

    def test_to_items_list(self):
        feeds_language = FeedsLanguage(language="en", feeds=self.feeds_str)
        feeds_language.save()
        feeds_list = feeds_language.to_items_list()
        self.assertEqual(len(feeds_list), 3)
        self.assertEqual(feeds_list[0]["title"], "How the Pandemic Inspired Mike to Lose 245 pounds")

    def test___str__(self):
        feeds_language = FeedsLanguage(language="en", feeds=self.feeds_str)
        feeds_language.save()
        str_ = feeds_language.__str__()
        self.assertEqual(str_, "en_feeds")


class HomeViewsTest(TestCase):

    def setUp(self):
        self.feeds_str = '[{"description": "\\n<img width=\\"1024\\" height=\\"643\\" src=\\"https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-scaled-1024x643.jpg\\" class=\\"attachment-large size-large wp-post-image\\" alt=\\"How the Pandemic Inspired Mike to Lose 245 pounds\\" loading=\\"lazy\\" srcset=\\"https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-scaled-1024x643.jpg 1024w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-scaled-300x188.jpg 300w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-768x482.jpg 768w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-1536x964.jpg 1536w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-2048x1286.jpg 2048w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-500x315.jpg 500w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-752x472.jpg 752w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-269x169.jpg 269w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-444x280.jpg 444w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-299x188.jpg 299w\\" sizes=\\"(max-width: 1024px) 100vw, 1024px\\"><p>Mike went to bed every night thinking he was going to have a heart attack. Watch his inspiring story of weight loss and grit.</p>\\n<p>The post <a rel=\\"nofollow\\" href=\\"https://blog.myfitnesspal.com/watch/how-the-pandemic-inspired-mike-to-lose-245-pounds/\\">How the Pandemic Inspired Mike to Lose 245 pounds</a> appeared first on <a rel=\\"nofollow\\" href=\\"https://blog.myfitnesspal.com/\\">MyFitnessPal Blog</a>.</p>\\n", "pubDate": "2021-09-27 20:00:52", "author": "Amy Hoehn", "title": "How the Pandemic Inspired Mike to Lose 245 pounds", "enclosure": {"link": "https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-scaled.jpg"}, "content": "\\n<img width=\\"1024\\" height=\\"643\\" src=\\"https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-scaled-1024x643.jpg\\" class=\\"attachment-large size-large wp-post-image\\" alt=\\"How the Pandemic Inspired Mike to Lose 245 pounds\\" loading=\\"lazy\\" srcset=\\"https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-scaled-1024x643.jpg 1024w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-scaled-300x188.jpg 300w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-768x482.jpg 768w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-1536x964.jpg 1536w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-2048x1286.jpg 2048w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-500x315.jpg 500w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-752x472.jpg 752w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-269x169.jpg 269w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-444x280.jpg 444w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-299x188.jpg 299w\\" sizes=\\"(max-width: 1024px) 100vw, 1024px\\"><p>Mike went to bed every night thinking he was going to have a heart attack. Watch his inspiring story of weight loss and grit.</p>\\n<p>The post <a rel=\\"nofollow\\" href=\\"https://blog.myfitnesspal.com/watch/how-the-pandemic-inspired-mike-to-lose-245-pounds/\\">How the Pandemic Inspired Mike to Lose 245 pounds</a> appeared first on <a rel=\\"nofollow\\" href=\\"https://blog.myfitnesspal.com/\\">MyFitnessPal Blog</a>.</p>\\n", "link": "https://blog.myfitnesspal.com/watch/how-the-pandemic-inspired-mike-to-lose-245-pounds/", "guid": "https://blog.myfitnesspal.com/?post_type=video_hub&amp;p=50944", "thumbnail": "https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Mike-2880x1808-1-scaled-1024x643.jpg", "categories": []}, {"description": "\\n<img width=\\"1024\\" height=\\"643\\" src=\\"https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-scaled-1024x643.jpg\\" class=\\"attachment-large size-large wp-post-image\\" alt=\\"How Cam\\u2019s Weight Loss and Fitness Journey Saved His Son\\u2019s Life\\" loading=\\"lazy\\" srcset=\\"https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-scaled-1024x643.jpg 1024w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-scaled-300x188.jpg 300w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-768x482.jpg 768w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-scaled-1536x964.jpg 1536w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-scaled-2048x1286.jpg 2048w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-500x315.jpg 500w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-scaled-752x472.jpg 752w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-269x169.jpg 269w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-444x280.jpg 444w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-299x188.jpg 299w\\" sizes=\\"(max-width: 1024px) 100vw, 1024px\\"><p>When Cam Summerson\\u2019s son needed his help, the only way he could give it was by losing weight.</p>\\n<p>The post <a rel=\\"nofollow\\" href=\\"https://blog.myfitnesspal.com/watch/how-cams-weight-loss-and-fitness-journey-saved-his-sons-life/\\">How Cam\\u2019s Weight Loss and Fitness Journey Saved His Son\\u2019s Life</a> appeared first on <a rel=\\"nofollow\\" href=\\"https://blog.myfitnesspal.com/\\">MyFitnessPal Blog</a>.</p>\\n", "pubDate": "2021-09-23 16:00:03", "author": "Amy Hoehn", "title": "How Cam\\u2019s Weight Loss and Fitness Journey Saved His Son\\u2019s Life", "enclosure": {"link": "https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-scaled.jpg"}, "content": "\\n<img width=\\"1024\\" height=\\"643\\" src=\\"https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-scaled-1024x643.jpg\\" class=\\"attachment-large size-large wp-post-image\\" alt=\\"How Cam\\u2019s Weight Loss and Fitness Journey Saved His Son\\u2019s Life\\" loading=\\"lazy\\" srcset=\\"https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-scaled-1024x643.jpg 1024w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-scaled-300x188.jpg 300w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-768x482.jpg 768w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-scaled-1536x964.jpg 1536w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-scaled-2048x1286.jpg 2048w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-500x315.jpg 500w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-scaled-752x472.jpg 752w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-269x169.jpg 269w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-444x280.jpg 444w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-299x188.jpg 299w\\" sizes=\\"(max-width: 1024px) 100vw, 1024px\\"><p>When Cam Summerson\\u2019s son needed his help, the only way he could give it was by losing weight.</p>\\n<p>The post <a rel=\\"nofollow\\" href=\\"https://blog.myfitnesspal.com/watch/how-cams-weight-loss-and-fitness-journey-saved-his-sons-life/\\">How Cam\\u2019s Weight Loss and Fitness Journey Saved His Son\\u2019s Life</a> appeared first on <a rel=\\"nofollow\\" href=\\"https://blog.myfitnesspal.com/\\">MyFitnessPal Blog</a>.</p>\\n", "link": "https://blog.myfitnesspal.com/watch/how-cams-weight-loss-and-fitness-journey-saved-his-sons-life/", "guid": "https://blog.myfitnesspal.com/?post_type=video_hub&amp;p=51015", "thumbnail": "https://blog.myfitnesspal.com/wp-content/uploads/2021/09/Blog-2880-scaled-1024x643.jpg", "categories": []}, {"description": "\\n<img width=\\"1024\\" height=\\"643\\" src=\\"https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-scaled-1024x643.jpg\\" class=\\"attachment-large size-large wp-post-image\\" alt=\\"Can Intermittent Fasting Help Me Lose Weight?\\" loading=\\"lazy\\" srcset=\\"https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-scaled-1024x643.jpg 1024w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-scaled-300x188.jpg 300w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-768x482.jpg 768w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-scaled-1536x964.jpg 1536w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-scaled-2048x1286.jpg 2048w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-500x315.jpg 500w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-scaled-752x472.jpg 752w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-269x169.jpg 269w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-444x280.jpg 444w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-299x188.jpg 299w\\" sizes=\\"(max-width: 1024px) 100vw, 1024px\\"><p>Wondering if you should try intermittent fasting to lose weight? Registered Dietitian Whitney English explains that the claim that intermittent fasting can help you lose weight is only partially true.</p>\\n<p>The post <a rel=\\"nofollow\\" href=\\"https://blog.myfitnesspal.com/watch/can-intermittent-fasting-help-me-lose-weight/\\">Can Intermittent Fasting Help Me Lose Weight?</a> appeared first on <a rel=\\"nofollow\\" href=\\"https://blog.myfitnesspal.com/\\">MyFitnessPal Blog</a>.</p>\\n", "pubDate": "2021-09-22 16:00:16", "author": "Amy Hoehn", "title": "Can Intermittent Fasting Help Me Lose Weight?", "enclosure": {"link": "https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-scaled.jpg"}, "content": "\\n<img width=\\"1024\\" height=\\"643\\" src=\\"https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-scaled-1024x643.jpg\\" class=\\"attachment-large size-large wp-post-image\\" alt=\\"Can Intermittent Fasting Help Me Lose Weight?\\" loading=\\"lazy\\" srcset=\\"https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-scaled-1024x643.jpg 1024w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-scaled-300x188.jpg 300w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-768x482.jpg 768w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-scaled-1536x964.jpg 1536w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-scaled-2048x1286.jpg 2048w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-500x315.jpg 500w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-scaled-752x472.jpg 752w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-269x169.jpg 269w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-444x280.jpg 444w, https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-299x188.jpg 299w\\" sizes=\\"(max-width: 1024px) 100vw, 1024px\\"><p>Wondering if you should try intermittent fasting to lose weight? Registered Dietitian Whitney English explains that the claim that intermittent fasting can help you lose weight is only partially true.</p>\\n<p>The post <a rel=\\"nofollow\\" href=\\"https://blog.myfitnesspal.com/watch/can-intermittent-fasting-help-me-lose-weight/\\">Can Intermittent Fasting Help Me Lose Weight?</a> appeared first on <a rel=\\"nofollow\\" href=\\"https://blog.myfitnesspal.com/\\">MyFitnessPal Blog</a>.</p>\\n", "link": "https://blog.myfitnesspal.com/watch/can-intermittent-fasting-help-me-lose-weight/", "guid": "https://blog.myfitnesspal.com/?post_type=video_hub&amp;p=51019", "thumbnail": "https://blog.myfitnesspal.com/wp-content/uploads/2021/09/2880kitchen-13-scaled-1024x643.jpg", "categories": []}]'

    def test_feeds_languages_api(self):
        set_feeds("test_en")
        response = self.client.get('/feeds_languages_api', {}, follow=True)
        json_response = json.loads(response.content)
        self.assertTrue(json_response.get("success"))
        self.assertEqual(len(json_response.get("feeds_languages")), 1)
        self.assertGreaterEqual(len(json_response.get("feeds_languages").get("test_en")), 1)

    def test_general_information_api(self):
        response = self.client.get('/general_information_api', {}, follow=True)
        json_response = json.loads(response.content)
        self.assertTrue(json_response.get("success"))
        self.assertEqual(json_response.get("general_information").get("site_name"), settings.SITE_NAME)
        self.assertEqual(json_response.get("general_information").get("contact_email"), settings.CONTACT_EMAIL)
        self.assertEqual(len(json_response.get("general_information").keys()), 2)

    def test_set_feeds(self):
        self.assertFalse(FeedsLanguage.objects.filter(language="test_en").exists())
        set_feeds("test_en")
        feeds_added = set_feeds("test_en")
        self.assertGreaterEqual(feeds_added, 1)
        self.assertTrue(FeedsLanguage.objects.filter(language="test_en").exists())
        feeds_language = FeedsLanguage.objects.get(language="test_en")
        feeds_list = feeds_language.to_items_list()
        self.assertGreaterEqual(len(feeds_list), 1)
        self.assertGreaterEqual(datetime.datetime.now().replace(tzinfo=timezone.utc), feeds_language.last_update.replace(tzinfo=timezone.utc))
        self.assertEqual(FeedsLanguage.objects.filter(language="test_en").count(), 1)
        feeds_added = set_feeds("test_en_failed")
        self.assertGreaterEqual(feeds_added, 0)
        # self.assertRaises(Exception, set_feeds, "test_en_failed")
