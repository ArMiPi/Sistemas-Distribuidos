import grpc

import catalog_pb2
import catalog_pb2_grpc


class CatalogService(catalog_pb2_grpc.CatalogServiceServicer):
    def __init__(self):
        # Inicializar o catálogo de livros em memória
        self.books = [
            {
                "title": "Book One",
                "author": "Author One",
                "year": 2001,
                "stock": 5,
                "price": 29.99,
            },
            {
                "title": "Book Two",
                "author": "Author Two",
                "year": 2002,
                "stock": 3,
                "price": 19.99,
            },
            # Adicione mais livros conforme necessário
        ]

    def GetBookInfo(self, request, context):
        for book in self.books:
            if book["title"] == request.title:
                return catalog_pb2.BookInfoResponse(
                    title=book["title"],
                    author=book["author"],
                    year=book["year"],
                    stock=book["stock"],
                    price=book["price"],
                )
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details("Book not found")
        return catalog_pb2.BookInfoResponse()

    def ListBooks(self, request, context):
        books = [catalog_pb2.Book(**book) for book in self.books]
        return catalog_pb2.BookListResponse(books=books)
