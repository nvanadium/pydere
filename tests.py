#!/usr/bin/env python

import unittest
import ConfigParser
import requests
from pydere import *

class TestPydereMethods(unittest.TestCase):
    
    def test_post_rating(self):
        self.assertEqual(post.rating, 's')

    def test_post_tags(self):
        self.assertEqual(post.tags,
            '13 amene calendar dress inugami_kira mitsuki_(13) necotoxin')

    def test_post_width(self):
        self.assertEqual(post.width, 2127)

    def test_post_height(self):
        self.assertEqual(post.height, 2226)

    def test_post_dimensions(self):
        self.assertEqual(post.dimensions, '2127x2226')

    def test_post_uploader(self):
        self.assertEqual(post.uploader, 'WtfCakes')

    def test_post_preview(self):
        self.assertEqual(post.preview,
            'https://kotonoha.yande.re/data/preview/da/2d/da2d7d478847085b337b426e9e02feea.jpg')

    def test_post_source(self):
        self.assertEqual(post.source, None)

    def test_post_artist(self):
        self.assertEqual(post.artist, 'inugami_kira')

    def test_post_circle(self):
        self.assertEqual(post.circle, 'necotoxin')

    def test_artist_name(self):
        self.assertEqual(artist.name, 'inugami_kira')

    def test_artist_urls(self):
        urls = ["http://www.kiss.ac/~vanilla/toxin/",
                "http://i1.pixiv.net/img23/img/kila_inugami/",
                "http://www.pixiv.net/member.php?id=465146"]
        self.assertEqual(artist.urls, urls)

    def test_danartist_urls(self):
        urls = ["http://dic.nicovideo.jp/id/4779564",
                "http://yfrog.com/user/kilacco/photos",
                "http://www.pixiv.net/member.php?id=465146",
                "http://www.kiss.ac/~vanilla/toxin/",
                "http://twitter.com/kilacco_info",
                "http://twitter.com/kilacco",
                "http://twitpic.com/photos/kilacco",
                "http://p.twipple.jp/user/kilacco",
                "http://i1.pixiv.net/img23/img/kila_inugami/"]
        self.assertEqual(danartist.urls, urls)

    def test_iqdb_similarity(self):
        self.assertEqual(iqdb.similarity, 99.233183)

    def test_iqdb_match(self):
        self.assertEqual(iqdb.match, True)

    def test_iqdb_id(self):
        self.assertEqual(iqdb.id, 1481429)

    def test_pixiv_id(self):
        self.assertEqual(pixiv.id, '37664499')

    def test_pixiv_source(self):
        self.assertEqual(pixiv.source,
                         'http://i2.pixiv.net/img06/img/roast/37664499.jpg')
    
    def test_pixiv_profile(self):
        self.assertEqual(pixiv.profile,
                         'http://www.pixiv.net/member.php?id=52416')
    
    def test_pixiv_imgformat(self):
        self.assertEqual(pixiv.imgformat, 'jpg')

    def test_pixiv_dimensions(self):
        self.assertEqual(pixiv.dimensions, '850x1200')

    def test_pixiv_width(self):
        self.assertEqual(pixiv.width, 850)
        
    def test_pixiv_height(self):
        self.assertEqual(pixiv.height, 1200)


def Login(base, url, params, cookie=None):
    '''Create a session and log in.'''
    print 'Logging in to', base
    s = requests.Session()
    resp = s.post(base + url, data=params, cookies=cookie)
    print 'Login response:', resp.status_code, resp.reason
    return s, resp


if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.read('config.cfg')
    pix_base = 'https://www.secure.pixiv.net'
    pix_url = '/login.php'
    pix_params = {'mode': 'login', 'pixiv_id': config.get('pixiv', 'username'),
                  'pass': config.get('pixiv', 'password')}
    pix_session, resp = Login(pix_base, pix_url, pix_params)
    
    post = Post(200000)
    artist = Artist('inugami_kira')
    danartist = DanArtist('inugami_kira')
    iqdb = IQDB('https://yomi.yande.re/data/preview/e2/2d/e22dfba71e8e32797c6b7b89560739dd.jpg')
    pixiv = Pixiv(pix_session, 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id=37664499')
    
    unittest.main()