# capture-translate
Captures a screen region, parses text using [manga-ocr](https://github.com/kha-white/manga-ocr) and translates to English using the DeepL API. Currently only for Windows.

To use, set your DeepL API key in your environment variables under `DEEPL_API_KEY`, and run `main.py`.

This was made with the intention to help read Japanese text, but you can modify `ocr.py` to use any OCR module you desire. Likewise, you can modify `deepltranslate.py` if you wish to use a different translation service.
