# lazyBids

This is the default app that gets created by default whenever a django project gets created. Most of the files are used to configure the whole application. In my case i had to edit [settings.py](settings.py) and [urls](urls.py)

# Settings

As the name suggest this app contains all the settings that can be configured.
The first thing that has to be done in a DRF projects is to install DRF:smile:.
```python

INSTALLED_APPS = [
    ...
    # rest-framework
    'rest_framework',
    'rest_framework.authtoken',
    ...
]
```

Then also your created apps and 3rd party libraries have to be installed:
```python
INSTALLED_APPS = [
    ...
    # Created apps
    'users',  # Custom User models and APIs
    'bids',
    'auctions',

    # External libraries
    'djoser',
    'corsheaders',
    ...
]
```

There are many settings and they are pretty much self-explainatory, however there are plenty of examples and documentaions.
You can also write your settings like i did for the pagination
```python
CUSTOM_PAGINATION = {
    'bids' : {
        'page_size' : 5,
        'default_page' : 1
    },
    'auctions' :{
        'page_size' : 8,
        'default_page' : 1
    }
}
```

Then use it like this:
```python
#auctions/api/pagination.py
from django.conf import settings

class AuctionsPagination(pagination.PageNumberPagination):

    page_size = settings.CUSTOM_PAGINATION.get('auctions').get('page_size')
    page = settings.CUSTOM_PAGINATION.get('auctions').get('default_page')

    ...
```

# Urls

This is the file that defines the endpoints for each app that it is included in the `urlpatterns` array. The best way to use it is to include the urls.py file of each app where another `urlpatterns` array specifies all the view's endpoints