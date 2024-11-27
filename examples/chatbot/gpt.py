from collections.abc import Iterable
from dataclasses import dataclass
from openai import OpenAI
from .openai_api_key import key



@dataclass
class Message:
    role: str
    content: str

client = None

def _real_gpt(messages: Iterable[Message]) -> str:
    global client
    if client is None:
        client = OpenAI(api_key=key)
    def convert_msg(message: Message):
        return {
            "role": message.role,
            "content": message.content
        }
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=map(convert_msg, messages),
    )
    return stream.choices[0].message.content

def _gpt_stub(messages: Iterable[Message]) -> str:
    _real_gpt(messages)
    # reply = "1, 1, 1, 1, 1, 1, 1, 1"
    # print(f'gpt request. returning "{reply}"')
    # return reply

def gpt(messages: Iterable[Message]) -> str:
    return _real_gpt(messages)
    