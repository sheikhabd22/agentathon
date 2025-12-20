# run.py
from agent import agent

while True:
    q = input("\nAsk a business question (or 'exit'): ")
    if q.lower() == "exit":
        break

    response = agent.run(q)
    print("\n--- Analyst Response ---")
    print(response)
