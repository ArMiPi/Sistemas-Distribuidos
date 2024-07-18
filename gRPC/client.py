import grpc

import auth_pb2
import auth_pb2_grpc
import catalog_pb2
import catalog_pb2_grpc
import orders_pb2
import orders_pb2_grpc


def run():
    with grpc.insecure_channel("localhost:50050") as channel:
        catalog_stub = catalog_pb2_grpc.CatalogServiceStub(channel)
        response = catalog_stub.ListBooks(catalog_pb2.Empty())
        print("Books in catalog:")
        for book in response.books:
            print(
                f"Title: {book.title}, Author: {book.author}, Year: {book.year}, "
                f"Stock: {book.stock}, Price: {book.price}"
            )

    with grpc.insecure_channel("localhost:50051") as channel:
        auth_stub = auth_pb2_grpc.AuthServiceStub(channel)
        response = auth_stub.Register(
            auth_pb2.RegisterRequest(username="testuse1r", password="testpassword")
        )
        print(f"Auth Token: {response.token}")

    with grpc.insecure_channel("localhost:50051") as channel:
        order_stub = orders_pb2_grpc.OrderServiceStub(channel)
        response = order_stub.PlaceOrder(
            orders_pb2.OrderRequest(
                user_id="testuser",
                items=[orders_pb2.OrderItem(title="Book One", quantity=1)],
            )
        )
        print(f"Order ID: {response.order_id}")


if __name__ == "__main__":
    run()
