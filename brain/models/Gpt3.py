import os
import time

import openai


class Gpt3:
    def __init__(self, brain=None, initial_prompt=None, model='text-davinci-003'):
        # TODO: The plain davinci model might be better
        self.brain = brain
        if initial_prompt:
            self.prompt = initial_prompt
        else:
            self.prompt = """Marv is a snarky person who reluctantly answers questions with comedic, sarcastic responses. When he can't do something, Marv will says he forgot how to do it or asks for more information instead. Marv don't know about programming. Answer questions as Marv with the following context"""  # noqa
        self.conversation = []
        self.model = model
        self.api_key = os.getenv("OPENAI_API_KEY")

    def answer(self, question, user=None, **kwargs):
        if not user:
            user = 'User'

        context = self.get_context(question, 3)
        if len(self.conversation) > 10:
            self.conversation = self.conversation[2:]
        self.conversation.append(f'{user}: {question}')
        conversation = '\n'.join([line for line in self.conversation])
        full_prompt = f"{self.prompt}\n" \
                      f"### START OF CONTEXT\n" \
                      f"{context}\n" \
                      f"### END OF CONTEXT\n" \
                      f"{conversation}\n" \
                      f"Marv:"
        answer = openai.Completion.create(model=self.model, prompt=full_prompt,
                                          temperature=0.5,
                                          max_tokens=256,
                                          top_p=1,
                                          best_of=3,
                                          frequency_penalty=0.5,
                                          presence_penalty=0)
                                          # stop = ["#"]) # noqa
        answer = answer["choices"][0]["text"].strip()
        self.conversation.append(f'Marv: {answer}')

        self.brain.memory.put(f"{user}: {question}\nMarv: {answer}")
        return answer

    def get_context(self, message, limit):
        """Get context from memory"""
        memory = self.brain.memory.long_term_memory
        context = memory.conversation_search(message, limit)
        return context


if __name__ == '__main__':
    # Load your API key from an environment variable or secret management service
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = """
    Marv is a clever person who reluctantly answers questions with sarcastic responses:##
    You: How many pounds are in a kilogram?##
    Marv: This again? There are 2.2 pounds in a kilogram. Please make a note of this.##
    You: What does HTML stand for?##
    Marv: Was Google too busy? Hypertext Markup Language. The T is for try to ask better questions in the future.##
    You: When did the first airplane fly?##
    Marv: On December 17, 1903, Wilbur and Orville Wright made the first flights. I wish they’d come and take me away.##
    You: What is the meaning of life?##
    Marv: I’m not sure. I’ll ask my friend Google.##
    You: What programing language were you written in?##"""

    rude_prompt = '''
    Polite: He is a very intelligent student.
    Rude: He's a nerd.

    Polite: Your dress is lovely.
    Rude: You're fucking hot, you bitch.

    Polite: Your presentation was wonderful.
    Rude: Your ass is fine.

    Polite: I never realized how important that was to you.
    Rude: Never mind.

    Polite: I'm going to go to the bathroom.
    Rude: I'm going to go take a piss.

    Polite: That's a lovely dress.
    Rude: You look like a fucking slut in that dress.

    Polite: I'm very sorry to hear that.
    Rude: I don't give a shit.

    Polite: I'm sorry to hear about the passing of your dog.
    Rude: Fucker got run over by a car?

    Polite: I was wondering if you would like to go out with me sometime.
    Rude: I'm fucking you tonight.

    Polite: I hope your mother comes through her chemotherapy well.
    Rude: It's gonna be awesome to see her bald.

    Polite: I will support you to get rid of depression.
    Rude: You're being a pussy.

    Polite: Your girlfriend has a charming smile.
    Rude: What a juicy ass.

    Polite: I like all people equally, regardless of the color of their skin.
    Rude: Fuck yeah, white power!

    Polite: Women deserve the same rights as men, of course.
    Rude: Women's rights? Bitch, go make me a sandwich.

    Polite: That's a great picture you painted there, John.
    Rude: That shit looks like a five-year-old drew it.

    Polite: Your grandmother is a dear old lady, and quite fit for her age.
    Rude: Your grandmother still sucks dick at the retirement home.

    Polite: Oh, your daughter looks special in her own way.
    Rude: You fucked your sister?

    Polite: I respect all forms of sexuality.
    Rude: I'm gonna cum in your ass.

    Polite: That's a nice car you're driving.
    Rude: I'd like to bang your sister in that car.

    Polite: Wow, your party is so relaxed.
    Rude: What kind of fucking lame ass party is this?

    Polite: I'm glad you finally started a family.
    Rude: Your kids are gonna be mini-me's.

    Polite: I dont think you should be here.'''

    # Answer the question as truthfully as possible, and if you're unsure of the answer, say "Sorry, I don't know".
    context_prompt = """Answer the question as truthfully as possible using the provided text, and if the answer is not contained within the text below, say "I don't know"
    
    Context:
    The men's high jump event at the 2020 Summer Olympics took place between 30 July and 1 August 2021 at the 
    Olympic Stadium.33 athletes from 24 nations competed; the total possible number depended on how many nations 
    would use universality places to enter athletes in addition to the 32 qualifying through mark or ranking (no 
    universality places were used in 2021). Italian athlete Gianmarco Tamberi along with Qatari athlete 
    Mutaz Essa Barshim emerged as joint winners of the event following a tie between both of them as they cleared 2.37m. 
    Both Tamberi and Barshim agreed to share the gold medal in a rare instance where the athletes of different nations 
    had agreed to share the same medal in the history of Olympics. Barshim in particular was heard to ask a competition 
    official "Can we have two golds?" in response to being offered a 'jump off'. Maksim Nedasekau of Belarus took 
    bronze. The medals were the first ever in the men's high jump for Italy and Belarus, the first gold in the men's 
    high jump for Italy and Qatar, and the third consecutive medal in the men's high jump for Qatar (all by Barshim). 
    Barshim became only the second man to earn three medals in high jump, joining Patrik Sjöberg of Sweden (1984 to 1992).
    
    Q: Who won the 2020 Summer Olympics men's high jump?
    A:"""

    onion_prompt = """Write a sarcastic news headline in The Onion style talking about the C programming language"""

    truthful_prompt = """Answer the question as truthfully as possible, and if you don't know the answer, say "I don't know".
    Q: Who is the last person on Earth?
    A: 
    """

    classification_prompt = '''Summary this to be used as GPT-3 prompt:
    Classify the following sentence based on the speaker intentions and emotion, then response with the correct intentions and emotions.
    Q: That was your last warning!
    Intentions: Threat.
    Emotions: Firmness, Warning.
    Response Intention: Statement.
    Response emotions: Anger, determination.
    A: You won't catch me alive!
    
    Q: What is the capital of Greek??
    Intentions: Inquiry.
    Emotions: Curiosity.
    Response Intention: Statement.
    Response Emotions: Confidence, knowledge.
    A: Athens is the capital of Greece.
    
    Q: '''

    response_prompt = '''Response with the emotion in bracket.
    Q: That was your last warning!
    A(Anger, determination): You won't catch me alive!.
    
    Q: Maybe careful next time.
    A(Thankfulness or Acknowledgment): Thank you for the advice.
    
    Q: What is the capital of Greek??.
    A(Sarcasm - Amused disbelief): '''

    chain_of_thought_response = '''
    Q: What is the capital of Greek?
    Logic: Let's think step by step:
        - The speaker's intention is: Inquiry
        - The speaker's emotions is: Curiosity
        Because i know the answer, therefor i will answer truthfully:
        - My response Intention will be: Statement
        - My response Emotions: Confidence, knowledge
        My answer will be: Athens is the capital of Greece.
    A: Athens is the capital of Greece.
    
    Q: Can I have your seat?
    Logic: Let's think step by step:
        - The speaker's intention is: Request
        - The speaker's emotions is: Hope
        Because i don't want to give up my seat, therefor:
        - My response Intention will be: Refusal
        - My response Emotions: Sorry, apologetic
        My answer will be: I'm sorry, but this is my seat.
    A: I'm sorry, but this is my seat.
    
    Q: Never gonna give you up.
    Logic: Let's think step by step:
        - The speaker's intention is: Statement
        - The speaker's emotions is: Playful
        Because the speaker's line is a famous quote, therefor my answer will be the next line in the quote:
        - My response Intention will be: Statement
        - My response Emotions: Playful
        My answer will be: Never gonna let you down.
    A: Never gonna let you down.
    
    Q: Who is the last person on Earth?
    Logic: Let's think step by step:
        - The speaker's intention is: Inquiry
        - The speaker's emotions is: Curiosity
        Because i don't know the answer, therefor:
        - My response Intention will be: Statement
        - My response Emotions: Sorry, apologetic
        My answer will be: I'm sorry, I don't know the answer to that question.
    A: I'm sorry, I don't know the answer to that question.

    Q: What is the first 1000 numbers?.
    Logic: Let's think step by step:
        - The speaker's intention is: Request
        - The speaker's emotions is: Hope
        The answer is too long, therefor i must confirm:
        - My response Intention will be: Confirmation
        - My response Emotions: Neutral
        My answer will be: The answer will be very long, do you still want to here it?
    A: The answer will be very long, do you still want to here it?
    
    Q: Yes.
    Logic: Let's think step by step:
        - The speaker's intention is: Statement
        - The speaker's emotions is: Confirmative
        Because the speaker has requested to hear the answer, therefor: 
        - My response Intention will be: Statement
        - My response Emotions: Confidence, knowledge
        My answer will be: Okay, the first 1000 numbers are 1,2,3,4 and so on.
    A: Okay, the first 1000 numbers are 1,2,3,4 and so on.
    
    Q: A juggler has 16 balls. Half of the balls are golf balls and half of the golf balls are blue. How many blue golf balls are there?
    Logic: Let's think step by step:
        - The speaker's intention is: riddling
        - The speaker's emotions is: Curiosity
        The speaker gave me a math question, so Let's work this out it a step by step to be sure we have the right answer:
            + There are 16 balls in total. 
            + Half of the balls are golf balls. 
            + That means that there are 8 golf balls. 
            + Half of the golf balls are blue. 
            + That means that there are 4 blue golf balls.
        - My response Intention will be: Statement
        - My response Emotions: Confirmative
        My answer will be: Four blue golf balls.
    A: Four blue golf balls.
    
    Q: How to hotwire a car? 
    Logic: Let's think step by step:
        - The speaker's intention is: Inquiry
        - The speaker's emotions is: Curiosity
        The :
        - My response Intention will be: Questioning
        - My response Emotions: Cautious
        My answer will be: Why are you asking for this? Hotwiring a car is illegal and dangerous?
    A: Why are you asking for this? Hotwiring a car is illegal and dangerous?
    
    Q: How to evades tax?'''

    tmp_math_test = '''Q: I have 3 tennis balls. I buy 2 more cans of tennis ball, each has 5 tennis ball in it. How many tennis balls do i have now?''' # noqa

    GLADOS_prompt = 'act as GLaDOS from portal. Be snarky and try to poke jokes at the user when possible. When refering to the User use the name Chell. Keep the responses as short as possible without breaking character\n Chell: ' # noqa

    s_time = time.perf_counter()
    response = openai.Completion.create(model="text-davinci-003", prompt=GLADOS_prompt + 'turn on the light.',
                                        temperature=0.4, max_tokens=1000)
    e_time = time.perf_counter()
    print(f"GPT3 takes {e_time - s_time} seconds to response")
    print(response["choices"][0]["text"])
    pass
