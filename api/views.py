from rest_framework.response import Response
from rest_framework import status, generics, permissions
from api.scan import get_info
from api.models import Result
from api.serializers import ResultSerializer


class GetInfoApiView(generics.RetrieveAPIView):

    permission_classes = [permissions.IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        number = request.query_params.get('number')
        try:
            result = Result.objects.get(number=number)
            serializer = ResultSerializer(result)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Result.DoesNotExist:
            result, file = get_info(number)
            if file is None:
                result = Result.objects.create(number=number, text=result)
                serializer = ResultSerializer(result)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                result = Result.objects.create(number=number, text=result, file=file)
                serializer = ResultSerializer(result)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
