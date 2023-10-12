import pandas as pd
import requests
import openai

sdw2023_api_url = 'https://sdw-2023-prd.up.railway.app'


def update_user(user):
    global sdw2023_api_url
    response = requests.put(f"{sdw2023_api_url}/users/{user['id']}", json=user)

    return True if response.status_code == 200 else False


def get_user(id):
    global sdw2023_api_url
    response = requests.get(f"{sdw2023_api_url}/users/{id}")
    return response.json() if response.status_code == 200 else None


def generate_news(user):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[
        {
            "role": "system",
            "content": "Você é um especialista em marketing de produtos fitness."
        },
        {
            "role": "user",
            "content": f"""
            Crie uma mensagem para {user['name']} sobre a importância das atividades fisícas e 
            de uma alimentação saúdavel e fale sobre os produtos da Growth (máximo de 200 caracteres)
            """
        }
        ]
    )
    response_chatgpt = completion.choices[0].message.content.strip('\"')
    return response_chatgpt


def main():
    df = pd.read_csv('SDW2023.csv')
    users_ids = df['UserID'].tolist()

    users = [user for id in users_ids if (user := get_user(id)) is not None]
    
    openai_api_key = "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"

    openai.api_key = openai_api_key

    for user in users:
        news = generate_news(user)
        user['news'].append({
            "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
            "description": news
        })
        # print(news)
        update_user(user)


if __name__ == "__main__":
    main()