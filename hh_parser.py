import asyncio
import aiohttp

"""
Почему-то выдает 403 ошибку я хз почему если авторизацию по докам не требует для обычного скана вакансий
"""
# def auth_lib():
#     url = "https: // hh.ru / oauth / authorize?"
#     response_type = code &
#     client_id = {client_id} &
#     state = {state} &
#     redirect_uri = {redirect_uri} &
#     code_challenge = {code_challenge} &
#     code_challenge_method = S256

async def fetch_hh_vacancies():
    async with aiohttp.ClientSession() as session:

        URL = "https://api.hh.ru/vacancies"

        params = {
            "text": "Python Junior",
            "per_page": 5,
        }

        headers = {
            "User-Agent": "AIJobHunter/1.0 ramzes335aa@gmail.com"
        }

        async with session.get(url=URL, params=params, headers=headers) as response:
            await asyncio.sleep(5)
            print(f"Статус ответа: {response.status}")
            data = await response.json()

            print(f"Детали ошибки: {data.get('errors')}")
            print(f"Ключи ответа: {list(data.keys())}")

            await asyncio.sleep(5)
            for item in data.get("items", []):
                await asyncio.sleep(5)
                print(item["name"])
                print(item["employer"]["name"])
                print(item["alternate_url"])

if __name__ == "__main__":
    asyncio.run(fetch_hh_vacancies())