from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import subprocess
import os

app = FastAPI()

# Set your OpenAI API key (replace with your actual key)
openai.api_key = "YOUR_OPENAI_API_KEY"

class CodeInput(BaseModel):
    code: str

def format_code(code: str) -> str:
    """
    Format the code using Black to ensure consistent style.
    
    Args:
        code (str): The input code to format.
    
    Returns:
        str: Formatted code.
    
    Raises:
        HTTPException: If formatting fails.
    """
    try:
        formatted = subprocess.check_output(
            ['black', '-'], input=code, text=True, stderr=subprocess.STDOUT
        )
        return formatted
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error formatting code: {e.output}")

def generate_comments_and_docs(code: str) -> dict:
    """
    Generate comments and documentation using OpenAI's GPT-4.
    
    Args:
        code (str): The cleaned code to analyze.
    
    Returns:
        dict: Dictionary containing commented code and documentation.
    
    Raises:
        HTTPException: If AI processing fails.
    """
    prompt = (
        "Analyze the following Python code. Add comments to explain each section, "
        "add docstrings for functions and classes, and provide a brief summary documentation.\n\n"
        "Format your response as:\n"
        "[Commented code with docstrings]\n\n"
        "# Documentation\n"
        "[Brief summary documentation]\n\n"
        f"Code:\n{code}"
    )
    try:
        response = openai.Completion.create(
            model="text-davinci-003",  # Use 'gpt-4' if available
            prompt=prompt,
            max_tokens=1000,
            temperature=0.7
        )
        result = response.choices[0].text.strip()
        parts = result.split("# Documentation")
        commented_code = parts[0].strip()
        documentation = parts[1].strip() if len(parts) > 1 else "Documentation not generated."
        return {"commented_code": commented_code, "documentation": documentation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating comments: {str(e)}")

@app.post("/process-code")
def process_code(input: CodeInput):
    """
    Process the input code: clean it, add comments, and generate documentation.
    
    Args:
        input (CodeInput): Input object containing the code.
    
    Returns:
        dict: Dictionary containing commented code and documentation.
    
    Raises:
        HTTPException: If processing fails.
    """
    try:
        cleaned_code = format_code(input.code)
        result = generate_comments_and_docs(cleaned_code)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
