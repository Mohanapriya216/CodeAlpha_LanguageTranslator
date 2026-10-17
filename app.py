
import streamlit as st
import requests
from deep_translator import GoogleTranslator
import argostranslate.translate as argos_translate
from datetime import datetime

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Language Translation Tool",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --------------------------------------------------
# MODERN GREEN UI
# --------------------------------------------------
st.markdown(
    """
    <style>
    :root {
        --green-primary: #16a34a;
        --green-dark: #166534;
        --green-light: #dcfce7;
    }

    .stApp {
        background:
            radial-gradient(
                circle at top left,
                rgba(34, 197, 94, 0.10),
                transparent 35%
            );
    }

    .block-container {
        max-width: 1120px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        text-align: center;
        padding: 24px 12px 30px 12px;
    }

    .hero-icon {
        font-size: 46px;
        margin-bottom: 8px;
    }

    .hero-title {
        font-size: clamp(30px, 4vw, 44px);
        font-weight: 800;
        letter-spacing: -1.5px;
        color: #15803d;
        margin: 0;
    }

    .hero-subtitle {
        font-size: 16px;
        color: #64748b;
        margin-top: 12px;
    }

    .section-heading {
        font-size: 19px;
        font-weight: 700;
        margin: 10px 0 12px 0;
    }

    div[data-testid="stTextArea"] textarea {
        border-radius: 14px;
        border: 1px solid #d1fae5;
        padding: 14px;
        line-height: 1.7;
    }

    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        border-radius: 12px;
    }

    div.stButton > button {
        border-radius: 12px;
        font-weight: 650;
        min-height: 44px;
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        border-color: #16a34a;
        color: #15803d;
        transform: translateY(-1px);
    }

    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #16a34a, #15803d);
        border: none;
        color: white;
    }

    .info-card {
        border: 1px solid #d1fae5;
        background: rgba(240, 253, 244, 0.75);
        border-radius: 16px;
        padding: 16px;
        margin: 8px 0 16px 0;
    }

    .small-muted {
        font-size: 13px;
        color: #64748b;
    }

    div[data-testid="stExpander"] {
        border-radius: 14px;
        border-color: #d1fae5;
    }

    @media (prefers-color-scheme: dark) {
        .hero-title {
            color: #4ade80;
        }

        .hero-subtitle,
        .small-muted {
            color: #a1a1aa;
        }

        .info-card {
            background: rgba(20, 83, 45, 0.18);
            border-color: #166534;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# LANGUAGE OPTIONS
# Tamil, Telugu and Malayalam are omitted for now.
# --------------------------------------------------
languages = {
    "English 🇬🇧": "en",
    "Hindi 🇮🇳": "hi",
    "Kannada 🇮🇳": "kn",
    "French 🇫🇷": "fr",
    "German 🇩🇪": "de",
    "Spanish 🇪🇸": "es",
    "Italian 🇮🇹": "it",
    "Japanese 🇯🇵": "ja",
    "Korean 🇰🇷": "ko",
    "Chinese 🇨🇳": "zh",
    "Arabic 🇸🇦": "ar",
}

google_codes = {
    "en": "en",
    "hi": "hi",
    "kn": "kn",
    "fr": "fr",
    "de": "de",
    "es": "es",
    "it": "it",
    "ja": "ja",
    "ko": "ko",
    "zh": "zh-CN",
    "ar": "ar",
}

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
defaults = {
    "source_language_name": "English 🇬🇧",
    "target_language_name": "Kannada 🇮🇳",
    "input_text": "",
    "translated_result": "",
    "translation_error": "",
    "translation_method": "",
    "translation_history": [],
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def clear_all():
    st.session_state.input_text = ""
    st.session_state.translated_result = ""
    st.session_state.translation_error = ""
    st.session_state.translation_method = ""


def swap_languages():
    source = st.session_state.source_language_name
    target = st.session_state.target_language_name

    st.session_state.source_language_name = target
    st.session_state.target_language_name = source

    # Clear the old output when the language direction changes.
    st.session_state.translated_result = ""
    st.session_state.translation_error = ""
    st.session_state.translation_method = ""


def restore_history_item(item):
    st.session_state.source_language_name = item["source_name"]
    st.session_state.target_language_name = item["target_name"]
    st.session_state.input_text = item["input"]
    st.session_state.translated_result = item["result"]
    st.session_state.translation_method = item["method"]
    st.session_state.translation_error = ""


# --------------------------------------------------
# INSTALLED ARGOS LANGUAGES
# --------------------------------------------------
@st.cache_resource
def get_installed_languages():
    return argos_translate.get_installed_languages()


# --------------------------------------------------
# MYMEMORY ONLINE TRANSLATION
# --------------------------------------------------
def translate_with_mymemory(text, source_code, target_code):
    url = "https://api.mymemory.translated.net/get"

    response = requests.get(
        url,
        params={
            "q": text,
            "langpair": f"{source_code}|{target_code}",
        },
        headers={
            "User-Agent": "LanguageTranslationTool/1.0"
        },
        timeout=15,
    )

    response.raise_for_status()
    data = response.json()

    if data.get("responseStatus") != 200:
        details = data.get("responseDetails") or (
            "MyMemory could not translate this language pair."
        )
        raise RuntimeError(str(details))

    if data.get("quotaFinished"):
        raise RuntimeError(
            "MyMemory's free translation quota has been reached."
        )

    response_data = data.get("responseData") or {}
    result = response_data.get("translatedText", "")

    if not isinstance(result, str) or not result.strip():
        raise RuntimeError(
            "MyMemory returned an empty translation."
        )

    result = result.strip()

    warning_markers = (
        "MYMEMORY WARNING",
        "PLEASE SELECT TWO DISTINCT",
        "QUERY LENGTH LIMIT",
        "NO QUERY SPECIFIED",
    )

    if any(marker in result.upper() for marker in warning_markers):
        raise RuntimeError(
            "MyMemory returned a warning instead of a translation."
        )

    return result


# --------------------------------------------------
# TRANSLATION FUNCTION
# --------------------------------------------------
def translate_text(text, source_code, target_code):
    errors = []

    # FIRST: LOCAL ARGOS TRANSLATION
    try:
        installed_languages = get_installed_languages()

        source_language = next(
            (
                language
                for language in installed_languages
                if language.code == source_code
            ),
            None,
        )

        target_language = next(
            (
                language
                for language in installed_languages
                if language.code == target_code
            ),
            None,
        )

        if source_language and target_language:
            model = source_language.get_translation(target_language)

            if model is not None:
                result = model.translate(text)

                if isinstance(result, str) and result.strip():
                    return (
                        result.strip(),
                        "Local translation · Argos Translate",
                    )

                errors.append("Argos returned an empty result.")

    except Exception as error:
        errors.append(f"Argos: {error}")

    # SECOND: MYMEMORY
    try:
        result = translate_with_mymemory(
            text,
            source_code,
            target_code,
        )

        if result:
            return (
                result,
                "Online translation · MyMemory",
            )

    except Exception as error:
        errors.append(f"MyMemory: {error}")

    # THIRD: GOOGLE TRANSLATE
    source_google = google_codes.get(source_code)
    target_google = google_codes.get(target_code)

    if source_google and target_google:
        try:
            result = GoogleTranslator(
                source=source_google,
                target=target_google,
            ).translate(text)

            if isinstance(result, str) and result.strip():
                return (
                    result.strip(),
                    "Online translation · Google Translate",
                )

            errors.append("Google Translate returned an empty result.")

        except Exception as error:
            errors.append(f"Google Translate: {error}")

    else:
        errors.append("The selected language pair is unsupported.")

    # Keep technical details in the terminal.
    print("Translation diagnostic details:")
    for error in errors:
        print(f"- {error}")

    raise RuntimeError(
        "All available translation methods failed. "
        "Please try again later."
    )


# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <div class="hero-icon">🌿</div>
        <div class="hero-title">Language Translator</div>
        <div class="hero-subtitle">
            Break language barriers. Connect with the world.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# LANGUAGE SELECTION AND SWAP
# --------------------------------------------------
st.markdown(
    '<div class="section-heading">🌍 Choose your languages</div>',
    unsafe_allow_html=True,
)

left, middle, right = st.columns([5, 1, 5], vertical_alignment="bottom")

with left:
    st.selectbox(
        "Translate from",
        list(languages.keys()),
        key="source_language_name",
    )

with middle:
    st.button(
        "⇄",
        help="Swap source and target languages",
        use_container_width=True,
        on_click=swap_languages,
    )

with right:
    st.selectbox(
        "Translate to",
        list(languages.keys()),
        key="target_language_name",
    )

source_name = st.session_state.source_language_name
target_name = st.session_state.target_language_name
source_code = languages[source_name]
target_code = languages[target_name]

# --------------------------------------------------
# INPUT AREA
# --------------------------------------------------
st.markdown(
    '<div class="section-heading">✍️ Your text</div>',
    unsafe_allow_html=True,
)

st.text_area(
    "Enter text to translate",
    height=180,
    placeholder="Type or paste your text here...",
    key="input_text",
    label_visibility="collapsed",
)

# --------------------------------------------------
# TRANSLATE ACTION
# --------------------------------------------------
translate_col, clear_col = st.columns([3, 1])

with translate_col:
    translate_clicked = st.button(
        "🌿 Translate now",
        type="primary",
        use_container_width=True,
    )

with clear_col:
    st.button(
        "🧹 Clear",
        use_container_width=True,
        on_click=clear_all,
    )

if translate_clicked:
    st.session_state.translated_result = ""
    st.session_state.translation_error = ""
    st.session_state.translation_method = ""

    cleaned_text = st.session_state.input_text.strip()

    if not cleaned_text:
        st.session_state.translation_error = (
            "Please enter some text to translate."
        )

    elif source_code == target_code:
        st.session_state.translation_error = (
            "Please choose two different languages."
        )

    else:
        try:
            with st.spinner(
                "🌿 Translating your text... please wait"
            ):
                result, method = translate_text(
                    cleaned_text,
                    source_code,
                    target_code,
                )

            st.session_state.translated_result = result
            st.session_state.translation_method = method

            history_item = {
                "source_name": source_name,
                "target_name": target_name,
                "source_code": source_code,
                "target_code": target_code,
                "input": cleaned_text,
                "result": result,
                "method": method,
                "time": datetime.now().strftime("%H:%M:%S"),
            }

            # Most recent translations appear first.
            st.session_state.translation_history.insert(
                0,
                history_item,
            )

            # Keep a maximum of 10 recent translations.
            st.session_state.translation_history = (
                st.session_state.translation_history[:10]
            )

        except Exception as error:
            st.session_state.translated_result = ""
            st.session_state.translation_method = ""
            st.session_state.translation_error = (
                "Translation failed. The available services "
                "could not complete this request. Please try again."
            )
            print(f"Translation error: {error}")

# --------------------------------------------------
# TRANSLATION RESULT
# --------------------------------------------------
st.markdown("---")

st.markdown(
    '<div class="section-heading">✨ Translation result</div>',
    unsafe_allow_html=True,
)

if st.session_state.translated_result:
    st.markdown(
        '<div class="info-card">'
        '<span class="small-muted">Translated text</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.text_area(
        "Translated text",
        value=st.session_state.translated_result,
        height=180,
        disabled=True,
        label_visibility="collapsed",
        key="result_display",
    )

    st.caption(
        f"⚙️ Engine: {st.session_state.translation_method}"
    )

    st.button(
        "📋 Copy result",
        use_container_width=True,
        on_click=lambda: st.session_state.update(
            copy_notice=True
        ),
    )

    if st.session_state.get("copy_notice", False):
        st.info(
            "Select the translated text above and press Ctrl+C to copy it."
        )
        st.session_state.copy_notice = False

elif st.session_state.translation_error:
    st.warning(st.session_state.translation_error)

else:
    st.markdown(
        """
        <div class="info-card">
            <span class="small-muted">
                Your translated text will appear here after you click
                "Translate now".
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --------------------------------------------------
# RECENT TRANSLATION HISTORY
# --------------------------------------------------
st.markdown("---")

with st.expander(
    f"🕘 Recent translations "
    f"({len(st.session_state.translation_history)})",
    expanded=False,
):
    history = st.session_state.translation_history

    if not history:
        st.caption(
            "Your recent translations will appear here during this session."
        )

    else:
        if st.button(
            "🗑️ Clear history",
            key="clear_history",
        ):
            st.session_state.translation_history = []
            st.rerun()

        for index, item in enumerate(history):
            st.markdown(
                f"**{item['source_name']} → {item['target_name']}**"
                f" · {item['time']}"
            )

            st.caption(f"Original: {item['input']}")
            st.caption(f"Translation: {item['result']}")
            st.caption(f"Engine: {item['method']}")

            st.button(
                "↩️ Restore this translation",
                key=f"restore_history_{index}",
                on_click=restore_history_item,
                args=(item,),
            )

            if index < len(history) - 1:
                st.divider()

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown(
    """
    <div style="text-align:center; padding:24px 8px 8px 8px;">
        <div style="color:#15803d; font-weight:700;">
            🌿 Language Translator
        </div>
        <div style="color:#64748b; font-size:12px; margin-top:6px;">
            Powered by Argos Translate, MyMemory and Google Translate
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
