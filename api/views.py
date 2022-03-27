from rest_framework.response import Response
from rest_framework import status, generics, permissions
from api.scan import get_info
from api.models import Result
from api.serializers import ResultSerializer
from background_task.models import Task


class GetInfoApiView(generics.RetrieveAPIView):

    permission_classes = [permissions.IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        number = request.query_params.get('number')
        try:
            result = Result.objects.get(number=number)
            serializer = ResultSerializer(result)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Result.DoesNotExist:
            if len(Task.objects.filter(task_params__contains=number)) == 0:
                get_info(number)
                return Response("Ваш запрос принят в обработку", status=status.HTTP_201_CREATED)
            else:
                return Response("Ваш запрос уже обрабатываеться", status=status.HTTP_200_OK)
