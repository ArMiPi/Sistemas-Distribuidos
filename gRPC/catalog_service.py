from __future__ import annotations

from typing import TYPE_CHECKING

import grpc
from typing_extensions import Literal

import catalog_pb2
import catalog_pb2_grpc

if TYPE_CHECKING:
    from catalog_pb2 import BookInfoResponse, BookListResponse, BookRequest


class CatalogService(catalog_pb2_grpc.CatalogServiceServicer):
    def __init__(self):
        self.__books: dict[
            str,
            dict[
                Literal["title", "author", "year", "stock", "price"], str | int | float
            ],
        ] = {
            "b1": {
                "title": "Book One",
                "author": "Author One",
                "year": 2001,
                "stock": 5,
                "price": 29.99,
            },
            "b2": {
                "title": "Book Two",
                "author": "Author Two",
                "year": 2002,
                "stock": 3,
                "price": 19.99,
            },
            "b3": {
                "title": "Book Three",
                "author": "Author Three",
                "year": 1998,
                "stock": 2,
                "price": 9.99,
            },
        }

    def GetBookInfo(self, request: BookRequest, context) -> BookInfoResponse:
        if request.b_id in self.__books:
            book = self.__books[b_id]
            return catalog_pb2.BookInfoResponse(
                b_id=request.b_id,
                title=book["title"],
                author=book["author"],
                year=book["year"],
                stock=book["stock"],
                price=book["price"],
            )

        msg_erro = "Livro não encontrado"
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details(msg_erro)
        return catalog_pb2.BookInfoResponse(erro=msg_erro)

    def ListBooks(self, request: BookRequest, context) -> BookListResponse:
        books = [
            catalog_pb2.Book(b_id=b_id, **book) for b_id, book in self.__books.items()
        ]
        return catalog_pb2.BookListResponse(books=books)
