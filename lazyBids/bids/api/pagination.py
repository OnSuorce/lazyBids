
from rest_framework.response import Response
from rest_framework import pagination

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 5

class BidsPagination(pagination.PageNumberPagination):
    page_size = DEFAULT_PAGE_SIZE
    page = DEFAULT_PAGE

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total_count': self.page.paginator.count,
            'page': int(self.request.GET.get('page', DEFAULT_PAGE)), 
            'page_size': int(self.request.GET.get('page_size', self.page_size)),
            'bids': data
        })