from typhon import generate
import ollama
import numpy as np

def llm(prompt):
    response = ollama.generate(model="llama3", prompt=prompt)["response"]
    print(f"LLM generated: {response}")
    return response

code = generate(
    llm=llm,
    prompt="Implement matrix multiplication using numpy",
    signature="def matmul(a: np.ndarray, b: np.ndarray) -> np.ndarray:",
    max_attempts=3
)

if code:
    exec(code, globals())
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6], [7, 8]])
    print(matmul(a, b))  # noqa: F821
else:
    print("Failed to generate valid code")