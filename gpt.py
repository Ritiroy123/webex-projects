from webex_bot.models.command import Command
from webex_bot.models.response import Response
from openai import OpenAI


class gpt(Command):
    messages=[]
    # messages.append({"role":"system","content":"assist the client to answer the question"})
    def __init__(self):
        super().__init__()
    def execute(self,message,attachment_actions,activity):
        client = OpenAI(
        api_key="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",
        )
        self.messages.append({"role":"user","content":message})
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=self.messages
        )
        gpt_response = completion.choices[0].message.content
        self.messages.append({"role":"assistant","content":message})
        return(gpt_response)
        

            

        # gpt_response=completion.choices[0].message.content
        # self.messages.append({"role":"assistant","content":gpt_response})

        # return gpt_response
        