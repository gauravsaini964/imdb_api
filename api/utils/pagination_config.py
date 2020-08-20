from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class PostLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100
    offset_query_param = "offset"


class PostPageNumberPagination(PageNumberPagination):
    page_size = 10
