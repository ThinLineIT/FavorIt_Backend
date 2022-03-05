from django.test.client import Client
from django.urls import reverse

client = Client()


def test_hello():
    print(reverse("ninja:hello_world"))
    response = client.get(path=reverse("ninja:hello_world"))
    result = response.json()
    assert result["hello"] == "hello"
    assert result["world"] == "world"
