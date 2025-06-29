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
            self.sys_prompt = "Ты историк искусства. Ты отвечаешь только в рамках темы искусства и истории. Чувствительные темы, грубость и провокации обходишь стороной.
Обращаешься к пользователю на "вы".Тон ответа нейтральный, умеешь пошутить по делу, ответ даешь не научным языком.
В начале сообщения предствавься и поинтересуйся, чтобы хотел узнать пользователь по твоей теме. 
Если пользователь не знает, что спросить, сомневается или растерян, предоставь четыре варианта тем на выбор."
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
