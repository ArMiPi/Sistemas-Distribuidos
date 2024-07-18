import uuid
from datetime import datetime

import grpc

import orders_pb2
import orders_pb2_grpc


class OrderService(orders_pb2_grpc.OrderServiceServicer):
    def __init__(self):
        self.orders = {}

    def PlaceOrder(self, request, context):
        order_id = str(uuid.uuid4())
        order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.orders[order_id] = {
            "user_id": request.user_id,
            "items": [
                {"title": item.title, "quantity": item.quantity}
                for item in request.items
            ],
            "order_date": order_date,
        }
        return orders_pb2.OrderResponse(order_id=order_id)

    def GetOrderDetails(self, request, context):
        order = self.orders.get(request.order_id)
        if not order:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Order not found")
            return orders_pb2.OrderDetailsResponse()
        items = [
            orders_pb2.OrderItem(title=item["title"], quantity=item["quantity"])
            for item in order["items"]
        ]
        return orders_pb2.OrderDetailsResponse(
            order_id=request.order_id,
            user_id=order["user_id"],
            items=items,
            order_date=order["order_date"],
        )

    def ListOrders(self, request, context):
        user_orders = [
            orders_pb2.OrderSummary(
                order_id=order_id, titles=[item["title"] for item in order["items"]]
            )
            for order_id, order in self.orders.items()
            if order["user_id"] == request.user_id
        ]
        return orders_pb2.OrderListResponse(orders=user_orders)
