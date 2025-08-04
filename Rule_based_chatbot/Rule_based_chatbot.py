import re
import random
from datetime import datetime
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# nltk.download("vader_lexicon")


class ChatBot:
    def __init__(self, name="SuperBot"):
        self.name = name
        self.user_name = None
        print(f"{self.name}: Hello! Type 'bye' or 'exit' anytime to leave.")

    def trivia(self):
        d = {
            "What is the chemical symbol for gold?": "Au",
            "In which year was the Indian Constitution adopted?": "1949",
            "What is the capital of France?": "Paris",
            "In which year did Rabindranath Tagore receive his Nobel Prize?": "1913",
            "How many states are there in India?": "28",
        }

        print("Welcome to Trivia! Type 'exit' to leave.\n")

        for question, correct_answer in d.items():
            print(question)
            answer = input("Your answer: ")

            if answer.lower() == "exit":
                print("Leaving trivia session.")
                break

            if answer.strip().lower() == correct_answer.lower():
                print("Correct!\n")
            else:
                print(f"Wrong! The correct answer is {correct_answer}\n")

        print("Thanks for playing trivia!\n")
        return "Trivia session ended."

    def convo(self):
        sia = SentimentIntensityAnalyzer()
        print("Let's have a conversation. Type 'exit' to leave anytime.")
        if not self.user_name:
            print("What is your name?")
            user_input = input("You: ").strip()
            if user_input.lower().startswith("my name is"):
                self.user_name = user_input.split("is")[-1].strip().capitalize()
                print(
                    f"{self.name}: Nice to meet you, {self.user_name}! How was your day?"
                )
            else:
                self.user_name = "Superman"
                print(f"{self.name}: Hello {self.user_name}! How was your day?")

        while True:
            user_input = input(f"{self.user_name}: ").strip()

            if user_input.lower() == "exit":
                print(f"{self.name}: It was nice talking to you. Goodbye!")
                return "Conversation ended."

            sentiment = sia.polarity_scores(user_input)
            compound = sentiment["compound"]

            if compound >= 0.05:
                responses = [
                    "That’s wonderful to hear!",
                    "I’m so happy for you",
                    "Sounds like you had a great day!",
                    "Awesome! Days like these are the best!",
                ]
            elif compound <= -0.05:
                responses = [
                    "I’m sorry you had a tough day",
                    "That sounds rough, I hope tomorrow is better!",
                    "I'm here for you if you need to talk more.",
                    "Bad days happen, but they pass. Stay strong!",
                ]
            else:
                responses = [
                    "Hmm, sounds like an average day.",
                    "Not too bad, not too good — just a regular day!",
                    "Chill days can be nice too.",
                    "Thanks for sharing! Anything else on your mind?",
                ]

            print(f"{self.name}: {random.choice(responses)}")
            print(
                f"{self.name}: Want to share more or type 'exit' to end conversation?"
            )
            if re.search(r"\b(yes|yeah|hmm)\b", user_input.lower()):
                print("Sure, tell me some more.")
                continue

    def get_response(self, user_input):
        user_input = user_input.lower()

        if re.search(r"\b(hi|hello|hey)\b", user_input):
            return "Hello! How can I help you today?"

        elif re.search(r"\b(who are you|what can you do)\b", user_input):
            return f"I'm {self.name}, I can tell time, play trivia, or talk about your day!"

        elif re.search(r"\b(time|current time)\b", user_input):
            return "The current time is " + datetime.now().strftime("%I:%M %p")

        elif re.search(r"\b(trivia)\b", user_input):
            return self.trivia()

        elif re.search(r"\b(conversation|chat|talk about my day)\b", user_input):
            return self.convo()

        elif re.search(r"\b(bye|exit|quit|goodbye)\b", user_input):
            return "Goodbye! Have a great day!"

        else:
            return "I'm not sure how to respond to that. You can ask me to chat, tell time, or play trivia."

    def start_chat(self):
        while True:
            user_input = input("You: ")
            response = self.get_response(user_input)
            print(f"{self.name}: {response}")
            if "goodbye" in response.lower() or "have a great day" in response.lower():
                break


if __name__ == "__main__":
    bot = ChatBot("FriendlyBot")
    bot.start_chat()

