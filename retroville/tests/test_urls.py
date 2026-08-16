from django.urls import resolve, reverse


class TestUrls:
    def test_ping_url(self):
        # path = reverse('ping', kwargs={'pk': 1})
        path = reverse("ping")
        assert resolve(path).view_name == "ping"
