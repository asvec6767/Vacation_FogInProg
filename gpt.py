from openai import OpenAI
#openai.api_key='gpt_key2' #openai, no money

client = OpenAI(
    api_key="gpt_key", #proxy api
    base_url="https://api.proxyapi.ru/openai/v1",
)

def prompt(place:str):
    query="Ты гид. Коротко напиши рекламную информацию о "+place+" в городе Тула"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[{"role": "user", "content": query}],
        temperature=0.7,
        max_tokens=75,
        n=1,
        stop=None
    )
    result = response.choices[0].message.content.__str__()
    return result[:result.rfind('.')]+'.'+'"'

def prompt_distance_name(places):
    place=''.join(places)
    query="Назови одним словосочетанием маршрут по местам "+place+" в городе Тула"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[{"role": "user", "content": query}],
        temperature=0.7,
        max_tokens=25,
        n=1,
        stop=None
    )
    result = response.choices[0].message.content.__str__()
    return result

def prompt_check_poem(poem:str):
    query="Ответь только 'да' или 'нет'. Связана ли эта фраза с новым годом, рождеством или зимой: '"+poem+"'"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[{"role": "user", "content": query}],
        temperature=0.7,
        max_tokens=10,
        n=1,
        stop=None
    )
    result = response.choices[0].message.content.__str__()
    if result == 'да' or result == 'Да' or result == 'ДА' or result == 'дА':
        return True
    else:
        return False
