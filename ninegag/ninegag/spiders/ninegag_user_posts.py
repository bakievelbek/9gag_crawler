import pdb
import json
import scrapy

from scrapy.http import JsonRequest
from scrapy.exceptions import CloseSpider

from ninegag.ninegag.items import NinegagItem
from ninegag.ninegag.spiders import prework


class NinegagUserPostsSpider(scrapy.Spider):
    name = "ninegag_user_posts"
    allowed_domains = ["9gag.com"]

    def __init__(self, user='', limit=100, **kwargs):
        super(NinegagUserPostsSpider, self).__init__(**kwargs)

        self.user = user
        self.start_urls = [f'https://9gag.com/u/{self.user}/posts']
        self.post_count = 10
        self.limit = int(limit)

    def parse(self, response):
        post_ids = response.css('span#jsid-latest-entries::text').get().split(',')

        for post_id in post_ids:
            one_of_ten_url = f'https://9gag.com/gag/{post_id}'
            yield scrapy.Request(url=one_of_ten_url, callback=self.one_of_ten)

        next_cursor = f"after={','.join(reversed(post_ids[-3:]))}&c={self.post_count}"
        next_url = f'https://9gag.com/v1/user-posts/username/{self.user}/type/posts?{next_cursor}'
        if self.limit > 10:
            yield JsonRequest(url=next_url,
                              callback=self.parse_next,
                              method='POST')

    def one_of_ten(self, response):

        # pdb.set_trace()
        id_ = response.url.split('/')[-1]
        item = {

            'id': id_,
            'title': response.css(f'title::text').get(),
            'url': response.url,
            'images': prework.images(response=response, url=response.url),
            'interaction_statistics': prework.interaction_statistics(response=response, url=response.url),
            'created_at': prework.created_datetime(response=response, url=response.url)

        }
        yield NinegagItem(**item)

    def parse_next(self, response):
        data = json.loads(response.text)

        posts = data['data']['posts']
        for post in posts:
            item = {
                'id': post['id'],
                'title': post['title'],
                'url': post['url'],
                'images': post['images'],
                'interaction_statistics': {
                    'likes': post['upVoteCount'],
                    'dislikes': post['downVoteCount'],
                    'comments': post['commentsCount']
                },
                'created_at': prework.convert_ts(post['creationTs'])
            }
            yield NinegagItem(**item)
            self.post_count += 1

            if self.post_count >= int(self.limit):
                raise CloseSpider(reason='Maximum number of posts fetched')

        if 'nextCursor' in data['data']:
            next_cursor = data['data']['nextCursor']
            next_url = f'https://9gag.com/v1/user-posts/username/{self.user}/type/posts?{next_cursor}'
            yield JsonRequest(url=next_url, callback=self.parse_next, method='POST')
