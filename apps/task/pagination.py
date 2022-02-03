from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class DefaultPaginator(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'page': self.page.number,
            'per_page': self.page.paginator.per_page,
            'num_pages': self.page.paginator.num_pages,
            'results': data
        })
