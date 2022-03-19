from django.views import View
from django.http.request import HttpRequest, QueryDict
from django.http.response import JsonResponse

from user_list.models import db_create_user, db_delete_user, db_update_user


class UserList(View):
    """用户信息 视图"""

    def get(self, request: HttpRequest):
        """查询"""
        raise NotImplementedError

    def post(self, request: HttpRequest):
        """增加"""
        username = request.POST.get('username')
        password = request.POST.get('password')
        res = db_create_user(username, password)
        return JsonResponse(res)

    def patch(self, request: HttpRequest):
        """更新（修改密码）"""
        data = QueryDict(request.body)
        username = data.get('username')
        password = data.get('password')
        res = db_update_user(username, password)
        return JsonResponse(res)

    def delete(self, request: HttpRequest):
        """删除"""
        data = QueryDict(request.body)
        username = data.get('username')
        res = db_delete_user(username=username)
        return JsonResponse(res)
