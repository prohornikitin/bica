from collections.abc import Iterable
from dataclasses import dataclass
from openai import OpenAI




@dataclass
class Message:
    role: str
    content: str

client = None

def _real_gpt(messages: Iterable[Message]) -> str:
    if client is None:
        client = OpenAI()
    def convert_msg(message: Message):
        return {
            "role": message.role,
            "content": messages.content
        }
    stream = client.chat.completions.create(
        model="gpt-3.5",
        messages=map(convert_msg, messages),
    )
    return stream.choices[0].message

def _gpt_stub(messages: Iterable[Message]) -> str:
    reply = "1, 1, 1, 1, 1, 1, 1, 1"
    print(f'gpt request. returning "{reply}"')
    return reply

def gpt(messages: Iterable[Message]) -> str:
    return _gpt_stub(messages)
    