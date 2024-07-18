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

        return redirect(url_for("index"))

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

        return redirect(url_for("index"))

    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
