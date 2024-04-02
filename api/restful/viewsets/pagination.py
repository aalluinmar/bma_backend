from rest_framework.pagination import LimitOffsetPagination


class CustomPagination(LimitOffsetPagination):
    """
    Set default pagination limit and offset value
    """
    default_limit = 25  # Set the default page size
    max_limit = 100  # Set the maximum page size
    limit_query_param = 'limit'  # Set the query parameter for limit
    offset_query_param = 'offset'  # Set the query parameter for offset
