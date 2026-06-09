from __future__ import annotations
import streamlit as st


# ─────────────────────────────────────────────────────────────────────────────
# Design system: Japanese editorial print.
# Warm washi paper, sumi ink, indigo (ai) as the structural colour, a single
# vermilion seal (shu) accent, gold (kin) used sparingly. Shippori Mincho display
# serif over Zen Kaku Gothic body. Hairline rules, vertical rhythm, zero rounding.
# The "Divergence" story is colour-coded: indigo = Tokyo / growth, vermilion = decline.
# ─────────────────────────────────────────────────────────────────────────────

WASHI   = "#F2EFE7"   # warm off-white paper ground
PANEL   = "#EBE6DA"   # deeper panel ground
SUMI    = "#1F1B16"   # warm near-black ink
INK60   = "#6E6557"   # muted ink
LINE    = "#DED7C8"   # hairline
AI      = "#2A4061"   # indigo · structural / primary / growth / Tokyo
AI_LT   = "#5C7397"   # lighter indigo
SHU     = "#C0492B"   # vermilion seal · accent / decline
KIN     = "#B08A36"   # gold · sparing secondary
POS     = AI          # growth reads indigo
NEG     = SHU         # decline reads vermilion

# Plotly diverging / sequential scales on the brand
PRICE_SCALE = [[0.0, "#E7E0D0"], [0.5, "#9FB0C6"], [1.0, AI]]      # low→high price
AKIYA_SCALE = [[0.0, "#E7E0D0"], [0.5, "#D29A7E"], [1.0, "#7A2E1C"]]  # vacancy (bad)
DIVERGE_SCALE = [[0.0, SHU], [0.5, "#CFC8BA"], [1.0, AI]]          # neg→0→pos
SERIES = [AI, SHU, KIN, AI_LT, "#7A8B6F", "#8C7A52"]


# ── Theme detection ────────────────────────────────────────────────────────────

def get_theme() -> str:
    try:
        return st.get_option("theme.base") or "light"
    except Exception:
        return "light"


def is_dark() -> bool:
    return get_theme() == "dark"


# ── Plotly helpers ─────────────────────────────────────────────────────────────

def plotly_base(height: int = 420, margin: dict | None = None) -> tuple[dict, str, str]:
    """Return (layout_dict, grid_color, zero_color) for a Plotly chart on washi.
    Pass margin= to override the default; avoids duplicate-keyword errors when spreading **base.
    """
    grid = LINE
    zero = "#CDC4B2"
    m = margin if margin is not None else dict(l=8, r=8, t=24, b=8)
    return (
        dict(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=height,
            font=dict(color=SUMI, family="'Zen Kaku Gothic New', sans-serif", size=12),
            colorway=SERIES,
            margin=m,
            dragmode=False,
        ),
        grid,
        zero,
    )


def year_ticks(periods: list[str]) -> tuple[list[str], list[str]]:
    """From a list of 'YYYY-Qn' strings, return tickvals/ticktext showing only years."""
    vals, texts = [], []
    seen: set[str] = set()
    for p in sorted(set(periods)):
        yr = p.split("-")[0]
        if yr not in seen:
            seen.add(yr)
            vals.append(p)
            texts.append(yr)
    return vals, texts


# ── CSS injection ──────────────────────────────────────────────────────────────

def inject_css() -> None:
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@500;600;700;800&family=Zen+Kaku+Gothic+New:wght@400;500;700;900&display=swap');

html, body, [class*="css"] {{ font-family:'Zen Kaku Gothic New', sans-serif !important; }}
[data-testid="stAppViewContainer"] {{ background:{WASHI} !important; }}
[data-testid="stHeader"] {{ display:none !important; }}
.main .block-container {{ padding-top:0 !important; padding-bottom:0 !important; max-width:1320px; }}
section[data-testid="stMain"] {{ padding-bottom:0 !important; }}
footer {{ display:none !important; }}
section[data-testid="stMain"] > div:first-child {{ padding-top:0 !important; }}
[data-testid="stSidebarNav"] {{ display:none !important; }}
[data-testid="collapsedControl"], [data-testid="stSidebar"],
section[data-testid="stSidebar"], button[kind="header"] {{ display:none !important; }}

.stApp *, [data-testid] * {{ border-radius:0 !important; }}

:root {{
    --accent:        {AI};
    --accent-dark:   #1B2C44;
    --accent-faint:  rgba(42,64,97,0.08);
    --seal:          {SHU};
    --pos:           {AI};
    --neg:           {SHU};
    --surface:       {WASHI};
    --surface-2:     {PANEL};
    --surface-3:     rgba(42,64,97,.06);
    --border:        {SUMI};
    --line:          {LINE};
    --text-h:        {SUMI};
    --text-body:     #3A352C;
    --text-muted:    {INK60};
    --text-faint:    #908775;
}}

/* ── Page header ── */
.page-header {{ padding:2rem 0 1.4rem; border-bottom:2px solid {SUMI}; margin-bottom:2rem; }}
.page-header-eyebrow {{
    font-family:'Zen Kaku Gothic New',sans-serif;
    font-size:0.70rem; font-weight:700; text-transform:uppercase; letter-spacing:0.16em;
    color:{SHU}; margin-bottom:0.6rem; }}
.page-header-title {{
    font-family:'Shippori Mincho',serif; font-size:2.6rem; font-weight:700; color:{SUMI};
    letter-spacing:-0.01em; line-height:1.1; margin-bottom:0.7rem; }}
.page-header-desc {{
    font-size:1.0rem; color:{INK60}; max-width:680px; line-height:1.75; }}

/* ── Section header ── */
.section-title {{
    font-family:'Shippori Mincho',serif; font-size:1.35rem; font-weight:700; color:{SUMI};
    margin:2rem 0 0.4rem; display:flex; align-items:center; gap:0.55rem; }}
.section-title::before {{
    content:''; display:inline-block; width:4px; height:1.0em; background:{SHU}; flex-shrink:0; }}
.section-sub {{ font-size:0.9rem; color:{INK60}; margin-bottom:1rem; line-height:1.65; }}

/* ── Callout ── */
.callout {{
    background:{PANEL}; border-left:3px solid {AI}; padding:0.85rem 1.1rem;
    margin:0.8rem 0 1.2rem; font-size:0.92rem; color:#3A352C; line-height:1.7; }}
.callout strong {{ color:{AI}; }}
.callout-pos {{ border-left-color:{AI}; }}
.callout-pos strong {{ color:{AI}; }}
.callout-neg {{ border-left-color:{SHU}; }}
.callout-neg strong {{ color:{SHU}; }}

/* ── KPI cards ── */
.kpi-row {{ display:flex; gap:0; margin:1rem 0 1.5rem; flex-wrap:wrap; border:1px solid {SUMI};
    border-right:none; }}
.kpi {{ background:{WASHI}; border-right:1px solid {SUMI}; padding:0.95rem 1.15rem; flex:1; min-width:130px; }}
.kpi-label {{ font-size:0.66rem; font-weight:700; text-transform:uppercase; letter-spacing:0.10em;
    color:{INK60}; margin-bottom:0.4rem; }}
.kpi-value {{ font-family:'Shippori Mincho',serif; font-size:1.7rem; font-weight:700; color:{SUMI};
    line-height:1.1; font-variant-numeric:tabular-nums; }}
.kpi-value-accent {{ color:{SHU}; }}
.kpi-sub {{ font-size:0.74rem; color:#908775; margin-top:0.25rem; }}

/* ── Streamlit metric overrides ── */
.stMetric {{ background:{WASHI}; border:1px solid {SUMI}; padding:0.85rem 1rem !important; }}
.stMetric label {{ font-size:0.68rem !important; font-weight:700 !important; text-transform:uppercase !important;
    letter-spacing:0.08em !important; color:{INK60} !important; }}
.stMetric [data-testid="stMetricValue"] {{ font-family:'Shippori Mincho',serif;
    font-size:1.5rem !important; font-weight:700 !important; color:{SUMI} !important;
    font-variant-numeric:tabular-nums; }}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {{ gap:0; border-bottom:1px solid {SUMI}; background:transparent !important; }}
.stTabs [data-baseweb="tab"] {{ font-family:'Zen Kaku Gothic New',sans-serif; font-size:0.84rem; font-weight:700;
    padding:0.55rem 1.15rem; color:{INK60}; border-bottom:3px solid transparent; margin-bottom:-1px;
    text-transform:uppercase; letter-spacing:0.04em; }}
.stTabs [aria-selected="true"] {{ color:{SUMI} !important; border-bottom-color:{SHU} !important; }}

/* ── Native widgets ── */
.stRadio > label, .stMultiSelect label, .stSelectbox label {{
    color:{INK60} !important; font-size:11px !important; font-weight:700 !important;
    text-transform:uppercase !important; letter-spacing:.08em !important; }}
.stRadio [data-testid="stMarkdownContainer"] p {{ color:#3A352C !important; }}
hr {{ border-color:{LINE} !important; }}
p {{ color:#3A352C; }}
h1, h2, h3 {{ color:{SUMI} !important; font-family:'Shippori Mincho',serif; }}
[data-baseweb="select"] > div {{ background:{WASHI} !important; border-color:{SUMI} !important; color:{SUMI} !important; }}
input, textarea {{ background:{WASHI} !important; border-color:{SUMI} !important; color:{SUMI} !important; }}
.stSlider [data-baseweb="slider"] div[role="slider"] {{ background:{SHU} !important; }}

/* ── Info badge / method box ── */
.info-badge {{ background:var(--surface-3); border:1px solid {SUMI}; padding:0.6rem 0.8rem;
    font-size:0.78rem; color:{INK60}; line-height:1.6; }}
.info-badge strong {{ color:#3A352C; }}
.method-box {{ background:{PANEL}; border:1px solid {SUMI}; padding:1rem 1.2rem; font-size:0.85rem;
    color:{INK60}; line-height:1.7; margin-top:0.5rem; }}
.method-box h4 {{ color:#3A352C; font-size:0.84rem; font-weight:700; margin:0.8rem 0 0.3rem;
    font-family:'Zen Kaku Gothic New',sans-serif; }}
.method-box h4:first-child {{ margin-top:0; }}

/* ── Chart & data containers ── */
[data-testid="stPlotlyChart"] {{ border:1px solid {SUMI}; background:{WASHI}; padding:6px; overflow:hidden; }}
[data-testid="stDataFrame"] {{ border:1px solid {SUMI}; overflow:hidden; }}

/* ── Footer ── */
.app-footer {{ margin-top:0.5rem; padding:1rem 0; border-top:1px solid {SUMI};
    font-size:0.76rem; color:#908775; text-align:center; line-height:1.8; }}
.app-footer a {{ color:{AI}; text-decoration:none; }}
.app-footer a:hover {{ text-decoration:underline; }}
</style>
""", unsafe_allow_html=True)


# ── Python component helpers ───────────────────────────────────────────────────

def page_header(eyebrow: str, title: str, desc: str, badges: list[str] | None = None) -> None:
    badge_html = ""
    if badges:
        for b in badges:
            badge_html += (f'<span style="display:inline-block;background:var(--accent-faint);'
                           f'color:{AI};border:1px solid {AI};padding:0.15rem 0.65rem;font-size:0.68rem;'
                           f'font-weight:700;text-transform:uppercase;letter-spacing:0.06em;'
                           f'margin-right:0.4rem;">{b}</span>')
    st.markdown(f"""
<div class="page-header">
    <div class="page-header-eyebrow">{eyebrow}</div>
    <div class="page-header-title">{title}</div>
    <div class="page-header-desc">{desc}</div>
    {'<div style="margin-top:0.8rem;">' + badge_html + '</div>' if badge_html else ''}
</div>
""", unsafe_allow_html=True)


def section_title(text: str, sub: str = "") -> None:
    sub_html = f'<div class="section-sub">{sub}</div>' if sub else ""
    st.markdown(f'<div class="section-title">{text}</div>{sub_html}', unsafe_allow_html=True)


def callout(text: str, variant: str = "") -> None:
    cls = f"callout callout-{variant}" if variant else "callout"
    st.markdown(f'<div class="{cls}">{text}</div>', unsafe_allow_html=True)


def kpi_card(label: str, value: str, sub: str = "", accent: bool = False) -> None:
    val_cls = "kpi-value kpi-value-accent" if accent else "kpi-value"
    sub_html = f'<div class="kpi-sub">{sub}</div>' if sub else ""
    st.markdown(
        f'<div class="kpi"><div class="kpi-label">{label}</div>'
        f'<div class="{val_cls}">{value}</div>{sub_html}</div>',
        unsafe_allow_html=True,
    )


def nav_top(current: str = "") -> None:
    """Top navigation bar. Pass current='overview'|'tokyo'|'about' to highlight active tab."""
    def _link(label: str, href: str, key: str) -> str:
        active = ' nav-active' if key == current else ''
        return f'<a href="{href}" target="_self" class="nav-lnk{active}">{label}</a>'

    st.markdown(f"""
<style>
.app-nav {{
    display:flex; align-items:center; gap:8px; padding:0 28px; height:64px;
    background:{WASHI}; border-bottom:2px solid {SUMI};
    position:sticky; top:0; z-index:9999; margin-bottom:0; }}
.app-nav .nav-logo {{
    font-family:'Shippori Mincho',serif; font-size:16px; font-weight:800; letter-spacing:.06em;
    color:{SUMI}; text-decoration:none; margin-right:22px; white-space:nowrap; }}
.app-nav .nav-logo .seal {{ color:{SHU}; }}
.app-nav .nav-lnk {{
    font-family:'Zen Kaku Gothic New',sans-serif; font-size:11px; font-weight:700;
    text-transform:uppercase; letter-spacing:.11em; color:{INK60}; text-decoration:none;
    white-space:nowrap; padding:6px 14px; border:1px solid {SUMI}; background:{WASHI};
    transition:color .15s, background .15s; }}
.app-nav .nav-lnk:hover {{ color:{WASHI}; background:{AI}; }}
.app-nav .nav-lnk.nav-active {{ color:{WASHI}; background:{SUMI}; border-color:{SUMI}; }}
div[data-testid="stVerticalBlock"] {{ gap:0 !important; }}
div[data-testid="stMarkdownContainer"]:has(.app-nav) {{ margin-bottom:0 !important; }}
</style>
<div class="app-nav">
  <a class="nav-logo" href="/" target="_self">Japan<span class="seal"> 不動産</span></a>
  {_link("The Divergence", "/Japan_Overview", "overview")}
  {_link("Tokyo Deep Dive", "/Tokyo_Deep_Dive", "tokyo")}
  {_link("About", "/About", "about")}
</div>
""", unsafe_allow_html=True)


def footer(page_name: str, source: str = "MLIT Real Estate Information Library") -> None:
    st.markdown(f"""
<div class="app-footer">
    <strong>Japan Real Estate Intelligence</strong> · {page_name} ·
    Built by <a href="https://santimuru.github.io" target="_blank">Santiago Martinez</a> ·
    <a href="https://github.com/santimuru/japan-real-estate" target="_blank">GitHub</a><br/>
    Data: {source}
</div>
""", unsafe_allow_html=True)
