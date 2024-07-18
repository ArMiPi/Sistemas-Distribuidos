.PHONY: all build install run_services run_app

PY_EXE = py
PROTOS_FOLDER = protos
OUT_FOLDER = .

all: build

build: install proto

install:
	pip install -r requirements.txt

proto:
	$(PY_EXE) -m grpc_tools.protoc -I=$(PROTOS_FOLDER) --python_out=$(OUT_FOLDER) --grpc_python_out=$(OUT_FOLDER) $(PROTOS_FOLDER)/auth.proto
	$(PY_EXE) -m grpc_tools.protoc -I=$(PROTOS_FOLDER) --python_out=$(OUT_FOLDER) --grpc_python_out=$(OUT_FOLDER) $(PROTOS_FOLDER)/catalog.proto
	$(PY_EXE) -m grpc_tools.protoc -I=$(PROTOS_FOLDER) --python_out=$(OUT_FOLDER) --grpc_python_out=$(OUT_FOLDER) $(PROTOS_FOLDER)/orders.proto

run_server:
	$(PY_EXE) server.py

run_app:
	$(PY_EXE) app.py
