from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .libs.netty_ops import NettyOps
from .libs.netty_auth import NettyAuth
from .serializers import UserSerializer
from .models import User
from datetime import datetime, timedelta, timezone

import environ
env = environ.Env()
environ.Env.read_env()


@api_view(['GET'])
def get_device_from_slug(request, slug):
    command = request.GET["command"]
    user_id = request.GET["user_id"]
    try:
        my_user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return Response("Please authenticate your credentials", status=status.HTTP_200_OK)
    serializer = UserSerializer(my_user)
    user = serializer.data
    obj = NettyAuth()
    username, password, expiration = user["username"], obj.decrypt(
        user["password"]), user["expiration"]
    init_current_datetime = datetime.now()
    current_datetime = init_current_datetime.strftime("%d/%m/%y %H:%M:%S")

    current_datetime = datetime.strptime(current_datetime, '%d/%m/%y %H:%M:%S')
    expiration_datetime = datetime.strptime(expiration, '%d/%m/%y %H:%M:%S')
    print(current_datetime)
    print(expiration_datetime)
    if current_datetime > expiration_datetime:
        return Response("Please authenticate your credentials", status=status.HTTP_200_OK)
    else:
        obj = NettyOps(slug, command, username, password)
        output = obj.parser()
        if output["status_code"] == 200:
            return Response(output["result"], status=output["status_code"])
        else:
            return Response(output["error"], status=output["status_code"])


@api_view(['POST'])
def authenticate(request):
    user_id, username, password = request.data["user_id"], request.data["username"], request.data["password"]
    obj = NettyAuth(user_id=user_id, username=username, password=password)
    encrypted_password = obj.encrypt()
    str_pass = encrypted_password.decode()
    try:
        instance = User.objects.get(user_id=user_id)
        serializer = UserSerializer(instance)
        my_user = serializer.data
        updated_user = {}
        changed = 0

        if username != my_user["username"] or password != obj.decrypt(my_user["password"]):
            up_obj = NettyAuth(
                user_id=user_id, username=username, password=password)
            up_encrypted_password = up_obj.encrypt()
            up_str_pass = up_encrypted_password.decode()
            changed = 1
            updated_user = {
                "user_id": user_id,
                "username": username,
                "password": up_str_pass,
            }
        else:
            updated_user = {
                "user_id": user_id,
                "username": my_user["username"],
                "password": my_user["password"],
            }

        init_current_datetime = datetime.now()
        str_current_datetime = init_current_datetime.strftime(
            "%d/%m/%y %H:%M:%S")
        current_datetime = datetime.strptime(
            str_current_datetime, '%d/%m/%y %H:%M:%S')

        init_expiration_datetime = my_user["expiration"]
        expiration_datetime = datetime.strptime(
            init_expiration_datetime, '%d/%m/%y %H:%M:%S')

        if current_datetime > expiration_datetime:
            updated_user["creation"] = str_current_datetime
            up_init_expiration_datetime = init_current_datetime + \
                timedelta(minutes=5)
            up_expiration_datetime = up_init_expiration_datetime.strftime(
                "%d/%m/%y %H:%M:%S")
            updated_user["expiration"] = up_expiration_datetime
        else:
            updated_user["creation"] = my_user["creation"]
            updated_user["expiration"] = my_user["expiration"]

        up_serializer = UserSerializer(instance, data=updated_user)
        if up_serializer.is_valid():
            my_user = up_serializer.validated_data
            up_serializer.save()
        else:
            print(up_serializer.errors)
            return Response("Something went wrong...", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if changed:
            print("Credentials updated...")
        else:
            print("Credentials matched...")

        print("User: ", my_user)

        return Response("Saved", status=status.HTTP_200_OK)

    except User.DoesNotExist:
        init_current_datetime = datetime.now()
        current_datetime = init_current_datetime.strftime("%d/%m/%y %H:%M:%S")
        init_expiration_datetime = init_current_datetime + timedelta(minutes=5)
        expiration_datetime = init_expiration_datetime.strftime(
            "%d/%m/%y %H:%M:%S")
        user = {
            "username": username,
            "password": str_pass,
            "user_id": user_id,
            "creation": current_datetime,
            "expiration": expiration_datetime
        }
        try:
            serializer = UserSerializer(data=user)
        except:
            return Response("Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if serializer.is_valid():
            serializer.save()
            return Response("Saved", status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response("Something went wrong...", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'DELETE'])
def all_users(request):
    users = User.objects.all()
    if(request.method == "DELETE"):
        for i in range(0, len(users)):
            user = users[i]
            user.delete()
    return Response({"result": "Database Cleared"}, status=status.HTTP_200_OK)


@api_view(['GET'])
def user(request):
    pass
