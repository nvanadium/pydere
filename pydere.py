import requests
from xml.dom.minidom import parseString

__all__ = ['Post', 'Artist', 'DanPost', 'IQDB']

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
        return str(self.Width()) + 'x' + str(self.Height())

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
        if s == '':
            return None
        else:
            return s

    @property
    def artist(self):
        artists = ''
        for k, v in self.post_tags.iteritems():
            if v == 'artist':
                artists += k
        if artists == '':
            return None
        else:
            return artists
    
    @property
    def circle(self):
        circles = ''
        for k, v in self.post_tags.iteritems():
            if v == 'circle':
                circles += k
        if circles == '':
            return None
        else:
            return circles


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
        else:
            return None

    @property
    def urls(self):
        if self.unique:
            return self.art_info['urls']
        else:
            return None


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


class IQDB(object):
    
    '''
    Given an image url, find similar images on danbooru using iqdb.
    An image is defined to match if the similarity is greater than the cutoff.
    The matching image's danbooru id can also be obtained.
    '''
    
    def __init__(self, image_url):
        self.cutoff = 90.0
        req = requests.get('http://danbooru.iqdb.org/index.xml',
                           params={'url': image_url})
        self.xml = parseString(req.text)

    @property
    def similarity(self):
        return float(self.xml.getElementsByTagName('match')[0]
                     .getAttribute('sim'))

    @property
    def id(self):
        return int(self.xml.getElementsByTagName('post')[0]
                   .getAttribute('id'))
    
    @property
    def match(self):
        if self.similarity >= self.cutoff:
            return True
        else:
            return False