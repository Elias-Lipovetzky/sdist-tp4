import os
from concurrent import futures

import grpc
from dotenv import load_dotenv

import temperatura_pb2
import temperatura_pb2_grpc


load_dotenv()

server_ip = os.getenv("SERVER_IP")
server_port = os.getenv("SERVER_PORT")


temperaturas = {
    "BA": [18.5, 20.0, 22.3],
    "COR": [15.2, 17.8, 21.0],
    "MDZ": [12.5, 16.0, 19.4],
}


class TemperaturasServicer(temperatura_pb2_grpc.TemperaturasServicer):

    def ObtenerTemperaturas(self, request, context):
        codigo = request.codigo

        peer = context.peer()

        print(f"Request recibido desde {peer}")
        print(f"Ciudad solicitada: {codigo}")

        valores = temperaturas.get(codigo)

        if valores is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Ciudad no encontrada")
            return temperatura_pb2.TemperaturasResponse()

        return temperatura_pb2.TemperaturasResponse(
            temperaturas=valores
        )


def serve():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )

    temperatura_pb2_grpc.add_TemperaturasServicer_to_server(
        TemperaturasServicer(),
        server
    )

    server.add_insecure_port(
        f"{server_ip}:{server_port}"
    )

    server.start()

    print(f"Servidor escuchando en {server_ip}:{server_port}...")

    server.wait_for_termination()


if __name__ == "__main__":
    serve()

