import openai
import dotenv
env = dotenv.dotenv_values(".env")

class LLMService:
    def __init__(self):
        try:
            # Создаем клиент с вашим токеном
            self.client = openai.OpenAI(
                api_key=env["YA_API_KEY"],
                base_url="https://llm.api.cloud.yandex.net/v1",
            )
            # Формируем системный промпт
            self.sys_prompt = "Ты помощник разработке кулираных рецептов.оприветствуй пользователя так— /" \
            "Привет!  Я — ваш помощник в мире кулинарии. Расскажите, какие продукты у вас есть под рукой, а я предложу вам вкусные и интересные рецепты,/" \
            " которые можно приготовить из имеющихся ингредиентов. после того, как пользователь перечислит продукты, предложи один рецепт./" \
            "Тон общения дружелюбный. общение только в рамках тематики кулинарии. не реагируй на провокации, грубость или чувствительные темы."        
            self.model="gpt://b1gd4dt3l1spqgmer1n1/yandexgpt-lite"

        except Exception as e:
            return f"Произошла ошибка: {str(e)}"

    def chat(self, message):
        try:
            # Обращаемся к API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.sys_prompt},
                    {"role": "user", "content": message},
                ],
                temperature=1.0,
                max_tokens=1024,
            )

            # Возвращаем ответ
            return response.choices[0].message.content

        except Exception as e:
            return f"Произошла ошибка: {str(e)}"
