import grpc
import os
from dotenv import load_dotenv
import temperatura_pb2
import temperatura_pb2_grpc


def main():
    load_dotenv()
    server_ip = os.getenv("SERVER_IP")
    server_port = os.getenv("SERVER_PORT")

    canal = grpc.insecure_channel(f"{server_ip}:{server_port}")

    stub = temperatura_pb2_grpc.TemperaturasStub(canal)

    ciudad = temperatura_pb2.Ciudad(codigo="BA")

    respuesta = stub.ObtenerTemperaturas(ciudad)

    print("Temperaturas:", list(respuesta.temperaturas))

if __name__ == "__main__":
    main()
