__author__ = 'OllyD'

from rest_framework import pagination

class StandardResultsPagination(pagination.PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 1000