def user_context(request):
    """Контекстный процессор для фиктивного авторизованного пользователя"""
    class MockUser:
        def __init__(self):
            self.username = "ziontab"
            self.is_authenticated = True #False чтобы не авторизованный режзим
            self.email = "ziontab@example.com"
    
    return {
        'user': MockUser()
    }