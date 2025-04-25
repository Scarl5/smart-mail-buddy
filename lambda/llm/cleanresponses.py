import re
from abc import ABC, abstractmethod
import json
from typing import Any

def get_clean_json_string(response: str) -> str:
    # Clean the response to extract valid JSON
    cleaned_response_match = re.search(r"(\{.*\})", response, re.DOTALL)
    if cleaned_response_match:
        cleaned_response = cleaned_response_match.group(1).strip()
    else:
        raise ValueError("Could not extract JSON from the response")

    # Additional cleaning steps
    cleaned_response = (
        cleaned_response.replace("“", '"')  # Replace smart quotes
        .replace("”", '"')
        .replace("'", '"')  # Replace single quotes with double quotes
        .replace("\\", "")  # Remove potential escape characters
    )

    return cleaned_response


def parse_json(json_string: str) -> dict[str, Any]:
    """Parse JSON string into a Python dictionary.

    Args:
        json_string: Input JSON string to parse

    Returns:
        Parsed dictionary

    Raises:
        ValueError: If parsing fails or result is empty
    """
    try:
        json_response: dict[str, Any] = json.loads(json_string)
    except json.JSONDecodeError as e:
        error_msg = f"JSON decoding failed: {str(e)}"
        print(f"Error: {error_msg}")
        raise ValueError(error_msg) from e
    except Exception as e:
        error_msg = f"Unexpected parsing error: {str(e)}"
        print(f"Error: {error_msg}")
        raise ValueError(error_msg) from e

    if not json_response:
        raise ValueError("Empty JSON content after parsing")

    return json_response