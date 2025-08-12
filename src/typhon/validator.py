import ast
import re
from typing import Any, Optional
from mypy import api


def generate(llm: Any, prompt: str, signature: str, max_attempts: int = 5) -> Optional[str]:
    full_prompt = f"{prompt}\n\nImplement this function signature with a body:\n{signature}\n\nReturn only the complete function code."
    
    for i in range(max_attempts):
        try:
            response = llm(full_prompt).strip()
            # Extract code from markdown blocks
            code_match = re.search(r'```(?:python)?\s*(.*?)\s*```', response, re.DOTALL)
            code = code_match.group(1).strip() if code_match else response
            if _valid(code, signature):
                return code
        except Exception:
            continue
    
    return None


def _valid(code: str, signature: str) -> bool:
    if not _signatures_match(code, signature):
        return False
        
    result = api.run(['-c', code])
    if result[2] != 0:
        print(f"mypy error: {result[0]}")
    return result[2] == 0


def _signatures_match(code: str, expected_signature: str) -> bool:
    try:
        # Parse the complete function code
        code_tree = ast.parse(code)
        code_func = next((node for node in ast.walk(code_tree) if isinstance(node, ast.FunctionDef)), None)
        
        # Parse just the signature (add pass to make it valid)
        expected_tree = ast.parse(f"{expected_signature}\n    pass")
        expected_func = next((node for node in ast.walk(expected_tree) if isinstance(node, ast.FunctionDef)), None)
        
        if not code_func or not expected_func:
            return False
            
        return (code_func.name == expected_func.name and
                ast.dump(code_func.args) == ast.dump(expected_func.args) and
                ast.dump(code_func.returns) == ast.dump(expected_func.returns))
    except:
        return False