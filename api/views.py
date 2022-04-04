from rest_framework.response import Response
from rest_framework import status, generics, permissions
from api.scan import get_info
from api.models import Result, Account
from api.serializers import ResultSerializer, AccountSerializer
from background_task.models import Task
from telethon.sync import TelegramClient
import asyncio


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


class GetAuthCode(generics.RetrieveAPIView):

    permission_classes = [permissions.IsAdminUser]

    def retrieve(self, request, *args, **kwargs):

        number = request.query_params.get('number')

        # try:
        #     Account.objects.get(name=number)
        #     return Response('Такой аккаунт уже есть', status=status.HTTP_201_CREATED)
        # except Account.DoesNotExist:
            # try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        client = TelegramClient(
            f'session_create/{number}',
            "3480264",
            "466a3ed928ef4dcc0936741b3b4cc745",
            loop=loop
        )
        client.connect()
        client.send_code_request(number)
        phone_code_hash = client.send_code_request(number).phone_code_hash
        # client.sign_in('380665971781', input('Enter code: '))
        account = Account.objects.create(name=number, phone_code_hash=phone_code_hash)
        client.disconnect()
        serializer = AccountSerializer(account)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
            # except Exception as e:
            #     print(e)
            #     return Response(f"Не удалось отправить код {str(e)}", status=status.HTTP_400_BAD_REQUEST)


class InputCode(generics.RetrieveAPIView):

    permission_classes = [permissions.IsAdminUser]

    def retrieve(self, request, *args, **kwargs):

        number = request.query_params.get('number')
        code = request.query_params.get('code')

        try:
            account = Account.objects.get(name=number)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            client = TelegramClient(
                f'session_create/{number}',
                "3480264",
                "466a3ed928ef4dcc0936741b3b4cc745",
                loop=loop
            )

            client.connect()
            try:
                client.sign_in(number, code, phone_code_hash=account.phone_code_hash)
                account.status = True
                account.save()
                print(client)
                client.disconnect()
                return Response('Удачно', status=status.HTTP_201_CREATED)
            except Exception as e:
                print(e)
                client.disconnect()
                return Response('Ошибка', status=status.HTTP_400_BAD_REQUEST)
        except Account.DoesNotExist:
            return Response("Вы ещё не отправили код!", status=status.HTTP_400_BAD_REQUEST)
