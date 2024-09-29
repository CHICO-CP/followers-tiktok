#Developer by @Gh0stDeveloper
#Channel Of telegram: @TEAM_CHICO_CP

import json
import os
import random
import asyncio
from pyppeteer import launch

json_file_path = "tiktok_users.json"
comments_file_path = "comments.json"

def create_example_json():
    example_data = {
        "users": [
            {"username": "example_user1", "password": "example_password1"},
            {"username": "example_user2", "password": "example_password2"}
        ]
    }
    with open(json_file_path, 'w') as json_file:
        json.dump(example_data, json_file, indent=4)
    print(f"Archivo {json_file_path} creado con ejemplos. Por favor, rellénalo con los datos de los usuarios.")

def create_comments_json():
    example_comments = {
        "comments": [
            "Buen video",
            "Eres el mejor",
            "Sigue así"
        ]
    }
    with open(comments_file_path, 'w') as json_file:
        json.dump(example_comments, json_file, indent=4)
    print(f"Archivo {comments_file_path} creado con ejemplos. Por favor, rellénalo con más comentarios si lo deseas.")

def read_users_from_json():
    if not os.path.exists(json_file_path):
        create_example_json()
        return []

    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
        return data.get("users", [])

def read_comments_from_json():
    if not os.path.exists(comments_file_path):
        create_comments_json()
        return []

    with open(comments_file_path, 'r') as json_file:
        data = json.load(json_file)
        return data.get("comments", [])

async def login_and_interact(page, username, password, username_to_search):
    await page.goto("https://www.tiktok.com/login")
    await page.waitForSelector('input[name="username"]')
    await page.waitForSelector('input[name="password"]')
    await page.type('input[name="username"]', username)
    await page.type('input[name="password"]', password)
    await page.click('button[type="submit"]')
    await page.waitForSelector('div[data-e2e="search-icon"]')
    await page.type('input[type="text"]', username_to_search)
    await page.keyboard.press('Enter')
    await page.waitForSelector('a[data-e2e="search-user-card"]')
    first_result = await page.querySelector('a[data-e2e="search-user-card"]')
    await first_result.click()
    await page.waitForSelector('button[data-e2e="user-follow"]')
    follow_button = await page.querySelector('button[data-e2e="user-follow"]')
    await follow_button.click()
    print(f"Seguiste al usuario: {username_to_search}")

    video_thumbnails = await page.querySelectorAll('div[data-e2e="user-post-item"]')
    if not video_thumbnails:
        print("El usuario no tiene videos")
        return

    comments = read_comments_from_json()
    if not comments:
        print("El archivo de comentarios está vacío. Por favor, rellénalo con más comentarios.")
        return

    for video in video_thumbnails:
        await video.click()
        await page.waitForSelector('div[data-e2e="like-icon"]')

        like_button = await page.querySelector('div[data-e2e="like-icon"]')
        await like_button.click()
        print("Like dado al video")

        comment_input = await page.querySelector('textarea[data-e2e="comment-input"]')
        random_comment = random.choice(comments)
        await comment_input.type(random_comment)
        await comment_input.press('Enter')
        print(f"Comentario realizado: {random_comment}")

        await page.waitForTimeout(3000)
        close_button = await page.querySelector('div[data-e2e="close-icon"]')
        await close_button.click()
        await page.waitForTimeout(2000)

async def main():
    if not os.path.exists(json_file_path):
        create_example_json()
    if not os.path.exists(comments_file_path):
        create_comments_json()

    users = read_users_from_json()
    if not users:
        print("El archivo JSON de usuarios está vacío. Por favor, rellénalo con los datos de los usuarios.")
        return

    browser = await launch(headless=False)
    page = await browser.newPage()
    username_to_search = input("Introduce el nombre de usuario a buscar: ").strip()
    for user in users:
        await login_and_interact(page, user["username"], user["password"], username_to_search)
    await browser.close()

if __name__ == "__main__":
    asyncio.run(main())