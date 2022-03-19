from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

SUCCESS_MESSAGE = 'success'
RESPONSE_CODE = {
    'success': 0,
    'failed': 1
}

def db_create_user(username, password, is_active: bool = True):
    """创建用户"""
    try:
        User.objects.create_user(username=username, password=password, is_active=is_active)
    except  IntegrityError:
        return {"code": RESPONSE_CODE['failed'], "message": f"{username}用户已存在"}  # 已经创建，无法重复创建
    else:
        return {"code": RESPONSE_CODE['success'], "message": SUCCESS_MESSAGE}


def db_delete_user(username):
    """删除用户"""
    try:
        User.objects.get(username=username).delete()
        return {"code": RESPONSE_CODE['success'], "message": SUCCESS_MESSAGE}
    except ObjectDoesNotExist:
        return {"code": RESPONSE_CODE['failed'], "message": f'{username}用户不存在！'}


def db_update_user(username, password):
    """修改密码"""
    try:
        user_obj = User.objects.get(username=username)
        user_obj.set_password(password)
        user_obj.save()
        return {'code': RESPONSE_CODE['success'], "message": SUCCESS_MESSAGE}
    except ObjectDoesNotExist:
        return {"code": RESPONSE_CODE['failed'], "message": f'{username}用户不存在！'}
