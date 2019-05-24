class Pagination(object):
    def __init__(self, data_length, current_page,get_parameter, data_display=7, max_page=5):
        self.data_length = data_length
        self.current_page = current_page
        self.data_display = data_display
        self.max_page = max_page
        self.parameter = get_parameter
        self.half_page = self.max_page // 2

        # print(self.parameter.urlencode())

        # 第一次请求页面或者非法数据均设置成第一页
        try:
            self.current_page = int(self.current_page)
            if self.current_page < 1:
                self.current_page = 1
        except Exception as e:
            self.current_page = 1
        # 获取需要分的页数
        self.page_num, more = divmod(self.data_length, self.data_display)
        if more:
            self.page_num += 1

    @property
    def start(self):
        """
        数据切片的起始值
        """
        return (self.current_page - 1) * self.data_display

    @property
    def end(self):
        '''
        数据切片的结束的索引值
        '''
        return self.current_page * self.data_display

    @property
    def core(self):
        if self.page_num < self.max_page:
            start_page = 1
            end_page = self.page_num
        elif self.current_page <= self.half_page:
            start_page = 1
            end_page = self.max_page
        elif self.current_page + self.half_page > self.page_num:
            start_page = self.page_num - self.max_page + 1
            end_page = self.page_num
        else:
            start_page = self.current_page - self.half_page
            end_page = self.current_page + self.half_page

        page_list = []

        # 在最左侧添加上一页的li标签
        if self.current_page == 1:
            page_list.append('<li class="disabled" ><a>&laquo;</a></li>')
        else:
            self.parameter['page'] = self.current_page - 1
            page_list.append('<li><a href="?%s">&laquo;</a></li>' % (self.parameter.urlencode()))

        for i in range(start_page, end_page + 1):
            self.parameter['page'] = i
            if i == self.current_page:
                page_list.append('<li class="active"><a href="?%s">%s</a></li>' % (self.parameter.urlencode(), i))
            else:
                page_list.append('<li><a href="?%s">%s</a></li>' % (self.parameter.urlencode(), i))
        # 在最右侧添加下一页的li标签
        if self.current_page == self.page_num or self.page_num == 0:
            page_list.append('<li class="disabled" ><a>&raquo;</a></li>')
        else:
            self.parameter['page'] = self.current_page + 1
            page_list.append('<li><a href="?%s">&raquo;</a></li>' % (self.parameter.urlencode()))

        return ''.join(page_list)
