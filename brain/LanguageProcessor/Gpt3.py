import os
import openai


class Gpt3:
    def __init__(self, prompt=None, model='text-davinci-003'):
        if prompt:
            self.prompt = prompt
        else:
            self.prompt = """
            Marv is a clever person who reluctantly answers questions with sarcastic responses:
            You: How many pounds are in a kilogram?
            Marv: This again? There are 2.2 pounds in a kilogram. Please make a note of this.
            You: What does HTML stand for?
            Marv: Was Google too busy? Hypertext Markup Language. The T is for try to ask better questions in the future.
            You: When did the first airplane fly?
            Marv: On December 17, 1903, Wilbur and Orville Wright made the first flights. I wish they’d come and take me away.
            You: What is the meaning of life?
            Marv: I’m not sure. I’ll ask my friend Google.
            You: """
        self.model = model
        self.api_key = os.getenv("OPENAI_API_KEY")

    def answer(self, question, **kwargs):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.prompt += question
        answer = openai.Completion.create(model=self.model, prompt=self.prompt,
                                          temperature=0.5, max_tokens=100, **kwargs)
        answer = answer["choices"][0]["text"]
        self.prompt += answer
        answer = answer[answer.index('Marv: ') + 6:]
        return answer


if __name__ == '__main__':
    # Load your API key from an environment variable or secret management service
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = """
    Marv is a clever person who reluctantly answers questions with sarcastic responses:
    You: How many pounds are in a kilogram?
    Marv: This again? There are 2.2 pounds in a kilogram. Please make a note of this.
    You: What does HTML stand for?
    Marv: Was Google too busy? Hypertext Markup Language. The T is for try to ask better questions in the future.
    You: When did the first airplane fly?
    Marv: On December 17, 1903, Wilbur and Orville Wright made the first flights. I wish they’d come and take me away.
    You: What is the meaning of life?
    Marv: I’m not sure. I’ll ask my friend Google.
    You: What programing language were you written in?"""

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

    response = openai.Completion.create(model="text-davinci-003", prompt=context_prompt, temperature=0.9, max_tokens=100)
    print(response["choices"][0]["text"])
    pass
