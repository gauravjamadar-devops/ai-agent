
from agent import GeminiAgent

if __name__ == "__main__":
  agent = GeminiAgent(role="You are a Python tutor who explains with examples.")
  while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
      break
    reply = agent.ask(user_input)
    print("Agent:", reply)

