from django.utils import timezone
from datetime import timedelta
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from .serializers import MatchingRoomSerializer
from .models import MatchingRoom
from djangochannelsrestframework.mixins import ListModelMixin
from djangochannelsrestframework.mixins import RetrieveModelMixin
from djangochannelsrestframework.mixins import UpdateModelMixin
from djangochannelsrestframework.decorators import action, list_action


class MatchingRoomConsumer(
        ListModelMixin,
        RetrieveModelMixin,
        UpdateModelMixin,
        GenericAsyncAPIConsumer
    ):
    queryset = MatchingRoom.objects.filter(modified_at__gt=timezone.now()-timedelta(hours=24))
    serializer_class = MatchingRoomSerializer

    # @action()
    # async def send_email(self, pk=None, to=None, **kwargs):
    #     user = await database_sync_to_async(self.get_object)(pk=pk)
    #     # ... do some stuff
    #     # remember to wrap all db actions in `database_sync_to_async`
    #     return {}, 200  # return the contenct and the response code.
    #
    # @action()  # if the method is not async it is already wrapped in `database_sync_to_async`
    # def publish(self, pk=None, **kwargs):
    #     user = self.get_object(pk=pk)
    #     # ...
    #     return {'pk': pk}, 200
