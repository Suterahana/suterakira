import re
import traceback

import discord
import greenlet
from actions.message_actions import send_quick_embed_message
from constants import Colour


class GreenAwait:
    def __init__(self, child):
        self.current = greenlet.getcurrent()
        self.value = None
        self.child = child

    def __call__(self, future):
        self.value = future
        self.current.switch()

    def __iter__(self):
        while self.value is not None:
            yield self.value
            self.value = None
            self.child.switch()


def gexec(code):
    child = greenlet.greenlet(exec)
    gawait = GreenAwait(child)
    child.switch(code, {'gawait': gawait})
    yield from gawait


async def aexec(code, message):
    green = greenlet.greenlet(gexec)
    code_lines = '\t'.join(code.splitlines(keepends=True))
    final_code = f'''
from actions.message_actions import send_quick_embed_message
from clients import discord_client
from constants import Colour
async def code_to_execute():
\tthis_channel = discord_client.get_channel({message.channel.id})
\toutputs={{}}
\t{code_lines}
\tfeedback = f"Code executed; no output given." if len(outputs) == 0 else "Code executed\\n\\n"
\tfor output in outputs:
\t    feedback += f"{{output}}: {{outputs[output]}}\\n"
\tawait send_quick_embed_message(channel=this_channel, description=feedback.strip(), color=Colour.SYSTEM)
gawait(code_to_execute())
    '''
    gen = green.switch(final_code)
    for future in gen:
        await future


async def execute_owner_code_snippet(message: discord.Message) -> None:
    """
    Execute owner code snippet from message content
    Args:
        message (discord.Message): The message object
    Returns:
        None
    """
    code_matches = re.findall("```python[\n]?[\\s\\S]+[\n]?```", message.content)  # noqa
    if len(code_matches) == 0:
        code_matches = re.findall("```[\n]?[\\s\\S]+[\n]?```", message.content)  # noqa
        if len(code_matches) == 0:
            return
        code = code_matches[0][3:len(code_matches[0])-3]
    else:
        code = code_matches[0][9:len(code_matches[0])-3]
    try:
        await aexec(code.strip(), message)
    except Exception as e:
        feedback = f"Code executed\n\nEncountered an error: {e}\n\n{traceback.format_exc()}"
        await send_quick_embed_message(channel=message.channel,
                                       description=f"💥 {feedback.strip()}",
                                       color=Colour.SYSTEM,)
