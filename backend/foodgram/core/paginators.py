from rest_framework.pagination import PageNumberPagination


class LimitedPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'limit'
