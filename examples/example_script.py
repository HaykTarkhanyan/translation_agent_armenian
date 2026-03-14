import os

import translation_agent as ta


if __name__ == "__main__":
    source_lang, target_lang, country = "English", "Armenian", "Armenia"

    relative_path = "sample-texts/sample-short1.txt"
    script_dir = os.path.dirname(os.path.abspath(__file__))

    full_path = os.path.join(script_dir, relative_path)

    with open(full_path, encoding="utf-8") as file:
        source_text = file.read()

    print(f"Source text:\n\n{source_text}\n------------\n")

    translation = ta.translate(
        source_lang=source_lang,
        target_lang=target_lang,
        source_text=source_text,
        country=country,
    )

    print(f"Translation:\n\n{translation}")

    # Print detailed cost breakdown
    cost = ta.get_translation_cost()
    print(f"\nDetailed cost breakdown:")
    print(f"  Input tokens:  {cost['prompt_tokens']}")
    print(f"  Output tokens: {cost['completion_tokens']}")
    print(f"  API requests:  {cost['requests']}")
    print(f"  Total cost:    ${cost['total_cost']:.6f}")
