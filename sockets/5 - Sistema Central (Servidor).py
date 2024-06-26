import asyncio
import websockets
import json

# Dicionário para armazenar dados recebidos das filiais
stores_data = {}

async def handle_client(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        store_id = data["store_id"]
        transaction = data["transaction"]

        # Inicializa os dados da filial se não existir
        if store_id not in stores_data:
            stores_data[store_id] = []

        # Armazena a transação recebida
        stores_data[store_id].append(transaction)
        print(f"Recebido da filial {store_id}: {transaction}")

async def main():
    async with websockets.serve(handle_client, "localhost", 8765):
        await asyncio.Future()  # Mantém o servidor em execução

if __name__ == "__main__":
    asyncio.run(main())
