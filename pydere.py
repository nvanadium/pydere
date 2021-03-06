# -*- coding: utf-8 -*-

import re
import time
import requests
from lxml import etree


__all__ = ['Post', 'Artist', 'Update', 'DanPost', 'DanArtist', 'IQDB', 'Pixiv']

class Post(object):
    
    '''Get info on a post on yande.re.'''
    
    def __init__(self, post_id):
        if not isinstance(post_id, int) and not post_id.isdigit():
            raise TypeError

        req = requests.get('https://yande.re/post.json',
                           params={'tags': 'id:' + str(post_id) + ' limit:1',
                           'api_version': '2', 'filter': '1',
                           'include_tags': '1', 'include_votes': '1',
                           'include_pools': '1'})
        self.post_json = req.json()
        self.post_info = self.post_json['posts'][0]
        self.post_tags = self.post_json['tags']
        self.post_id = int(post_id)
        del self.post_json

    @property
    def rating(self):
        return self.post_info['rating']

    @property
    def tags(self):
        return self.post_info['tags']

    @property
    def expanded_tags(self):
        tag_string = ''
        for k, v in self.post_tags.iteritems():
            tag_string = tag_string + ' ' + v + ':' + k
        return tag_string[1:]

    @property
    def width(self):
        return self.post_info['width']

    @property
    def height(self):
        return self.post_info['height']

    @property
    def dimensions(self):
        return str(self.width) + 'x' + str(self.height)

    @property
    def parent_id(self):
        if self.post_info['parent_id'] is not None:
            return self.post_info['parent_id']
        else:
            raise Exception

    def ParentPost(self):
        return Post(self.parent_id)

    @property    
    def uploader(self):
        return self.post_info['author']

    @property
    def preview(self):
        return self.post_info['preview_url']

    @property
    def source(self):
        s = self.post_info['source']
        return s if s else None

    @property
    def artist(self):
        artists = ''
        for k, v in self.post_tags.iteritems():
            if v == 'artist':
                artists += k + ' '
        return artists.strip() if artists else None
    
    @property
    def circle(self):
        circles = ''
        for k, v in self.post_tags.iteritems():
            if v == 'circle':
                circles += k + ' '
        return circles.strip() if circles else None


class Artist(object):
    
    '''
    Get info on a artist on yande.re.
    <name> can be an artist's name or website
    '''
    
    def __init__(self, name):
        req = requests.get('https://yande.re/artist.json',
                           params={'name': name})
        self.art_json = req.json()
        if len(self.art_json) == 1:
            self.unique = True
            self.art_info = self.art_json[0]
        else:
            self.unique = False
            self.art_info = None

    @property
    def name(self):
        if self.unique:
            return self.art_info['name']

    @property
    def urls(self):
        if self.unique:
            return self.art_info['urls']


class Update(object):
    
    '''
    Update the tags and/or source of a post on yande.re
    <session>: a requests session in which you've already logged in
    <token>: authenticity token
    <post>: an instance of the Post class
    '''
    
    def __init__(self, session, token, post, tags=None, source=None):
        self.session = session
        self.token = token
        self.post = post
        self.tags = tags
        self.source = source

    def update(self):
        url = 'https://yande.re/post/update.json'
        if self.tags:
            new_tags = self.post.tags + ' ' + self.tags
            print '    Updating tags:', new_tags
            params = {'id': self.post.post_id, 'post[tags]': new_tags,
                      'commit': 'Save changes',
                      'authenticity_token': self.token}
            response = self.session.post(url, data=params)
            print '    Response:', response.status_code, response.reason
        if self.source:
            print '    Updating source:', self.source
            params = {'id': self.post.post_id, 'post[source]': self.source,
                      'commit': 'Save changes',
                      'authenticity_token': self.token}
            response = self.session.post(url, data=params)
            print '    Response:', response.status_code, response.reason


class DanPost(Post):
    
    '''Get info on a post on danbooru.'''
    
    def __init__(self, post_id):
        if not isinstance(post_id, int) and not post_id.isdigit():
            raise TypeError

        req = requests.get('http://danbooru.donmai.us/post/index.json',
                           params={'tags': 'id:' + str(post_id)})
        self.post_json = req.json()
        self.post_info = self.post_json[0]
        self.post_id = int(post_id)
        del self.post_json

    @property
    def expanded_tags(self):
        return None
    
    @property
    def artist(self):
        return None
    
    @property
    def circle(self):
        return None


class DanArtist(Artist):
    
    '''
    Get info on a artist on danbooru.
    <name> can be an artist's name or website
    '''
    
    def __init__(self, name):
        req = requests.get('http://danbooru.donmai.us/artists.json',
                           params={'name': name})
        self.art_json = req.json()
        if len(self.art_json) == 1:
            self.unique = True
            self.art_info = self.art_json[0]
        else:
            self.unique = False
            self.art_info = None

    @property
    def urls(self):
        if self.unique:
            return [x['url'] for x in self.art_info['urls']]


class IQDB(object):
    
    '''
    Given an image url, find similar images on danbooru using iqdb.
    An image is defined to match if the similarity is greater than the cutoff.
    The matching image's danbooru id can also be obtained.
    '''
    
    def __init__(self, image_url):
        self.cutoff = 90.0
        url = 'http://danbooru.iqdb.org/index.xml?url='
        tree = etree.parse(url+image_url)
        self.root = tree.getroot()

    @property
    def similarity(self):
        return float(self.root.xpath('/matches/match')[0].attrib['sim'])

    @property
    def id(self):
        return int(self.root.xpath('/matches/match/post')[0].attrib['id'])
    
    @property
    def match(self):
        if self.similarity >= self.cutoff:
            return True
        else:
            return False


class Pixiv(object):
    
    '''
    Get the direct, full-size image url on pixiv, given an url with
    'member_illust' in it.
    The direct image url can then be used with Artist and DanArtist to find an
    artist's name.
    Requires a logged in requests session.
    '''
    
    def __init__(self, session, url):
        self.url = url
        if 'member_illust' in self.url:
            req = session.get(self.url)
            self.html = req.text
            self.root = etree.fromstring(self.html, etree.HTMLParser())
        else:
            self.html = None
            self.root = None
    
    @property
    def id(self):
        q = 'illust_id=\d+'
        m = re.search(q, self.url)
        if m:
            return self.url[m.start():m.end()].split('=')[-1]
    
    @property
    def source(self):
        if self.id and self.html:
            q = self.id + '_m\.(png|jpg)'
            m = re.search(q, self.html)
            if m:
                s = self.html[:m.end()].split('src="')[-1]
                return s.replace('_m.', '.')
            else:
                spans = [x for x in self.root.iter() if x.tag=='span']
                try:
                    error_span = [x for x in spans if x.attrib['class']=='error'][0]
                    if error_span != []:
                        print '    Pixiv message:', error_span.getchildren()[0].text
                    return None
                except:
                    print '    Getting direct linked failed'
                    return None

    @property
    def dimensions(self):
        if self.html:
            uls = [x for x in self.root.iter() if x.tag == 'ul']
            t = {'class': 'meta'}
            meta = [x for x in uls if x.attrib == t][0]
            return meta.getchildren()[1].text.replace(u'×', u'x')

    @property
    def width(self):
        if self.dimensions:
            return int(self.dimensions.split('x')[0])

    @property
    def height(self):
        if self.dimensions:
            return int(self.dimensions.split('x')[1])
    
    @property
    def date(self):
        if self.html:
            uls = [x for x in self.root.iter() if x.tag == 'ul']
            t = {'class': 'meta'}
            meta = [x for x in uls if x.attrib == t][0]
            fmt = '%d/%m/%Y %H:%M'
            posttime = time.strptime(meta.getchildren()[0].text, fmt)
            return posttime

    @property
    def profile(self):
        if self.html:
            url = 'http://www.pixiv.net'
            a = [x for x in self.root.iter() if x.tag == 'a']
            a = [x for x in a if x.attrib.has_key('class')]
            link = [x for x in a if x.attrib['class']=='user-link'][0]
            return url + link.attrib['href']

    @property
    def imgformat(self):
        if self.source:
            return self.source[-3:]
        
    @property
    def name(self):
        if self.html:
            h1 = [x for x in self.root.iter() if x.tag == 'h1']
            h1 = [x for x in h1 if x.attrib.has_key('class')]
            name = [x for x in h1 if x.attrib['class']=='user'][0]
            return name.text
