import aiohttp
import asyncio
import random
import requests
import time

def get_blum_token(query_id, referral_token):
    url = "https://user-domain.blum.codes/api/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP"
    headers = {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "origin": "https://telegram.blum.codes",
        "referer": "https://telegram.blum.codes/"
    }
    payload = {
        "query": query_id,
        "referralToken": referral_token
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            token = response.json().get("token").get("access")
            return f"Bearer {token}"
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def read_tokens_from_file():
    with open('tokens.txt', 'r') as f:
        lines = f.readlines()
        query_id = lines[0].strip()
        referral_token = "JxBox7eZv3"
    return query_id, referral_token

def display_banner():
    banner = """
    ██████╗ ██╗     ██╗   ██╗███╗   ███╗    ██████╗  ██████╗ ████████╗
    ██╔══██╗██║     ██║   ██║████╗ ████║    ██╔══██╗██╔═══██╗╚══██╔══╝
    ██████╔╝██║     ██║   ██║██╔████╔██║    ██████╔╝██║   ██║   ██║   
    ██╔═══╝ ██║     ██║   ██║██║╚██╔╝██║    ██╔═══╝ ██║   ██║   ██║   
    ██║     ███████╗╚██████╔╝██║ ╚═╝ ██║    ██║     ╚██████╔╝   ██║   
    ╚═╝     ╚══════╝ ╚═════╝ ╚═╝     ╚═╝    ╚═╝      ╚═════╝    ╚═╝   
      BLUM BOT by MixTubeCats
    """
    print(banner)

async def claim(token):
    url = "https://game-domain.blum.codes/api/v1/farming/claim"
    headers = {
        "Authorization": token,
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers) as resp:
                resp_json = await resp.json()
                if 'message' in resp_json:
                    print( resp_json['message'])
                    return False
                print(f"Claim success: {resp_json}")
                return True
    except Exception as e:
        return False

async def do_tasks(token):
    url = "https://earn-domain.blum.codes/api/v1/tasks"
    headers = {
        "Authorization": token,
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9,uk;q=0.8,ru;q=0.7",
        "Origin": "https://telegram.blum.codes"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                resp_json = await resp.json()

                if 'message' in resp_json:
                    return 0

                for task in resp_json[1]['subSections']:
                    if task['title'] == "Frens":
                        continue
                    tasks = task['tasks']
                    for task in tasks:
                        if random.randint(0, 2) == 0:
                            if task['status'] == "NOT_STARTED":
                                await session.post(f"https://earn-domain.blum.codes/api/v1/tasks/{task['id']}/start", headers=headers)
                                await asyncio.sleep(random.randint(1, 3))
                            elif task['status'] == "READY_FOR_CLAIM":
                                answer = await session.post(f"https://earn-domain.blum.codes/api/v1/tasks/{task['id']}/claim", headers=headers)
                                answer_json = await answer.json()
                                if 'message' in answer_json:
                                    continue
                                print(f"Claimed TASK reward! Claimed: {answer_json['reward']}")
                                await asyncio.sleep(random.randint(1, 3)) 

    except Exception as e:
        print(e)

async def get_diamonds_balance(token):
    url = "https://game-domain.blum.codes/api/v1/user/balance"
    headers = {
        "Authorization": token,
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9,uk;q=0.8,ru;q=0.7",
        "Origin": "https://telegram.blum.codes"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                resp_json = await resp.json()

                if 'message' in resp_json:
                    return 0

                diamonds_balance = resp_json['playPasses']
                print(f"Diamonds Balance: {diamonds_balance}")
                return diamonds_balance

    except Exception as e:
        print(e)

async def game(token):
    try:
        url_play = "https://game-domain.blum.codes/api/v1/game/play"
        url_claim = "https://game-domain.blum.codes/api/v1/game/claim"
        headers = {
            "Authorization": token,
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9,uk;q=0.8,ru;q=0.7",
            "Origin": "https://telegram.blum.codes"
        }

        async with aiohttp.ClientSession() as session:
            response = await session.post(url_play, headers=headers)
            response_json = await response.json()

            if 'message' in response_json:
                return

            game_id = response_json['gameId']
            count = random.randint(140, 200)

            if count >= 160:
                await asyncio.sleep(30 + (count - 160) // 7 * 4)
            else:
                await asyncio.sleep(30)

            json_data = {
                'gameId': game_id,
                'points': count,
            }

            response_claim = await session.post(url_claim, json=json_data, headers=headers)
            if await response_claim.text() == "OK":
                print(f"Claimed DROP GAME! Claimed: {count}")

    except Exception as e:
        print(e)

async def claim_diamond(token):
    url = "https://game-domain.blum.codes/api/v1/daily-reward?offset=-180"
    headers = {
        "Authorization": token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9,uk;q=0.8,ru;q=0.7",
        "Origin": "https://telegram.blum.codes"
    }

    try:
        async with aiohttp.ClientSession() as session:
            resp = await session.post(url, headers=headers)
            txt = await resp.text()
            if 'message' in txt:
                return False
            return True if txt == 'OK' else txt

    except Exception as e:
        print(e)

async def start(token):
    url = "https://game-domain.blum.codes/api/v1/farming/start"
    headers = {
        "Authorization": token,
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9,uk;q=0.8,ru;q=0.7",
        "Origin": "https://telegram.blum.codes"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers) as resp:
                resp_json = await resp.json()

                if 'message' in resp_json:
                    return 0
    except Exception as e:
        print(e) 

async def main_loop():
    query_id, referral_token = read_tokens_from_file()
    token = get_blum_token(query_id, referral_token)

    if not token:
        return

    while True:
        try:
            await claim(token)
            await asyncio.sleep(5)
            await do_tasks(token)
            await asyncio.sleep(5)
            await game(token)
            await asyncio.sleep(5)
            await claim_diamond(token)
            await asyncio.sleep(5)
            await start(token)
        except Exception as e:
            print(e)

        await asyncio.sleep(30 - 5 * 5)

        if not await claim(token): 
            token = get_blum_token(query_id, referral_token)

async def menu():
    display_banner()
    await main_loop()

if __name__ == "__main__":
    asyncio.run(menu())
