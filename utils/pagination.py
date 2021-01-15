from rest_framework.pagination import PageNumberPagination


class ManualPageNumberPagination(PageNumberPagination):
    # 前端用户指定的页面key的名称
    # page_query_param = 'page'
    # 前端用户指定的每一页条数key的名称
    page_size_query_param = 'size'
    max_page_size = 20
    # 指定默认每一页2条数据
    # page_size = 10
    page_query_description = "第几页"
    page_size_query_description = "每页几条"

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        # "total_pages": 6,
        # "current_page_num": 2
        response.data["current_page_num"] = self.page.number
        response.data["total_pages"] = self.page.paginator.num_pages

        return response
