from __future__ import annotations
import streamlit as st


# ─────────────────────────────────────────────────────────────────────────────
# Design system: Minimal Swiss.
# White ground, generous whitespace, light Inter, ink + a single red accent,
# hairline rules and thin line-art charts. No cards, no shadows, no chrome.
# The "Divergence" story reads ink (growth / Tokyo) vs red (decline / vacancy).
# ─────────────────────────────────────────────────────────────────────────────

WASHI   = "#FFFFFF"   # white ground
PANEL   = "#F6F6F4"   # faint panel
SUMI    = "#111111"   # ink
INK60   = "#6B6B68"   # muted grey (readable on white)
LINE    = "#E7E7E4"   # hairline
AI      = "#111111"   # ink · primary data / growth / Tokyo
AI_LT   = "#777777"   # grey
SHU     = "#D8412F"   # the single red accent · decline / emphasis
KIN     = "#999999"   # grey (gold dropped in this system)
POS     = SUMI        # growth reads ink
NEG     = SHU         # decline reads red

PRICE_SCALE = [[0.0, "#F2F2F0"], [0.5, "#9A9A98"], [1.0, SUMI]]      # low→high price (ink)
AKIYA_SCALE = [[0.0, "#F5ECEA"], [0.5, "#E0A091"], [1.0, "#9E2C1C"]]  # vacancy (red)
DIVERGE_SCALE = [[0.0, SHU], [0.5, "#DCDCD9"], [1.0, SUMI]]          # neg→0→pos
SERIES = [SUMI, SHU, "#9A9A98", "#5A5A58", "#C7857A", "#3A3A38"]


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
    """Return (layout_dict, grid_color, zero_color) for a thin-line chart on white."""
    grid = LINE
    zero = "#D8D8D4"
    m = margin if margin is not None else dict(l=8, r=8, t=24, b=8)
    return (
        dict(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=height,
            font=dict(color=SUMI, family="Inter, sans-serif", size=12),
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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {{ font-family:'Inter', system-ui, sans-serif !important; }}
[data-testid="stAppViewContainer"] {{ background:{WASHI} !important; }}
[data-testid="stHeader"] {{ display:none !important; }}
.main .block-container {{ padding-top:0 !important; padding-bottom:0 !important; max-width:1180px; }}
section[data-testid="stMain"] {{ padding-bottom:0 !important; }}
footer {{ display:none !important; }}
section[data-testid="stMain"] > div:first-child {{ padding-top:0 !important; }}
[data-testid="stSidebarNav"] {{ display:none !important; }}
[data-testid="collapsedControl"], [data-testid="stSidebar"],
section[data-testid="stSidebar"], button[kind="header"] {{ display:none !important; }}

:root {{
    --accent:{SHU}; --accent-dark:#B83422; --accent-faint:rgba(216,65,47,.06);
    --seal:{SHU}; --pos:{SUMI}; --neg:{SHU};
    --surface:{WASHI}; --surface-2:{PANEL}; --surface-3:{PANEL};
    --border:{LINE}; --line:{LINE};
    --text-h:{SUMI}; --text-body:#3A3A38; --text-muted:{INK60}; --text-faint:#B4B4B0;
}}

/* ── Page header ── */
.page-header {{ padding:3.2rem 0 1.8rem; margin-bottom:2.4rem; }}
.page-header-eyebrow {{ font-size:0.68rem; font-weight:600; text-transform:uppercase;
    letter-spacing:0.22em; color:{INK60}; margin-bottom:1.4rem; }}
.page-header-title {{ font-weight:300; font-size:clamp(2.6rem,5.4vw,4.2rem); color:{SUMI};
    letter-spacing:-0.03em; line-height:1.04; margin-bottom:1.2rem; }}
.page-header-title b, .page-header-title strong {{ font-weight:600; }}
.page-header-desc {{ font-weight:300; font-size:1.18rem; color:#3A3A38; max-width:620px; line-height:1.7; }}

/* ── Section header ── */
.section-title {{ font-weight:300; font-size:1.7rem; color:{SUMI}; letter-spacing:-0.02em;
    margin:3rem 0 0.3rem; }}
.section-sub {{ font-size:0.72rem; color:{INK60}; margin-bottom:1.8rem; line-height:1.6;
    text-transform:uppercase; letter-spacing:0.16em; }}

/* ── Callout ── */
.callout {{ border-left:2px solid {SUMI}; padding:0.4rem 0 0.4rem 1.1rem; margin:1.2rem 0 1.6rem;
    font-size:0.96rem; color:#3A3A38; line-height:1.7; font-weight:300; }}
.callout strong {{ color:{SUMI}; font-weight:600; }}
.callout-pos {{ border-left-color:{SUMI}; }}
.callout-pos strong {{ color:{SUMI}; }}
.callout-neg {{ border-left-color:{SHU}; }}
.callout-neg strong {{ color:{SHU}; }}

/* ── KPI · numbers in air, no cards ── */
.kpi-row {{ display:flex; gap:3.5rem; margin:1.6rem 0 2.4rem; flex-wrap:wrap; }}
.kpi {{ padding:0; }}
.kpi-label {{ font-size:0.66rem; font-weight:600; text-transform:uppercase; letter-spacing:0.14em;
    color:{INK60}; margin-bottom:0.7rem; order:2; }}
.kpi-value {{ font-weight:300; font-size:clamp(1.6rem,6.5vw,2.7rem); color:{SUMI}; line-height:1; letter-spacing:-0.02em;
    font-variant-numeric:tabular-nums; }}
.kpi-value-accent {{ color:{SHU}; }}
.kpi-sub {{ font-size:0.74rem; color:{INK60}; margin-top:0.5rem; font-weight:400; }}

/* ── Streamlit metric ── */
.stMetric {{ background:transparent; border:none; padding:0 !important; }}
.stMetric label {{ font-size:0.66rem !important; font-weight:600 !important; text-transform:uppercase !important;
    letter-spacing:0.14em !important; color:{INK60} !important; }}
.stMetric [data-testid="stMetricValue"] {{ font-weight:300 !important; font-size:2.2rem !important;
    color:{SUMI} !important; font-variant-numeric:tabular-nums; }}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {{ gap:2rem; border-bottom:1px solid {LINE}; background:transparent !important; }}
.stTabs [data-baseweb="tab"] {{ font-size:0.72rem; font-weight:600; padding:0.6rem 0; color:{INK60};
    text-transform:uppercase; letter-spacing:0.12em; border-bottom:1px solid transparent; margin-bottom:-1px; }}
.stTabs [aria-selected="true"] {{ color:{SUMI} !important; border-bottom-color:{SHU} !important; }}

/* ── Native widgets ── */
.stRadio > label, .stMultiSelect label, .stSelectbox label {{
    color:{INK60} !important; font-size:11px !important; font-weight:600 !important;
    text-transform:uppercase !important; letter-spacing:.12em !important; }}
.stRadio [data-testid="stMarkdownContainer"] p {{ color:#3A3A38 !important; }}
hr {{ border-color:{LINE} !important; }}
p {{ color:#3A3A38; }}
h1, h2, h3 {{ color:{SUMI} !important; font-family:'Inter',sans-serif; font-weight:300; }}
[data-baseweb="select"] > div {{ background:{WASHI} !important; border-color:{LINE} !important; color:{SUMI} !important; }}
input, textarea {{ background:{WASHI} !important; border-color:{LINE} !important; color:{SUMI} !important; }}
.stSlider [data-baseweb="slider"] div[role="slider"] {{ background:{SHU} !important; }}

/* ── Info badge / method box ── */
.info-badge {{ background:transparent; border:none; border-left:2px solid {LINE}; padding:0.2rem 0 0.2rem 0.9rem;
    font-size:0.8rem; color:{INK60}; line-height:1.6; }}
.info-badge strong {{ color:#3A3A38; }}
.method-box {{ background:transparent; border:none; border-top:1px solid {LINE}; padding:1.2rem 0 0; font-size:0.88rem;
    color:{INK60}; line-height:1.75; margin-top:0.5rem; font-weight:300; }}
.method-box h4 {{ color:{SUMI}; font-size:0.82rem; font-weight:600; margin:1rem 0 0.3rem;
    font-family:'Inter',sans-serif; }}
.method-box h4:first-child {{ margin-top:0; }}

/* ── Chart & data containers · no frames ── */
[data-testid="stPlotlyChart"] {{ border:none; background:transparent; padding:0; }}
[data-testid="stDataFrame"] {{ border:1px solid {LINE}; overflow:hidden; }}

/* ── Footer ── */
.app-footer {{ margin-top:3rem; padding:1.4rem 0; border-top:1px solid {LINE};
    font-size:0.74rem; color:#B4B4B0; text-align:center; line-height:1.8; }}
.app-footer a {{ color:{SUMI}; text-decoration:none; border-bottom:1px solid {SHU}; }}
.app-footer a:hover {{ color:{SHU}; }}

/* ===== Mobile responsive ===== */
@media (max-width: 640px){{
  [data-testid="stHorizontalBlock"]{{ flex-direction:column !important; gap:.75rem !important; }}
  [data-testid="stHorizontalBlock"] > [data-testid="column"],
  [data-testid="stColumn"]{{ width:100% !important; flex:1 1 100% !important; min-width:0 !important; }}
  .kpi-row{{ flex-direction:column !important; gap:1rem !important; }}
  .block-container, .main .block-container{{ padding-left:1rem !important; padding-right:1rem !important; }}
  /* tab strip scrollable en vez de romper */
  .stTabs [data-baseweb="tab-list"]{{ overflow-x:auto !important; flex-wrap:nowrap !important; gap:1.2rem !important; }}
  .stTabs [data-baseweb="tab"]{{ flex:0 0 auto !important; white-space:nowrap !important; }}
  .page-header{{ padding:1.8rem 0 1.2rem !important; margin-bottom:1.6rem !important; }}
  /* hero split (raw-HTML, not a Streamlit column) stacks vertically */
  .hero-split{{ flex-direction:column !important; align-items:stretch !important; gap:1.6rem !important; }}
  .hero-split .hero-text{{ max-width:100% !important; }}
  .hero-split .hero-kpis{{ grid-template-columns:1fr 1fr !important; gap:1.2rem 1.4rem !important; }}
}}
</style>
""", unsafe_allow_html=True)


# ── Python component helpers ───────────────────────────────────────────────────

def page_header(eyebrow: str, title: str, desc: str, badges: list[str] | None = None) -> None:
    badge_html = ""
    if badges:
        for b in badges:
            badge_html += (f'<span style="display:inline-block;color:{INK60};border:1px solid {LINE};'
                           f'padding:0.15rem 0.65rem;font-size:0.66rem;font-weight:600;'
                           f'text-transform:uppercase;letter-spacing:0.10em;margin-right:0.4rem;">{b}</span>')
    st.markdown(f"""
<div class="page-header">
    <div class="page-header-eyebrow">{eyebrow}</div>
    <div class="page-header-title">{title}</div>
    <div class="page-header-desc">{desc}</div>
    {'<div style="margin-top:1.2rem;">' + badge_html + '</div>' if badge_html else ''}
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
    """Minimal text nav. Pass current='overview'|'tokyo'|'about' to highlight active."""
    def _link(label: str, href: str, key: str) -> str:
        active = ' nav-active' if key == current else ''
        return f'<a href="{href}" target="_self" class="nav-lnk{active}">{label}</a>'

    st.markdown(f"""
<style>
.app-nav {{ display:flex; align-items:center; gap:2.2rem; padding:1.4rem 0; height:auto;
    background:{WASHI}; border-bottom:1px solid {LINE};
    position:sticky; top:0; z-index:9999; margin-bottom:0; }}
.app-nav .nav-logo {{ font-weight:600; font-size:15px; letter-spacing:-0.01em;
    color:{SUMI}; text-decoration:none; margin-right:auto; }}
.app-nav .nav-logo .seal {{ color:{SHU}; }}
.app-nav .nav-lnk {{ font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:.14em;
    color:{INK60}; text-decoration:none; white-space:nowrap; padding:0.2rem 0;
    border-bottom:1px solid transparent; transition:color .15s; }}
.app-nav .nav-lnk:hover {{ color:{SUMI}; }}
.app-nav .nav-lnk.nav-active {{ color:{SUMI}; border-bottom-color:{SHU}; }}
div[data-testid="stVerticalBlock"] {{ gap:0 !important; }}
div[data-testid="stMarkdownContainer"]:has(.app-nav) {{ margin-bottom:0 !important; }}
@media (max-width: 640px) {{
  .app-nav {{ overflow-x:auto !important; flex-wrap:nowrap !important; gap:1.1rem !important;
      padding:0.9rem 0 !important; -webkit-overflow-scrolling:touch; }}
  .app-nav .nav-logo {{ font-size:13px !important; white-space:nowrap !important; margin-right:1.4rem !important; }}
  .app-nav .nav-lnk {{ flex:0 0 auto; }}
}}
</style>
<div class="app-nav">
  <a class="nav-logo" href="/" target="_self">Japan Real Estate<span class="seal"> · 不動産</span></a>
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
