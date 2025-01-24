import pytest
from logs.filter.access_resource import AccessResource

@pytest.mark.parametrize(
    "resource",
    [
        ("https://fake-domain/fake-resource/2099.1/12345"),
        ("https://fake-domain/fake-resource/2099.2/54321"),
        ("https://fake-domain/fake-resource/2099.3/56347"),
        ("https://fake-domain/fake-resource/2099.4/345678"),
        ("https://fake-domain/fake-resource/2117/314522"),
    ]
)
def test_access_resource_with_correct_handle(resource: str):

    assert AccessResource.filter(resource) == True


@pytest.mark.parametrize(
    "resource",
    [
        ("https://fake-domain/fake-resource/2099.1/12345/2117/51432"),
        ("https://fake-domain/fake-resource/2099.2/54321/2099.4/33123"),
    ]
)
def test_access_resource_with_multiple_handle(resource: str):

    assert AccessResource.filter(resource) == True


@pytest.mark.parametrize(
    "resource",
    [
        ("https://fake-domain/fake-resource/2099.5/12345"),
        ("https://fake-domain/fake-resource/2134/54321"),
    ]
)
def test_access_resource_with_incorrect_handle(resource: str):

    assert AccessResource.filter(resource) == False


def test_access_resource_with_empty_resource():

    resource = ""
    assert AccessResource.filter(resource) == False
