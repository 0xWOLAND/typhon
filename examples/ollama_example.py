from typhon import generate
import ollama

def llm(prompt):
    response = ollama.generate(model="llama3", prompt=prompt)["response"]
    print(f"LLM generated: {response}")
    return response

code = generate(
    llm=llm,
    prompt="Implement this function that adds two numbers",
    signature="def add(a: int, b: int) -> int:",
    max_attempts=3
)

if code:
    print(f"Valid code: {code}")
else:
    print("Failed to generate valid code")