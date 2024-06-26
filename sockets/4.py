import asyncio
import websockets
import json

# Dicionário para armazenar informações das contas
accounts = {}

# Bloqueios para evitar conflitos durante operações concorrentes
account_locks = {}

async def handle_client(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        action = data["action"]
        account_id = data["account_id"]
        
        # Inicializa a conta se não existir
        if account_id not in accounts:
            accounts[account_id] = 0
            account_locks[account_id] = asyncio.Lock()

        # Opera conforme a ação solicitada
        if action == "deposit":
            amount = data["amount"]
            await deposit(account_id, amount)
            await websocket.send(json.dumps({"status": "success", "balance": accounts[account_id]}))
        
        elif action == "withdraw":
            amount = data["amount"]
            success = await withdraw(account_id, amount)
            if success:
                await websocket.send(json.dumps({"status": "success", "balance": accounts[account_id]}))
            else:
                await websocket.send(json.dumps({"status": "failed", "balance": accounts[account_id]}))
        
        elif action == "balance":
            await websocket.send(json.dumps({"status": "success", "balance": accounts[account_id]}))
        
        elif action == "exit":
            await websocket.send(json.dumps({"status": "bye"}))
            break

async def deposit(account_id, amount):
    async with account_locks[account_id]:
        accounts[account_id] += amount

async def withdraw(account_id, amount):
    async with account_locks[account_id]:
        if accounts[account_id] >= amount:
            accounts[account_id] -= amount
            return True
        else:
            return False

async def main():
    async with websockets.serve(handle_client, "localhost", 8765):
        await asyncio.Future()  # Mantém o servidor em execução

if __name__ == "__main__":
    asyncio.run(main())
