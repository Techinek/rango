import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from rango.models import Category, Page


def populate():
    python_pages = [
        {'title': 'Official Python Tutorial',
         'url': 'http://docs.python.org/3/tutorial/'},
        {'title': 'How to Think like a Computer Scientist',
         'url': 'http://www.greenteapress.com/thinkpython/'},
        {'title': 'Learn Python in 10 Minutes',
         'url': 'http://www.korokithakis.net/tutorials/python/'},

    ]

    fastapi_pages = [
        {'title': 'Official FastApi tutorial',
         'url': 'https://fastapi.tiangolo.com/'},
        {'title': 'Source code of FastApi',
         'url': 'https://github.com/tiangolo/fastapi'}
    ]

    django_pages = [
        {'title': 'Official Django Tutorial',
         'url': 'https://docs.djangoproject.com/en/2.1/intro/tutorial01/'},
        {'title': 'Django Rocks',
         'url': 'http://www.djangorocks.com/'},
        {'title': 'How to Tango with Django',
         'url': 'http://www.tangowithdjango.com/'}]

    other_pages = [
        {'title': 'Bottle',
         'url': 'http://bottlepy.org/docs/dev/'},
        {'title': 'Flask',
         'url': 'http://flask.pocoo.org'}]

    cats = {'Python': {'pages': python_pages},
            'Django': {'pages': django_pages},
            'Other Frameworks': {'pages': other_pages},
            'FastApi': {'pages': fastapi_pages}
            }

    for cat, cat_data in cats.items():
        c = add_cat(cat)
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'])

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')


def add_page(cat, title, url, views=1):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p


def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    if c.name == 'Python':
        c.likes = 64
        c.views = 128
        c.save()
    if c.name == 'Django':
        c.likes = 32
        c.views = 64
        c.save()
    if c.name == 'Other Frameworks':
        c.likes = 16
        c.views = 32
        c.save()
    if c.name == 'FastApi':
        c.likes = 8
        c.views = 15
        c.save()
    return c


if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()
