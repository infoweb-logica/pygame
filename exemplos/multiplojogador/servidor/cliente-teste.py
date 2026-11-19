import asyncio
import json
import websockets
import os
from dotenv import load_dotenv


async def main():
    player_id = int(input("ID do jogador: "))
    name = input("Nome do jogador: ")
    load_dotenv()
    host = os.getenv("HOST", "localhost")
    porta = os.getenv("PORT", "8765")

    async with websockets.connect(f"ws://{host}:{porta}") as ws:

        # Identificação
        await ws.send(json.dumps({
            "tipo": "entrar",
            "id": player_id,
            "nome": name,
            "posicao": {"x": 0, "y": 0}
        }))

        async def receive_messages():
            async for message in ws:
                data = json.loads(message)
                print("\nServidor:", data)

        async def send_positions():
            while True:
                x = float(input("Nova posição X: "))
                y = float(input("Nova posição Y: "))

                await ws.send(json.dumps({
                    "tipo": "mover",
                    "posicao": {"x": x, "y": y}
                }))

        await asyncio.gather(
            receive_messages(),
            send_positions()
        )

if __name__ == "__main__":
    asyncio.run(main())
