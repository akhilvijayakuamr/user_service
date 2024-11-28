import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'user_service.settings')

import django

django.setup()

import grpc
from concurrent import futures
from proto import user_service_pb2
from proto import user_service_pb2_grpc
import time
from .service import UserServiceServicer


server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
user_service_pb2_grpc.add_UserServiceServicer_to_server(UserServiceServicer(), server)

server.add_insecure_port('[::]:50051')
server.start()


try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)