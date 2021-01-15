def jwt_response_payload_handler(token, user=None, request=None):
    """
    对返回的数据进行重写
    添加用户的信息
    :param token:
    :param user:
    :param request:
    :return:
    """
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }

