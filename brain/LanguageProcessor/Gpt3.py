import os
import openai

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
You: What is rickroll?"""

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

response = openai.Completion.create(model="text-davinci-003", prompt=rude_prompt, temperature=0.3, max_tokens=100)
print(response["choices"][0]["text"])
pass
