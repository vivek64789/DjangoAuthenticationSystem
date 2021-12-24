from django.urls import reverse, resolve


class TestAccountUrls:
    def test_register_urls(self):
        path = reverse('register')
        assert resolve(path).view_name == 'register'

    def test_login_urls(self):
        path = reverse('register')
        assert resolve(path).view_name == 'register'

    def test_logout_urls(self):
        path = reverse('logout')
        assert resolve(path).view_name == 'logout'

    def test_validate_email_urls(self):
        path = reverse('validate-email')
        assert resolve(path).view_name == 'validate-email'

    def test_activateUser_urls(self):
        path = reverse('activateUser')
        assert resolve(path).view_name == 'activateUser'
