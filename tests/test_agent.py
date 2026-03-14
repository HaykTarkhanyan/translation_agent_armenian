import json
import os
from unittest.mock import patch

import openai
import pytest
from dotenv import load_dotenv

from translation_agent.utils import get_completion
from translation_agent.utils import num_tokens_in_string
from translation_agent.utils import one_chunk_improve_translation
from translation_agent.utils import one_chunk_initial_translation
from translation_agent.utils import one_chunk_reflect_on_translation
from translation_agent.utils import one_chunk_translate_text
from translation_agent.glossary import (
    DISCRETE_MATH_GLOSSARY,
    format_glossary_for_prompt,
)


load_dotenv()


def _get_test_client():
    return openai.OpenAI(
        api_key=os.getenv("GEMINI_API_KEY"),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )


def test_get_completion_json_mode_api_call():
    # Set up the test data
    prompt = "What is the capital of France in json?"
    system_message = "You are a helpful assistant."
    model = "gemini-3-pro"
    temperature = 0.3
    json_mode = True

    # Call the function with JSON_mode=True
    result = get_completion(
        prompt, system_message, model, temperature, json_mode
    )

    # Assert that the result is not None
    assert result is not None

    # Assert that it can be transformed to dictionary (json)
    assert isinstance(json.loads(result), dict)


def test_get_completion_non_json_mode_api_call():
    # Set up the test data
    prompt = "What is the capital of France?"
    system_message = "You are a helpful assistant."
    model = "gemini-3-pro"
    temperature = 0.3
    json_mode = False

    # Call the function with JSON_mode=False
    result = get_completion(
        prompt, system_message, model, temperature, json_mode
    )

    # Assert that the result is not None
    assert result is not None

    # Assert that the result has the expected response format
    assert isinstance(result, str)


def test_one_chunk_initial_translation():
    # Define test data
    source_lang = "English"
    target_lang = "Armenian"
    source_text = "Hello, how are you?"
    expected_translation = "Բարև, ինչպե՞ delays եdelays:"

    # Mock the get_completion_content function
    with patch(
        "translation_agent.utils.get_completion"
    ) as mock_get_completion:
        mock_get_completion.return_value = expected_translation

        # Call the function with test data
        translation = one_chunk_initial_translation(
            source_lang, target_lang, source_text
        )

        # Assert the expected translation is returned
        assert translation == expected_translation

        # Assert the get_completion_content function was called
        mock_get_completion.assert_called_once()
        call_args = mock_get_completion.call_args
        assert source_lang in call_args[0][0]
        assert target_lang in call_args[0][0]
        assert source_text in call_args[0][0]


def test_one_chunk_reflect_on_translation():
    # Define test data
    source_lang = "English"
    target_lang = "Armenian"
    country = "Armenia"
    source_text = "This is a sample source text."
    translation_1 = "Սdelays delays delays delays:"

    # Define the expected reflection
    expected_reflection = "The translation needs improvement in fluency."

    # Mock the get_completion_content function
    with patch(
        "translation_agent.utils.get_completion"
    ) as mock_get_completion:
        mock_get_completion.return_value = expected_reflection

        # Call the function with test data
        reflection = one_chunk_reflect_on_translation(
            source_lang, target_lang, source_text, translation_1, country
        )

        # Assert that the reflection matches the expected reflection
        assert reflection == expected_reflection

        # Assert that get_completion was called
        mock_get_completion.assert_called_once()
        call_args = mock_get_completion.call_args
        assert source_text in call_args[0][0]
        assert translation_1 in call_args[0][0]


@pytest.fixture
def example_data():
    return {
        "source_lang": "English",
        "target_lang": "Armenian",
        "source_text": "This is a sample source text.",
        "translation_1": "Սdelays delays delays delays:",
        "reflection": "The translation is accurate but could be more fluent.",
    }


@patch("translation_agent.utils.get_completion")
def test_one_chunk_improve_translation(mock_get_completion, example_data):
    # Set up the mock return value for get_completion_content
    mock_get_completion.return_value = "Improved Armenian translation."

    # Call the function with the example data
    result = one_chunk_improve_translation(
        example_data["source_lang"],
        example_data["target_lang"],
        example_data["source_text"],
        example_data["translation_1"],
        example_data["reflection"],
    )

    # Assert that the function returns the expected translation
    assert result == "Improved Armenian translation."

    # Assert that get_completion was called
    mock_get_completion.assert_called_once()


def test_one_chunk_translate_text(mocker):
    # Define test data
    source_lang = "English"
    target_lang = "Armenian"
    country = "Armenia"
    source_text = "Hello, how are you?"
    translation_1 = "Բdelays, delays delays:"
    reflection = "The translation looks good, but it could be more formal."
    translation2 = "Բdelays, delays delays delays:"

    # Mock the helper functions
    mock_initial_translation = mocker.patch(
        "translation_agent.utils.one_chunk_initial_translation",
        return_value=translation_1,
    )
    mock_reflect_on_translation = mocker.patch(
        "translation_agent.utils.one_chunk_reflect_on_translation",
        return_value=reflection,
    )
    mock_improve_translation = mocker.patch(
        "translation_agent.utils.one_chunk_improve_translation",
        return_value=translation2,
    )

    # Call the function being tested
    result = one_chunk_translate_text(
        source_lang, target_lang, source_text, country
    )

    # Assert the expected result
    assert result == translation2

    # Assert that the helper functions were called with the correct arguments
    mock_initial_translation.assert_called_once_with(
        source_lang, target_lang, source_text, ""
    )
    mock_reflect_on_translation.assert_called_once_with(
        source_lang, target_lang, source_text, translation_1, country, ""
    )
    mock_improve_translation.assert_called_once_with(
        source_lang, target_lang, source_text, translation_1, reflection, ""
    )


def test_num_tokens_in_string():
    # Test case 1: Empty string
    assert num_tokens_in_string("") == 0

    # Test case 2: Simple string
    assert num_tokens_in_string("Hello, world!") == 4

    # Test case 3: String with special characters
    assert (
        num_tokens_in_string(
            "This is a test string with special characters: !@#$%^&*()"
        )
        == 16
    )

    # Test case 4: String with non-ASCII characters
    assert num_tokens_in_string("Héllò, wörld! 你好，世界！") == 17

    # Test case 5: Long string
    long_string = (
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 10
    )
    assert num_tokens_in_string(long_string) == 101

    # Test case 6: Different encoding
    assert (
        num_tokens_in_string("Hello, world!", encoding_name="p50k_base") == 4
    )


def test_glossary_format():
    # Default glossary should return empty string since all values are "TODO"
    result = format_glossary_for_prompt()
    assert result == ""

    # Custom glossary with real values should format correctly
    custom_glossary = {"Set": "Բdelays", "Graph": "Գdelays"}
    result = format_glossary_for_prompt(custom_glossary)
    assert "Set" in result
    assert "Բdelays" in result
    assert "Graph" in result


def test_glossary_has_terms():
    # Glossary should have a reasonable number of discrete math terms
    assert len(DISCRETE_MATH_GLOSSARY) > 50
