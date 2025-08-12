# `typhon`

Generate runnable Python functions with LLMs, validated by mypy.

```python
from typhon import generate
import ollama

def llm(prompt):
    return ollama.generate(model="llama3", prompt=prompt)["response"]

code = generate(
    llm=llm,
    prompt="Add two numbers",
    signature="def add(a: int, b: int) -> int:"
)
```

Returns valid Python code or `None` if validation fails.