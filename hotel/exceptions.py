from rest_framework.views import exception_handler

statusMessages = {
    'not_authenticated': 'Учетные данные не были предоставлены.',
    'authentication_failed': 'Неверные учетные данные.',
    'permission_denied': 'У вас нет прав для выполнения этого действия.',
    'not_found': 'Страница или объект не найдены.',
    'method_not_allowed': 'Метод не разрешен.',
    'throttled': 'Слишком много запросов. Попробуйте позже.',
}

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if response.data.get('detail').code is not None:
            code = response.data.get('detail').code
            if code in statusMessages:
                response.data['detail'] = statusMessages[code]

    return response
