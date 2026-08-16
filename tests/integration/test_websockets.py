import pytest
from channels.testing import WebsocketCommunicator
from rest_framework.authtoken.models import Token

from retroville.asgi import application
from tests.factories import UserFactory


@pytest.mark.integration
@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_websocket_rejects_anonymous():
    communicator = WebsocketCommunicator(application, "/ws/chat/lobby/")
    connected, code = await communicator.connect()
    assert connected is False or code in {1000, 4401, 403, 1006}
    await communicator.disconnect()


@pytest.mark.integration
@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_websocket_auth_message_and_disconnect():
    user = UserFactory()
    token = Token.objects.get(user=user)
    communicator = WebsocketCommunicator(application, f"/ws/chat/lobby/?token={token.key}")
    connected, _code = await communicator.connect()
    assert connected
    await communicator.send_json_to({"message": "hello"})
    response = await communicator.receive_json_from()
    assert response["message"] == "hello"
    await communicator.disconnect()


@pytest.mark.integration
@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_websocket_oversized_payload_closes():
    user = UserFactory()
    token = Token.objects.get(user=user)
    communicator = WebsocketCommunicator(application, f"/ws/chat/lobby/?token={token.key}")
    connected, _code = await communicator.connect()
    assert connected
    await communicator.send_to(text_data='{"message":"' + ("x" * 5000) + '"}')
    close = await communicator.receive_output()
    assert close["type"] == "websocket.close"
    await communicator.disconnect()
