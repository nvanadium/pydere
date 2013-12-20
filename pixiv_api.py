#! /usr/bin/env python

import re
import lxml
import requests


class Pixiv(object):

    def __init__(self, url):
        self.url = url
        keys = ['img_id', 'user_id', 'ext', 'title', 'unknown1', 'user_name',
                'sample_url', 'unused0', 'unused1', 'mobile_url', 'unused2',
                'unused3', 'date', 'tags', 'tools', 'votes', 'points', 'reads',
                'description', 'manga_pages', 'unused4', 'unused5', 'unknown3',
                'unknown4', 'user_login_id', 'unused6', 'unknown5', 'unused7',
                'unused8', 'profile_img', 'unused9']
        api_url = 'http://spapi.pixiv.net/iphone/illust.php'
        if self.img_id:
            params = {'illust_id': self.img_id, 'p': 1}
            response = requests.get(api_url, params=params)
            values = response.text.split(',')
            values[-1] = values[-1].replace('\n', '')
            self.post_info = {}
            for i in range(len(keys)):
                self.post_info[keys[i]] = values[i].replace('"', '')
        else:
            self.post_info = None

    def __str__(self):
        s = u''
        t = u'    '
        s += u'<Pixiv object>\n'
        s += t + u'url: ' + self.url + u'\n'
        if self.img_id:
            keys = self.post_info.keys()
            keys.sort()
            for key in keys:
                s += t + key.ljust(14) + u': ' + self.post_info[key] + u'\n'
        return s

    @property
    def img_id(self):
        if 'member_illust' in self.url:
            pattern = 'illust_id=(\d+)'
        else:
            pattern = '\/(\d+)(_m|_s|_big_p\d+)?\.(png|jpg)'
        m = re.search(pattern, self.url)
        if m:
            return m.groups()[0]

    @property
    def ext(self):
        if self.post_info:
            return self.post_info['ext']

    @property
    def user_login_id(self):
        if self.post_info:
            return self.post_info['user_login_id']

    @property
    def sample_url(self):
        if self.post_info:
            return self.post_info['sample_url']

    @property
    def mobile_url(self):
        if self.post_info:
            return self.post_info['mobile_url']

    @property
    def source(self):
        if self.post_info:
            temp = self.mobile_url.replace('mobile/', '')
            pattern = self.img_id + '.+' + self.ext + '$'
            repl = self.img_id + '.' + self.ext
            return re.sub(pattern, repl, temp)

    @property
    def date(self):
        if self.post_info:
            return self.post_info['date']

    @property
    def user_id(self):
        if self.post_info:
            return self.post_info['user_id']

    @property
    def profile(self):
        if self.post_info:
            url = 'http://www.pixiv.net/member.php?id='
            return url + self.user_id

    @property
    def name(self):
        if self.post_info:
            return self.post_info['user_name']

    @property
    def manga_pages(self):
        if self.post_info:
            return self.post_info['manga_pages']

    @property
    def dimensions(self):
        if self.manga_pages == '':
            return


if __name__ == '__main__':
    import rlcompleter
    import readline
    readline.parse_and_bind('tab: complete')
    #url = 'http://i2.pixiv.net/img06/img/roast/37664499.jpg'
    #url = 'http://i2.pixiv.net/img06/img/roast/37664499_m.jpg'
    url = 'http://i2.pixiv.net/img06/img/roast/37664499_s.jpg'
    #url = 'http://i2.pixiv.net/img06/img/roast/37664499_big_p10.jpg'
    #url = 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id=37664499'
    #url = 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id=34959240'
    p = Pixiv(url)
