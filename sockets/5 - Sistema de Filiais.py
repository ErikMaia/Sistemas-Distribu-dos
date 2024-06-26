import asyncio
import websockets
import json
import random
import time

async def simulate_store(store_id):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        for _ in range(1500):  # Simular 1500 ocorrências
            transaction = {
                "type": random.choice(["compra", "venda"]),
                "amount": random.uniform(10.0, 500.0),
                "timestamp": time.time()
            }
            message = json.dumps({"store_id": store_id, "transaction": transaction})
            await websocket.send(message)
            await asyncio.sleep(random.uniform(0.1, 0.5))  # Delay para simular tempo real

async def main():
    tasks = [simulate_store(store_id) for store_id in range(1, 6)]  # 5 filiais
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
