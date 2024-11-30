import re

import numpy as np
from bica.intensions import InSpace, InVec
from .gpt import gpt, Message


sem_space1 = [
    'вовлечь в диалог',
    'выразить недовольство',
    'задавать вопросы',
    'обратить внимание',
    'проявить инициативу',
    'рассказать',
    'выразить понимание',
]

sem_space2 = [
    'выразить свое мнение',
    'отрицать',
    'оценить',
    'поддержать',
    'пояснить',
    'предложить',
    'предположить',
    'уточнить',
    'поделиться опытом',
]

sem_space3 = [
    'выразить надежду',
    'выразить обеспокоенность',
    'выразить согласие',
    'завершить разговор',
    'подтвердить',
    'поставить цель',
    'убедить'
]


def numbers_from_reply(reply: str) -> list[float]: 
    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", reply)
    return [float(num) for num in numbers]


def intensional_calc(intent: list[str], space: InSpace, phrase: str) -> InVec:
    cat_str = ', '.join(intent)
    num = len(intent)
    string = f'''
    Ты механизм по определению интенсивности интенcиональностей в речи человека, связанных с его поведением в различных социальных ситуациях.
    В твоем распоряжении только список из {num} интенcиональностей для угадывания(они перечислены через запятую): {cat_str}. 
    Далее есть предложение: "{phrase}"
    Оцени интенсивность содержания каждой интенции в предложении.
    В конце выведи эти интенсивности по шкале от 0 до 1:
    где 0 - очень низкая (интенция не прослеживается вообще),
    0.25 слабая интенсивность (интенция почти незаметна),
    0.5 - средняя интенсивность (интенция присутствует, но выражена неявно),
    0.75 - умеренная интенсивность (интенция точно присутствует),
    а 1 - сильная интенсивность (интенция является главным мотивом фразы).
    Значения которые ты укажешь не обязательно должны равняться выше указанным, это всего лишь отметки на шкале.
    Выведи ТОЛЬКО значения интенсивности каждой интенции через запятую (всего должно быть {num} число). Не выводи названия самих интенции
    и не пиши порядковые номера.
    Перед ответом проверь правильность каждой цифры отдельно на правдоподобность и исправь если что-то нашёл.
    '''
    
    question = Message('assistant', string)
    reply = gpt([question])
    nums = np.array(numbers_from_reply(reply))
    nums.resize(len(intent))
    if intent == sem_space1:
        return InVec(space, space_1_matrix.dot(nums))
    elif intent == sem_space2:
        return InVec(space, space_2_matrix.dot(nums))
    elif intent == sem_space3:
        return InVec(space, space_3_matrix.dot(nums))
    else:
        return InVec(InSpace([]), [])


space_1_matrix = np.array([
    [1, -0.2, 0.5, 0.3, 0.5, 0.75, 0.1],
    [0.2, -0.8, 0.4, 0.2, 0.5, 0.7, 0.2],
    [0.3, -0.1, 1, 0.7, 0.2, 0.2, 0.1],
    [0.2, -0.2, 0.6, 1, 0.3, 0.3, 0.2],
    [0.7, -0.1, 0.3, 0.3, 1, 0.4, 0.2]
])

space_2_matrix = np.array([
    [0.95, -0.1, 0.1, 0.1, 0.5, 0.3, 0.1, 0.2, 0.34],
    [0.1, 0.95, 0.1, -0.5, 0.2, 0.1, 0.1, 0.05, 0.05],
    [0.8, -0.1, 0.2, 0.1, 0.4, 0.9, 0.1, 0.1, 0.2],
    [0.05, -0.1, 0.3, 0.9, 0.1, 0.2, 0.1, 0.2, 0.1],
    [0.2, 0.1, 0.2, 0.21, 0.9, 0.1, 0.2, 0.8, 0.4],
    [0.7, -0.5, 0.6, 0.2, 0.4, 0.6, 0.4, 0.4, 0.7]
])

space_3_matrix = np.array([
    [0.7, -0.7, 0.2, 0.1, 0.4, 0.8, 0.6],
    [0.2, -0.5, 0.2, 0.1, 0.4, 0.2, 0.3],
    [0.6, -0.4, 0.5, 0.1, 0.3, 0.5, 0.1],
    [0.5, -0.5, 0.2, 0.1, 0.5, 0.9, 0.1],
    [0.2, 0.1, 0.2, 0.21, 0.5, 0.1 ,0.2],
])