"""
Management command to manage feeds.
"""
from home.utils import set_feeds
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = """
        Save feeds from remote servers in FeedsLanguage model
    """

    option_list = (
        make_option(
            '-l',
            '--language',
            dest='language',
            default=None,
            help='Choose the language witch will be linked to feeds.'
        ),
    )
    def add_arguments(self, parser):
        parser.add_argument('--language', type=str)
        parser.add_argument('-l', type=str)

    def handle(self, *args, **options):
        if options.get("language") or options.get("l"):
            language = options.get("language") or options.get("l")
            if not settings.LANGUAGES_DICT.get(language):
                raise CommandError('Language code is not valid. Choose one of those values: {}.'.format(', '.join(settings.LANGUAGES_DICT.keys())))
            feeds_added = set_feeds(language)
            print("{} feeds added for language: {}".format(str(feeds_added), settings.LANGUAGES_DICT.get(language)))
        else:
            raise CommandError('Language code is required.')



