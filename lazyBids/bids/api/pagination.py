
from rest_framework.response import Response
from rest_framework import pagination
from django.conf import settings

class BidsPagination(pagination.PageNumberPagination):
    page_size = settings.CUSTOM_PAGINATION.get('bids').get('page_size')
    page = settings.CUSTOM_PAGINATION.get('bids').get('default_page')

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total_count': self.page.paginator.count,
            'page': int(self.get_page_number(self.request, self.django_paginator_class)),
            'bids': data
        })