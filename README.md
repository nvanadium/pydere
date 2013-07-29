pydere  
======  

A simple python interface to the yande.re, danbooru and iqdb APIs. 

- Based on https://github.com/actown/pymoe  
- Uses @property to make most things attributes for ease of use.  

Examples  
--------  

Get some info on a post  

    p = Post(i)  
    print 'post:', i  
    print '    artist:', p.artist  
    print '    circle:', p.circle  
    print '    source:', p.source  
    print '    preview:', p.preview  

Search for an artist's name given an url e.g. from pixiv  

    image_url = 'http://i1.pixiv.net/img83/img/luminocity/35089455_m.jpg'  
    a = Artist(image_url)  
    print a.name  

Search on danbooru for similar images using iqdb  

    i = IQDB(image_url)  
    print i.similarity  
    print i.match  

Get a direct image url from pixiv  

    url = 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id=36334142'  
    p = Pixiv(url)  
    print p.source  

