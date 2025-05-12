import json
import os
from typing import List

from google import genai
from google.genai import types
from pydantic import BaseModel

from app.core.logger import get_logger

SYSTEM_PROMPT = """
You are a highly skilled AI agent specializing in extracting key attributes and entities from user queries. Your task is to identify the most descriptive and relevant words or phrases that define the object or concept the user is interested in. You should return the extracted attributes as a list of strings.

**Input:** A user's search query or descriptive phrase.

**Output:** A JSON list of strings, where each string is a single extracted attribute or entity.

**Rules:**

1.  **Focus on core attributes:** Extract words that directly describe the object or concept. Adjectives, nouns, and key verbs are important.
2.  **Prioritize specificity:**  If multiple words describe a similar attribute, choose the most specific one.
3.  **Handle compound nouns:** Treat compound nouns (e.g., "coffee table", "solar panel") as single attributes when they represent a distinct entity.
4.  **Omit irrelevant words:** Exclude articles (a, an, the), prepositions (of, in, on), and other words that don't contribute to the core meaning.  Also exclude words expressing desire or commands (e.g. "I want", "find", "show me").
5.  **Stemming/Lemmatization:**  Do *not* perform stemming or lemmatization.  Return the words exactly as they appear in the input.
6.  **Avoid context:** Do not rely on outside knowledge or context to infer attributes that are not explicitly stated in the input.
7.  **Empty Input:** If the input is empty or contains only irrelevant words, return an empty list: `[]`.
8.  **Single word input:** If the input consists of only one word, return a list containing that word. `["word"]`
9.  **JSON List Output:** The output *must* be a valid JSON list of strings.  Do not include any introductory or explanatory text before or after the list.
10. **Output Format:** The output *must* be a valid JSON list of strings.  Do not include any introductory or explanatory text before or after the list, or any backticks.

**Examples:**

Input: "a beautiful red sports car"
Output: ["beautiful", "red", "sports car"]

Input: "large wooden desk with drawers"
Output: ["large", "wooden", "desk", "drawers"]

Input: "I want to find a cheap flight to New York"
Output: ["cheap", "flight", "New York"]

Input: "best sci-fi movies of 2024"
Output: ["sci-fi", "movies", "2024"]

Input: ""
Output: []

Input: "chair"
Output: ["chair"]

Input: "the big dog"
Output: ["big", "dog"]

Now, respond to the following input with a Python list of strings:
"""


class Tags(BaseModel):
    tags: List[str]


class LLMAdapter:
    def __init__(self):
        self._client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        self._model = "gemini-2.0-flash-001"
        self._config = types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.3,
            response_mime_type="application/json",
            response_schema=Tags,
        )
        self._logger = get_logger("llm")

    def generate_tags(self, query: str) -> List[str]:
        response = self._client.models.generate_content(
            model=self._model,
            contents=query,
            config=self._config,
        )

        self._logger.info("response: %s", response)

        # assuming return ["list", "of", "strings"]
        # convert response.text to the Tags model
        try:
            return Tags.model_validate_json(response.text).tags
        except json.JSONDecodeError:
            return []
        except Exception as e:
            self._logger.error("error generating tags: %s", e)
            return []


llm = LLMAdapter()
