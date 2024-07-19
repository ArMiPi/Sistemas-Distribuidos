import grpc
from flask import Flask, redirect, render_template, request, session, url_for

import auth_pb2
import auth_pb2_grpc
import catalog_pb2
import catalog_pb2_grpc
import orders_pb2
import orders_pb2_grpc

app = Flask(__name__)
app.secret_key = "SOMeUltimaTERanDoMKEyyY"

GRPC_ROUTE = "localhost:50051"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        with grpc.insecure_channel(GRPC_ROUTE) as channel:
            auth_stub = auth_pb2_grpc.AuthServiceStub(channel)

            try:
                response = auth_stub.Register(
                    auth_pb2.RegisterRequest(username=username, password=password)
                )
                session["token"] = response.token
            except:
                return render_template(
                    "register.html", msg_erro="Usuário já cadastrado"
                )

        return redirect(url_for("bookstore"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        with grpc.insecure_channel(GRPC_ROUTE) as channel:
            auth_stub = auth_pb2_grpc.AuthServiceStub(channel)

            try:
                response = auth_stub.Login(
                    auth_pb2.LoginRequest(username=username, password=password)
                )
                session["token"] = response.token
            except:
                return render_template(
                    "login.html", msg_erro="Usuário ou senha incorreto"
                )

        return redirect(url_for("bookstore"))

    return render_template("login.html")


@app.route("/logout", methods=["POST"])
def logout():
    session["token"] = ""

    return render_template("index.html")


@app.route("/bookstore", methods=["GET", "POST"])
def bookstore():
    with grpc.insecure_channel(GRPC_ROUTE) as channel:
        catalog_stub = catalog_pb2_grpc.CatalogServiceStub(channel)

        books = catalog_stub.ListBooks(catalog_pb2.Empty())

        if request.method == "POST":
            orders_stub = orders_pb2_grpc.OrderServiceStub(channel)
            book_id = request.form["b_id"]
            quantity = int(request.form["quantity"])

            try:
                order = orders_stub.PlaceOrder(
                    orders_pb2.OrderRequest(
                        user_id=session["token"], b_id=book_id, quantity=quantity
                    )
                )

                catalog_stub.BuyBook(
                    catalog_pb2.BuyBookRequest(b_id=book_id, quantity=quantity)
                )

                books = catalog_stub.ListBooks(catalog_pb2.Empty())

                return render_template(
                    "bookstore.html",
                    books=books.books,
                    order=order.order_id,
                    b_id_info=book_id,
                )
            except Exception as e:
                print(e)
                return render_template(
                    "bookstore.html",
                    books=books.books,
                    msg_erro="Não foi possível realizar a compra",
                    b_id_info=book_id,
                )

    return render_template("bookstore.html", books=books.books)


@app.route("/orders", methods=["GET"])
def orders():
    with grpc.insecure_channel(GRPC_ROUTE) as channel:
        orders_stub = orders_pb2_grpc.OrderServiceStub(channel)

        try:
            orders = orders_stub.ListOrders(
                orders_pb2.UserRequest(user_id=session["token"])
            )

            orders = orders.orders
        except:
            orders = []

    return render_template("orders.html", pedidos=orders)


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        if request.form["tipo"] == "book":
            with grpc.insecure_channel(GRPC_ROUTE) as channel:
                try:
                    catalog_stub = catalog_pb2_grpc.CatalogServiceStub(channel)
                    book_name = request.form["book_name"]

                    book = catalog_stub.GetBookInfo(
                        catalog_pb2.BookRequest(book_name=book_name)
                    )

                    return render_template("search.html", book=book)

                except Exception as e:
                    print(e)
                    return render_template(
                        "search.html", msg_erro_livro="Livro não encontrado"
                    )

        if request.form["tipo"] == "order":
            with grpc.insecure_channel(GRPC_ROUTE) as channel:
                try:
                    orders_stub = orders_pb2_grpc.OrderServiceStub(channel)
                    catalog_stub = catalog_pb2_grpc.CatalogServiceStub(channel)
                    id_pedido = request.form["id_pedido"]

                    pedido = orders_stub.GetOrder(
                        orders_pb2.OrderGetterRequest(
                            user_id=session["token"], order_id=id_pedido
                        )
                    )

                    book = catalog_stub.GetBookInfoById(
                        catalog_pb2.BookRequestId(b_id=pedido.b_id)
                    )

                    return render_template(
                        "search.html",
                        book_pedido=book,
                        pedido=pedido,
                        id_pedido=id_pedido,
                    )
                except Exception as e:
                    print(e)
                    return render_template(
                        "search.html", msg_erro_pedido="Pedido não encontrado"
                    )

    return render_template("search.html")


if __name__ == "__main__":
    app.run(debug=True)
