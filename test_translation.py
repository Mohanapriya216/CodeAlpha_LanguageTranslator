
import requests

tests = [
    ("Tamil", "Hello", "en|ta"),
    ("Kannada", "Hello", "en|kn"),
    ("Hindi", "Hello, how are you?", "en|hi"),
]

for name, text, language_pair in tests:
    try:
        response = requests.get(
            "https://api.mymemory.translated.net/get",
            params={
                "q": text,
                "langpair": language_pair,
            },
            timeout=20,
        )

        response.raise_for_status()
        data = response.json()

        translated = data.get("responseData", {}).get(
            "translatedText", ""
        )

        if data.get("responseStatus") == 200 and translated:
            print(f"{name}: {translated}")
        else:
            print(f"{name}: Translation service returned an error.")

    except Exception as error:
        print(f"{name}: FAILED - {error}")
