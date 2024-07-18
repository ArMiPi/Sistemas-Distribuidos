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


@app.route("/bookstore", methods=["GET", "POST"])
def bookstore():
    with grpc.insecure_channel(GRPC_ROUTE) as channel:
        catalog_stub = catalog_pb2_grpc.CatalogServiceStub(channel)

        books = catalog_stub.ListBooks(catalog_pb2.Empty())
        if request.method == "POST":
            book_id = request.form["b_id"]
            quantity = request.form["quantity"]

            try:
                response = catalog_stub.GetBookInfo(
                    catalog_pb2.BookRequest(b_id=book_id)
                )

                print(response)
            except Exception as e:
                print(e)
                return render_template(
                    "bookstore.html", books=books.books, msg_erro="Não foi possível realizar a compra", b_id_error=book_id
                )

    return render_template("bookstore.html", books=books.books)


if __name__ == "__main__":
    app.run(debug=True)
