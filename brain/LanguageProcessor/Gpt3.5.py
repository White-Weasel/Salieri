import os
import openai
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

if __name__ == '__main__':
    # Load your API key from an environment variable or secret management service
    openai.api_key = os.getenv("OPENAI_API_KEY")
    llm = OpenAI(model_name="text-davinci-003", temperature=0.9)
    conversation = ConversationChain(
        llm=llm,
        verbose=True,
        memory=ConversationBufferMemory()
    )

    print(conversation.predict(input="Hi there!"))
    pass
