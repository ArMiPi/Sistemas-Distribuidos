from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

import grpc
from typing_extensions import Literal

import orders_pb2
import orders_pb2_grpc

if TYPE_CHECKING:
    from orders_pb2 import (
        OrderGetterRequest,
        OrderGetterResponse,
        OrderListResponse,
        OrderRequest,
        OrderResponse,
        UserRequest,
    )


class OrderService(orders_pb2_grpc.OrderServiceServicer):
    def __init__(self):
        self.__orders: dict[
            str, dict[str, dict[Literal["b_id", "quantidade", "hora"], str | int]]
        ] = {}

    def PlaceOrder(self, request: OrderRequest, context) -> OrderResponse:
        order_id = str(uuid.uuid4())
        user_id = request.user_id

        if user_id not in self.__orders:
            self.__orders.update({user_id: {}})

        orders = self.__orders[user_id]
        orders.update(
            {
                order_id: {
                    "b_id": request.b_id,
                    "quantidade": request.quantity,
                    "hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
            }
        )

        return orders_pb2.OrderResponse(order_id=order_id)

    def ListOrders(self, request: UserRequest, context) -> OrderListResponse:
        user_id = request.user_id
        if user_id not in self.__orders:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User not found")
            return orders_pb2.OrderListResponse(orders=[])

        user_orders = self.__orders[user_id]
        orders = [
            orders_pb2.OrderSummary(order_id=order_id, hour=livro["hora"])
            for order_id, livro in user_orders.items()
        ]
        return orders_pb2.OrderListResponse(orders=orders)

    def GetOrder(self, request: OrderGetterRequest, context) -> OrderGetterResponse:
        user_id = request.user_id
        order_id = request.order_id

        if user_id not in self.__orders:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User not found")
            return orders_pb2.OrderGetterResponse()

        orders = self.__orders[user_id]

        if order_id not in orders:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Order not found")
            return orders_pb2.OrderGetterResponse()

        order = orders[order_id]

        return orders_pb2.OrderGetterResponse(
            b_id=order["b_id"], quantity=order["quantidade"], hour=order["hora"]
        )
