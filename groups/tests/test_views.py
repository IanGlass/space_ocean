from django.contrib.auth.models import User
from django.contrib.messages import get_messages

import pytest

from groups.models import Group, GroupMember


@pytest.mark.django_db
def test_list_groups(client):
    response = client.get('/groups/')
    assert response.status_code == 200
