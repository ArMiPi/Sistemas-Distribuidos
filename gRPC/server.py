from concurrent import futures

import grpc

import auth_pb2_grpc
import catalog_pb2_grpc
import orders_pb2_grpc
from auth_service import AuthService
from catalog_service import CatalogService
from order_service import OrderService


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    catalog_pb2_grpc.add_CatalogServiceServicer_to_server(CatalogService(), server)
    orders_pb2_grpc.add_OrderServiceServicer_to_server(OrderService(), server)
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
