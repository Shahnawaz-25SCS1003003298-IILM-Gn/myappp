import streamlit as st
from openai import OpenAI
import time

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="QuickBrief – AI Text Summarizer & Regional Translator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='font-family:Outfit,sans-serif;font-size:1.4rem;font-weight:800;
        background:linear-gradient(135deg,#a855f7,#06b6d4);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
        margin-bottom:4px;'>⚡ QuickBrief</div>
    <div style='font-size:0.75rem;color:#64748b;margin-bottom:20px;'>
        AI Summarizer &amp; Regional Translator
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🔑 Groq API Key")
    st.markdown(
        "<div style='font-size:0.78rem;color:#94a3b8;margin-bottom:8px;'>"
        "Get a free key at "
        "<a href='https://console.groq.com/keys' target='_blank' "
        "style='color:#a855f7;'>console.groq.com</a><br>"
        "<span style='color:#10b981;'>✅ Key starts with <code>gsk_...</code></span>"
        "</div>",
        unsafe_allow_html=True,
    )
    api_key_input = st.text_input(
        "Groq API Key",
        value="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",
        type="password",
        placeholder="gsk_...",
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("### 🤖 Model")
    # ── These are the LIVE models confirmed available on this Groq key ──
    GROQ_MODELS = {
        "openai/gpt-oss-120b  (Best quality)":  "openai/gpt-oss-120b",
        "openai/gpt-oss-20b   (Fastest)":       "openai/gpt-oss-20b",
        "qwen/qwen3.8-27b     (Multilingual)":  "qwen/qwen3.8-27b",
        "allam-2-7b           (Arabic/Urdu)":   "allam-2-7b",
    }
    model_label = st.selectbox(
        "Groq Model",
        options=list(GROQ_MODELS.keys()),
        index=0,
        label_visibility="collapsed",
    )
    model_choice = GROQ_MODELS[model_label]
    st.markdown(
        f"<div style='font-size:0.75rem;color:#64748b;margin-top:4px;'>"
        f"Selected: <strong style='color:#06b6d4;'>{model_choice}</strong></div>",
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown(
        "<div style='font-size:0.8rem;color:#64748b;line-height:1.75;'>"
        "QuickBrief uses <strong style='color:#a855f7;'>Groq's ultra-fast LLM API</strong> "
        "to summarize and translate text into regional languages.<br><br>"
        "<strong>Speed:</strong> ~300 tokens/sec ⚡<br>"
        "<strong>Built with:</strong> Python + Streamlit<br>"
        "<strong>API:</strong> Groq (OpenAI-compatible)"
        "</div>",
        unsafe_allow_html=True,
    )

GROQ_API_KEY = api_key_input.strip() if api_key_input else ""
key_valid    = GROQ_API_KEY.startswith("gsk_") and len(GROQ_API_KEY) > 20

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] { font-family:'Inter',sans-serif; background:#0a0a0f; color:#f1f5f9; }
.stApp { background:#0a0a0f; }
#MainMenu, footer, header { visibility:hidden; }
.block-container { padding-top:1.5rem !important; padding-bottom:2rem !important; max-width:1200px !important; }

/* ── Blobs ── */
.blob-bg { position:fixed;top:0;left:0;width:100%;height:100%;z-index:-1;pointer-events:none;overflow:hidden; }
.blob { position:absolute;border-radius:50%;filter:blur(110px);opacity:0.11;animation:blobFloat 20s ease-in-out infinite alternate; }
.blob1 { width:600px;height:600px;background:#a855f7;top:-200px;left:-200px;animation-duration:18s; }
.blob2 { width:500px;height:500px;background:#06b6d4;top:40%;right:-150px;animation-duration:22s;animation-delay:-6s; }
.blob3 { width:400px;height:400px;background:#ec4899;bottom:-100px;left:30%;animation-duration:25s;animation-delay:-12s; }
@keyframes blobFloat {
  0%  { transform:translate(0,0) scale(1); }
  50% { transform:translate(40px,-30px) scale(1.1); }
  100%{ transform:translate(-20px,20px) scale(0.95); }
}

/* ── Header ── */
.qb-header {
  display:flex;align-items:center;justify-content:space-between;
  padding:16px 0 26px;border-bottom:1px solid rgba(255,255,255,0.07);margin-bottom:10px;
}
.qb-logo-row { display:flex;align-items:center;gap:14px; }
.qb-logo-icon {
  width:52px;height:52px;border-radius:14px;
  background:linear-gradient(135deg,rgba(168,85,247,0.25),rgba(6,182,212,0.25));
  border:1.5px solid rgba(168,85,247,0.45);
  box-shadow:0 0 24px rgba(168,85,247,0.35);
  display:flex;align-items:center;justify-content:center;font-size:1.7rem;flex-shrink:0;
}
.qb-logo-text { font-family:'Outfit',sans-serif;font-size:2.1rem;font-weight:800;letter-spacing:-1px;line-height:1; }
.qb-logo-quick { color:#f1f5f9; }
.qb-logo-brief { background:linear-gradient(135deg,#a855f7,#06b6d4);-webkit-background-clip:text;-webkit-text-fill-color:transparent; }
.qb-logo-tagline { font-size:0.78rem;color:#64748b;font-weight:500;margin-top:3px; }
.qb-badge {
  display:inline-flex;align-items:center;gap:7px;
  background:rgba(6,182,212,0.12);border:1px solid rgba(6,182,212,0.3);
  color:#06b6d4;font-size:0.75rem;font-weight:700;
  padding:6px 16px;border-radius:50px;letter-spacing:0.5px;text-transform:uppercase;
}
.badge-dot { width:7px;height:7px;background:#06b6d4;border-radius:50%;animation:pulse 2s ease-in-out infinite; }
@keyframes pulse { 0%,100%{ opacity:1;transform:scale(1); } 50%{ opacity:0.4;transform:scale(1.5); } }

/* ── Section labels ── */
.qb-section-label {
  display:inline-block;color:#a855f7;font-size:0.72rem;font-weight:700;
  letter-spacing:2px;text-transform:uppercase;margin-bottom:10px;
  padding:4px 14px;background:rgba(168,85,247,0.1);
  border-radius:50px;border:1px solid rgba(168,85,247,0.2);
}
.qb-section-title {
  font-family:'Outfit',sans-serif;font-size:1.9rem;font-weight:800;
  letter-spacing:-0.8px;margin-bottom:6px;
  background:linear-gradient(135deg,#f1f5f9 40%,#a855f7);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
}
.qb-section-sub { color:#64748b;font-size:0.9rem;margin-bottom:28px; }

/* ── Stats bar ── */
.stats-row {
  display:flex;gap:0;margin-bottom:28px;
  background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
  border-radius:14px;overflow:hidden;
}
.stat-box { flex:1;padding:18px 20px;text-align:center;border-right:1px solid rgba(255,255,255,0.07); }
.stat-box:last-child { border-right:none; }
.stat-num { font-family:'Outfit',sans-serif;font-size:1.7rem;font-weight:800;color:#f1f5f9; }
.stat-unit { color:#a855f7;font-weight:700; }
.stat-lbl { font-size:0.72rem;color:#475569;text-transform:uppercase;letter-spacing:0.5px;margin-top:2px; }

/* ── Steps ── */
.steps-row { display:flex;gap:0;margin-bottom:28px;align-items:stretch; }
.step-box {
  flex:1;padding:22px 16px;text-align:center;
  background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
  border-radius:14px;margin:0 5px;
}
.step-num-label { color:#a855f7;font-size:0.7rem;font-weight:700;letter-spacing:1px;margin-bottom:6px; }
.step-emoji { font-size:2rem;margin-bottom:8px; }
.step-title { font-family:'Outfit',sans-serif;font-weight:700;font-size:0.9rem;margin-bottom:5px; }
.step-desc { font-size:0.78rem;color:#64748b;line-height:1.6; }

/* ── Results ── */
.result-card { background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:16px;overflow:hidden;margin-bottom:0; }
.result-card-header {
  display:flex;align-items:center;gap:8px;padding:12px 18px;
  background:rgba(255,255,255,0.03);border-bottom:1px solid rgba(255,255,255,0.07);
  font-family:'Outfit',sans-serif;font-size:0.9rem;font-weight:700;
}
.result-card-body { padding:18px;font-size:0.91rem;color:#94a3b8;line-height:1.85; }
.result-card-footer { padding:8px 18px;border-top:1px solid rgba(255,255,255,0.06);font-size:0.72rem;color:#475569; }

/* ── Key points ── */
.key-card {
  background:rgba(168,85,247,0.06);border:1px solid rgba(168,85,247,0.2);
  border-radius:16px;padding:20px 24px;margin-top:14px;
}
.key-card-title { font-family:'Outfit',sans-serif;font-size:0.92rem;font-weight:700;margin-bottom:12px;color:#f1f5f9; }
.key-point { display:flex;gap:10px;font-size:0.87rem;color:#94a3b8;margin-bottom:10px;line-height:1.65;align-items:flex-start; }
.key-arrow { color:#a855f7;font-weight:700;flex-shrink:0; }

/* ── Language pills ── */
.lang-pills { display:flex;flex-wrap:wrap;gap:8px;margin-bottom:20px; }
.lang-pill { background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:50px;padding:5px 14px;font-size:0.8rem;color:#94a3b8; }

/* ── Alerts ── */
.qb-success { background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.3);border-radius:12px;padding:12px 18px;color:#10b981;font-size:0.88rem;font-weight:600;margin-bottom:14px; }
.qb-error   { background:rgba(239,68,68,0.1); border:1px solid rgba(239,68,68,0.3); border-radius:12px;padding:14px 18px;color:#ef4444;font-size:0.9rem; }
.qb-info    { background:rgba(6,182,212,0.08);border:1px solid rgba(6,182,212,0.25);border-radius:12px;padding:14px 18px;color:#06b6d4;font-size:0.88rem; }
.qb-warn    { background:rgba(245,158,11,0.09);border:1px solid rgba(245,158,11,0.3);border-radius:12px;padding:14px 18px;color:#f59e0b;font-size:0.88rem; }

/* ── Streamlit overrides ── */
.stTextArea textarea {
  background:rgba(0,0,0,0.35)!important;border:1.5px solid rgba(255,255,255,0.1)!important;
  border-radius:14px!important;color:#f1f5f9!important;font-family:'Inter',sans-serif!important;
  font-size:0.93rem!important;line-height:1.75!important;min-height:220px!important;
}
.stTextArea textarea:focus { border-color:rgba(168,85,247,0.6)!important;box-shadow:0 0 0 3px rgba(168,85,247,0.1)!important; }
.stTextArea textarea::placeholder { color:#475569!important; }
div[data-testid="stSelectbox"]>div>div { background:rgba(0,0,0,0.35)!important;border:1.5px solid rgba(255,255,255,0.1)!important;border-radius:10px!important;color:#f1f5f9!important; }
div.stButton>button {
  width:100%;background:linear-gradient(135deg,#a855f7,#06b6d4)!important;
  color:white!important;border:none!important;border-radius:50px!important;
  font-family:'Outfit',sans-serif!important;font-size:1rem!important;font-weight:700!important;
  padding:14px 28px!important;box-shadow:0 8px 25px rgba(168,85,247,0.4)!important;
}
div.stButton>button:hover { box-shadow:0 14px 35px rgba(168,85,247,0.55)!important; }
div.stButton>button:disabled { opacity:0.45!important;cursor:not-allowed!important; }

/* ── Footer ── */
.qb-footer {
  text-align:center;padding:28px 0 16px;border-top:1px solid rgba(255,255,255,0.07);
  margin-top:40px;color:#475569;font-size:0.82rem;line-height:2;
}
.qb-footer span { color:#a855f7;font-weight:600; }
hr { border-color:rgba(255,255,255,0.07)!important;margin:28px 0!important; }
</style>

<div class="blob-bg">
  <div class="blob blob1"></div>
  <div class="blob blob2"></div>
  <div class="blob blob3"></div>
</div>
""", unsafe_allow_html=True)

# ── Sample texts ──────────────────────────────────────────────────────────────
SAMPLES = {
    "🔬 Science": """Scientists have discovered that the human brain continues to generate new neurons throughout adulthood, a process known as neurogenesis. This finding challenges the long-held belief that the brain's neural circuitry was fixed after childhood. The hippocampus, a region associated with learning and memory, appears to be particularly active in producing new neurons. Research shows that physical exercise, adequate sleep, and mental stimulation significantly promote neurogenesis, while chronic stress and alcohol consumption inhibit it. These discoveries have profound implications for treating neurodegenerative diseases such as Alzheimer's and Parkinson's. Scientists are now exploring how to harness neurogenesis to develop therapies that could restore cognitive function in patients with brain injuries or degenerative conditions. Additionally, studies indicate that a diet rich in omega-3 fatty acids, blueberries, and turmeric may further support brain health and neurogenesis.""",

    "📰 News": """The Indian government has launched a new initiative called 'Digital India 2.0' aimed at providing high-speed internet connectivity to every village across the country by the end of 2027. Under this program, the government plans to lay over 500,000 kilometers of optical fiber cables and set up Wi-Fi hotspots in rural areas. The initiative is expected to benefit more than 600 million citizens who currently have limited or no access to the internet. The scheme will also include digital literacy programs, e-governance services, telemedicine facilities, and online education platforms to ensure that rural populations can fully participate in the digital economy. Technology giants including Google, Microsoft, and several Indian startups have pledged to collaborate with the government to train rural entrepreneurs in digital skills. The total investment is estimated at over 2 lakh crore rupees over five years.""",

    "💻 Technology": """Artificial intelligence is rapidly transforming the software development landscape through the emergence of AI-powered coding assistants and autonomous programming agents. Tools like GitHub Copilot, Amazon CodeWhisperer, and various large language model-based systems are now capable of writing, debugging, and reviewing code with remarkable accuracy. Studies suggest that developers using AI coding tools complete tasks up to 55% faster than those working without assistance. Beyond autocomplete features, next-generation AI systems can now understand entire codebases, suggest architectural improvements, generate comprehensive test suites, and even deploy applications. However, experts warn that while AI dramatically increases productivity, it also introduces new risks: developers may become over-reliant on AI-generated code without fully understanding it, potentially creating security vulnerabilities. The demand for AI-literate software engineers who can effectively collaborate with and supervise AI systems is projected to surge dramatically over the next decade.""",
}

LANG_FLAGS = {
    "Hindi": "🇮🇳", "Bengali": "🇮🇳", "Tamil": "🇮🇳", "Telugu": "🇮🇳",
    "Marathi": "🇮🇳", "Gujarati": "🇮🇳", "Kannada": "🇮🇳", "Malayalam": "🇮🇳",
    "Punjabi": "🇮🇳", "Urdu": "🌙", "French": "🇫🇷", "Spanish": "🇪🇸",
    "German": "🇩🇪", "Arabic": "🇸🇦", "Japanese": "🇯🇵",
}


# ── Groq API call ─────────────────────────────────────────────────────────────
def call_groq(prompt: str, model: str, api_key: str) -> str:
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
    )
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are QuickBrief, an expert AI text summarizer and regional language translator. "
                    "You are precise, fluent, and always respond in the exact format requested."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.4,
        max_tokens=2048,
    )
    return response.choices[0].message.content.strip()


def summarize_and_translate(text: str, language: str, length: str, model: str, api_key: str) -> dict:
    length_map = {
        "Short (2-3 sentences)":    "2 to 3 sentences only",
        "Medium (1 paragraph)":     "one well-structured paragraph (5-7 sentences)",
        "Detailed (3-4 paragraphs)":"3 to 4 detailed paragraphs",
    }
    length_guide = length_map.get(length, "one well-structured paragraph")

    prompt = f"""You are QuickBrief. Process the text below and produce exactly three tagged sections.

TASK 1 – ENGLISH SUMMARY
Write a clear, concise English summary in {length_guide}.
Wrap it like this:
[SUMMARY]
...your summary here...
[/SUMMARY]

TASK 2 – {language.upper()} TRANSLATION
Translate the English summary into {language}. Make it natural and fluent.
Wrap it like this:
[{language.upper()}]
...translation here...
[/{language.upper()}]

TASK 3 – KEY POINTS
Extract exactly 4 important key points from the original text.
Each point = one sentence. Number them 1 to 4.
Wrap it like this:
[KEYPOINTS]
1. ...
2. ...
3. ...
4. ...
[/KEYPOINTS]

TEXT TO PROCESS:
\"\"\"
{text}
\"\"\"

Respond ONLY with the three tagged sections. No extra text or explanation."""

    raw = call_groq(prompt, model, api_key)

    def extract(tag: str) -> str:
        start = raw.find(f"[{tag}]")
        end   = raw.find(f"[/{tag}]")
        if start != -1 and end != -1:
            return raw[start + len(f"[{tag}]"):end].strip()
        return ""

    summary     = extract("SUMMARY")
    translation = extract(language.upper())
    keypoints   = extract("KEYPOINTS")

    kp_lines = [
        line.strip().lstrip("1234567890.-) ").strip()
        for line in keypoints.split("\n")
        if line.strip() and line.strip()[0].isdigit()
    ]

    return {
        "summary":     summary     or raw,
        "translation": translation or "",
        "keypoints":   kp_lines[:4],
    }


def word_count(t: str) -> int:
    return len(t.split()) if t else 0


# ══════════════════════════════════════════════════════════════════════════════
#  UI LAYOUT
# ══════════════════════════════════════════════════════════════════════════════

# ── Header / Logo ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="qb-header">
  <div class="qb-logo-row">
    <div class="qb-logo-icon">⚡</div>
    <div>
      <div class="qb-logo-text">
        <span class="qb-logo-quick">Quick</span><span class="qb-logo-brief">Brief</span>
      </div>
      <div class="qb-logo-tagline">AI Text Summarizer &amp; Regional Translator</div>
    </div>
  </div>
  <div class="qb-badge">
    <span class="badge-dot"></span>
    Powered by Groq LLM API
  </div>
</div>
""", unsafe_allow_html=True)

# ── Stats bar ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="stats-row">
  <div class="stat-box">
    <div class="stat-num">15<span class="stat-unit">+</span></div>
    <div class="stat-lbl">Languages</div>
  </div>
  <div class="stat-box">
    <div class="stat-num">~3<span class="stat-unit">s</span></div>
    <div class="stat-lbl">Avg Response</div>
  </div>
  <div class="stat-box">
    <div class="stat-num">300<span class="stat-unit">t/s</span></div>
    <div class="stat-lbl">Groq Speed</div>
  </div>
  <div class="stat-box">
    <div class="stat-num">3<span class="stat-unit">×</span></div>
    <div class="stat-lbl">Output Sections</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── How it works ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="steps-row">
  <div class="step-box">
    <div class="step-num-label">STEP 01</div>
    <div class="step-emoji">📋</div>
    <div class="step-title">Paste Your Text</div>
    <div class="step-desc">Copy any article, news, or study material into the text box.</div>
  </div>
  <div class="step-box">
    <div class="step-num-label">STEP 02</div>
    <div class="step-emoji">🌐</div>
    <div class="step-title">Select Language</div>
    <div class="step-desc">Choose your regional or global target language.</div>
  </div>
  <div class="step-box">
    <div class="step-num-label">STEP 03</div>
    <div class="step-emoji">🤖</div>
    <div class="step-title">AI Processes</div>
    <div class="step-desc">Groq LLM summarizes and translates at blazing speed.</div>
  </div>
  <div class="step-box">
    <div class="step-num-label">STEP 04</div>
    <div class="step-emoji">✨</div>
    <div class="step-title">Get Results</div>
    <div class="step-desc">English summary + regional translation + 4 key points.</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── App heading ───────────────────────────────────────────────────────────────
st.markdown('<div class="qb-section-label">TRY IT NOW</div>', unsafe_allow_html=True)
st.markdown('<div class="qb-section-title">QuickBrief AI Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="qb-section-sub">Paste your text below and get an AI summary with regional translation instantly</div>', unsafe_allow_html=True)

# ── Sample loaders ────────────────────────────────────────────────────────────
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

c1, c2, c3, c4 = st.columns([1, 1, 1, 3])
with c1:
    if st.button("🔬 Science Sample"):
        st.session_state.input_text = SAMPLES["🔬 Science"];  st.rerun()
with c2:
    if st.button("📰 News Sample"):
        st.session_state.input_text = SAMPLES["📰 News"];     st.rerun()
with c3:
    if st.button("💻 Tech Sample"):
        st.session_state.input_text = SAMPLES["💻 Technology"]; st.rerun()
with c4:
    if st.button("🗑️ Clear"):
        st.session_state.input_text = ""; st.rerun()

# ── Main two-column layout ────────────────────────────────────────────────────
left_col, right_col = st.columns([1, 1], gap="large")

# ── LEFT: Input panel ─────────────────────────────────────────────────────────
with left_col:
    st.markdown(
        "<div style='color:#94a3b8;font-size:0.82rem;font-weight:600;margin-bottom:6px;'>📄 INPUT TEXT</div>",
        unsafe_allow_html=True,
    )
    user_input = st.text_area(
        label="Input",
        value=st.session_state.input_text,
        placeholder="Paste your article, news report, or any long text here…",
        height=240,
        max_chars=20000,
        label_visibility="collapsed",
        key="textarea_input",
    )

    char_count    = len(user_input)
    counter_color = "#ef4444" if char_count > 18000 else "#475569"
    st.markdown(
        f'<div style="text-align:right;font-size:0.74rem;color:{counter_color};margin-top:-6px;margin-bottom:12px;">'
        f'{char_count:,} / 20,000 characters</div>',
        unsafe_allow_html=True,
    )

    ctrl1, ctrl2 = st.columns(2)
    with ctrl1:
        target_lang = st.selectbox(
            "Target Language",
            options=list(LANG_FLAGS.keys()),
            format_func=lambda x: f"{LANG_FLAGS[x]} {x}",
            index=0,
        )
    with ctrl2:
        summary_len = st.selectbox(
            "Summary Length",
            options=["Short (2-3 sentences)", "Medium (1 paragraph)", "Detailed (3-4 paragraphs)"],
            index=1,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # API key status indicator
    if not GROQ_API_KEY:
        st.markdown('<div class="qb-info">🔑 Enter your Groq API key in the sidebar to get started.</div>', unsafe_allow_html=True)
    elif not key_valid:
        st.markdown(
            '<div class="qb-error">❌ <strong>Invalid key format.</strong> '
            'Groq keys start with <code>gsk_</code>. '
            '<a href="https://console.groq.com/keys" target="_blank" style="color:#a855f7;">Get one free →</a></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="qb-success">✅ API key ready &nbsp;·&nbsp; '
            f'Model: <strong>{model_choice}</strong></div>',
            unsafe_allow_html=True,
        )

    process_clicked = st.button(
        "⚡  Summarize & Translate",
        use_container_width=True,
        disabled=not key_valid,
    )

# ── RIGHT: Output panel ───────────────────────────────────────────────────────
with right_col:
    if not process_clicked and "result" not in st.session_state:
        st.markdown("""
        <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
          text-align:center;min-height:400px;
          background:rgba(255,255,255,0.03);
          border:1px dashed rgba(255,255,255,0.1);
          border-radius:20px;padding:48px 32px;">
          <div style="font-size:4rem;margin-bottom:16px;opacity:0.6;">🎯</div>
          <div style="font-family:'Outfit',sans-serif;font-size:1.05rem;font-weight:700;margin-bottom:8px;">
            Your Results Will Appear Here
          </div>
          <div style="font-size:0.85rem;color:#475569;max-width:280px;line-height:1.65;">
            Paste your text, choose a language, and click
            <strong style="color:#a855f7;">Summarize &amp; Translate</strong> to get started.
          </div>
        </div>
        """, unsafe_allow_html=True)

    elif process_clicked:
        if not user_input.strip():
            st.markdown('<div class="qb-error">⚠️ Please paste some text before processing.</div>', unsafe_allow_html=True)
        elif len(user_input.strip().split()) < 20:
            st.markdown('<div class="qb-error">⚠️ Text too short — provide at least 20 words for a meaningful summary.</div>', unsafe_allow_html=True)
        else:
            with st.spinner(f"🤖 Groq ({model_choice}) is processing…"):
                try:
                    t_start = time.time()
                    result  = summarize_and_translate(
                        user_input.strip(), target_lang, summary_len,
                        model_choice, GROQ_API_KEY,
                    )
                    result["elapsed"] = round(time.time() - t_start, 1)
                    st.session_state.result      = result
                    st.session_state.result_lang = target_lang
                except Exception as e:
                    err = str(e)
                    hint = ""
                    if "401" in err or "invalid_api_key" in err.lower() or "authentication" in err.lower():
                        hint = "<br>→ <strong>Invalid API key.</strong> Check your key at <a href='https://console.groq.com/keys' target='_blank' style='color:#a855f7;'>console.groq.com</a>"
                    elif "429" in err or "rate_limit" in err.lower():
                        hint = "<br>→ <strong>Rate limit hit.</strong> Wait a moment and try again."
                    elif "model" in err.lower() and "not found" in err.lower():
                        hint = "<br>→ <strong>Model not available.</strong> Try a different model in the sidebar."
                    st.markdown(
                        f'<div class="qb-error">❌ <strong>Groq API Error:</strong><br>{err}{hint}</div>',
                        unsafe_allow_html=True,
                    )
                    st.session_state.pop("result", None)

    # ── Show cached result ────────────────────────────────────────────────────
    if "result" in st.session_state:
        r    = st.session_state.result
        lang = st.session_state.get("result_lang", target_lang)
        flag = LANG_FLAGS.get(lang, "🌐")

        st.markdown(
            f'<div class="qb-success">✅ Done in <strong>{r.get("elapsed","–")}s</strong>'
            f' &nbsp;·&nbsp; Summary: <strong>{word_count(r["summary"])} words</strong>'
            f' &nbsp;·&nbsp; Language: <strong>{flag} {lang}</strong></div>',
            unsafe_allow_html=True,
        )

        # English summary
        st.markdown(f"""
        <div class="result-card">
          <div class="result-card-header">🇬🇧 English Summary</div>
          <div class="result-card-body">{r['summary']}</div>
          <div class="result-card-footer">📝 {word_count(r['summary'])} words</div>
        </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        # Translation
        st.markdown(f"""
        <div class="result-card">
          <div class="result-card-header">{flag} {lang} Translation</div>
          <div class="result-card-body" style="font-size:0.95rem;line-height:1.9;">{r['translation']}</div>
          <div class="result-card-footer">📝 {word_count(r['translation'])} words</div>
        </div>""", unsafe_allow_html=True)

        # Key points
        if r.get("keypoints"):
            kp_html = "".join(
                f'<div class="key-point"><span class="key-arrow">→</span><span>{kp}</span></div>'
                for kp in r["keypoints"]
            )
            st.markdown(f"""
            <div class="key-card">
              <div class="key-card-title">🎯 Key Points Extracted</div>
              {kp_html}
            </div>""", unsafe_allow_html=True)

        # Copy boxes
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        cc1, cc2 = st.columns(2)
        with cc1:
            st.markdown("<div style='font-size:0.75rem;color:#64748b;margin-bottom:4px;'>📋 Copy Summary</div>", unsafe_allow_html=True)
            st.code(r["summary"], language=None)
        with cc2:
            st.markdown("<div style='font-size:0.75rem;color:#64748b;margin-bottom:4px;'>📋 Copy Translation</div>", unsafe_allow_html=True)
            st.code(r["translation"], language=None)

# ── Supported languages ───────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown('<div class="qb-section-label">SUPPORTED LANGUAGES</div>', unsafe_allow_html=True)
pills = "".join(f'<span class="lang-pill">{f} {l}</span>' for l, f in LANG_FLAGS.items())
st.markdown(f'<div class="lang-pills">{pills}</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="qb-footer">
  <div style="font-size:1.5rem;margin-bottom:8px;">⚡ <span>Quick</span>Brief</div>
  Making information accessible to everyone through Generative AI.<br>
  Powered by <span>Groq LLM API</span> &nbsp;·&nbsp; Built with ❤️ using Python &amp; Streamlit<br>
  <span style="font-size:0.72rem;opacity:0.5;">© 2026 QuickBrief. All rights reserved.</span>
</div>
""", unsafe_allow_html=True)
