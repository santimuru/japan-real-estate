from __future__ import annotations
import streamlit as st


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
    """Return (layout_dict, grid_color, zero_color) for a transparent Plotly chart.
    Pass margin= to override the default; avoids duplicate-keyword errors when spreading **base.
    """
    dark = is_dark()
    font_color = "#F1F5F9" if dark else "#0F172A"
    grid  = "#2D3748" if dark else "#E2E8F0"
    zero  = "#4A5568" if dark else "#CBD5E0"
    m = margin if margin is not None else dict(l=8, r=8, t=24, b=8)
    return (
        dict(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=height,
            font=dict(color=font_color, family="Inter, sans-serif", size=12),
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
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}
/* Match page background to hero canvas so any leftover space is invisible */
[data-testid="stAppViewContainer"] {
    background: #080808 !important;
}
/* Streamlit header — hidden entirely, replaced by our sticky nav */
[data-testid="stHeader"] {
    display: none !important;
}
.main .block-container {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    max-width: 1440px;
}
/* Kill the extra bottom space Streamlit appends after all content */
section[data-testid="stMain"] {
    padding-bottom: 0 !important;
}
footer { display: none !important; }
/* Remove the auto gap Streamlit inserts for the fixed header */
section[data-testid="stMain"] > div:first-child {
    padding-top: 0 !important;
}
/* Hide Streamlit's auto-generated sidebar nav (shows raw filenames) */
[data-testid="stSidebarNav"] { display: none !important; }
/* Hide sidebar and toggle completely */
[data-testid="collapsedControl"],
[data-testid="stSidebar"],
section[data-testid="stSidebar"],
button[kind="header"],
.st-emotion-cache-czk5ss { display: none !important; }

/* ── Design tokens — dark ── */
:root,
[data-theme="dark"] {
    --accent:        #3B82F6;
    --accent-dark:   #1D4ED8;
    --accent-faint:  rgba(59,130,246,0.10);
    --pos:           #10B981;
    --neg:           #EF4444;
    --surface:       rgba(255,255,255,.04);
    --surface-2:     rgba(255,255,255,.02);
    --surface-3:     rgba(59,130,246,.08);
    --border:        rgba(59,130,246,.20);
    --text-h:        #ffffff;
    --text-body:     rgba(180,215,255,.78);
    --text-muted:    rgba(140,185,235,.52);
    --text-faint:    rgba(100,150,210,.38);
    --shadow:        0 1px 8px rgba(0,0,0,.55);
    --shadow-md:     0 4px 20px rgba(0,0,0,.65);
}

/* ── Page header ── */
.page-header {
    padding: 2rem 0 1.5rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2rem;
}
.page-header-eyebrow {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.10em;
    color: var(--accent);
    margin-bottom: 0.4rem;
}
.page-header-title {
    font-size: 2.2rem;
    font-weight: 800;
    color: var(--text-h);
    letter-spacing: -0.02em;
    line-height: 1.15;
    margin-bottom: 0.6rem;
}
.page-header-desc {
    font-size: 1rem;
    color: var(--text-muted);
    max-width: 680px;
    line-height: 1.7;
}

/* ── Section header ── */
.section-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text-h);
    margin: 1.8rem 0 0.4rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-title::before {
    content: '';
    display: inline-block;
    width: 3px;
    height: 1.1em;
    background: var(--accent);
    border-radius: 2px;
    flex-shrink: 0;
}
.section-sub {
    font-size: 0.85rem;
    color: var(--text-muted);
    margin-bottom: 1rem;
    line-height: 1.6;
}

/* ── Insight / callout box ── */
.callout {
    background: var(--accent-faint);
    border-left: 3px solid var(--accent);
    border-radius: 0 8px 8px 0;
    padding: 0.85rem 1.1rem;
    margin: 0.8rem 0 1.2rem;
    font-size: 0.875rem;
    color: var(--text-body);
    line-height: 1.65;
}
.callout strong { color: var(--accent); }
.callout-pos { border-left-color: var(--pos); background: rgba(16,185,129,.08); }
.callout-pos strong { color: var(--pos); }
.callout-neg { border-left-color: var(--neg); background: rgba(239,68,68,.08); }
.callout-neg strong { color: var(--neg); }

/* ── KPI cards ── */
.kpi-row { display: flex; gap: 0.75rem; margin: 1rem 0 1.5rem; flex-wrap: wrap; }
.kpi {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    flex: 1;
    min-width: 130px;
    box-shadow: var(--shadow);
}
.kpi-label {
    font-size: 0.70rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-muted);
    margin-bottom: 0.3rem;
}
.kpi-value {
    font-size: 1.55rem;
    font-weight: 700;
    color: var(--text-h);
    line-height: 1.15;
}
.kpi-value-accent { color: var(--accent); }
.kpi-sub {
    font-size: 0.75rem;
    color: var(--text-faint);
    margin-top: 0.2rem;
}

/* ── Streamlit metric overrides ── */
.stMetric {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.85rem 1rem !important;
    box-shadow: var(--shadow);
}
.stMetric label {
    font-size: 0.70rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    color: var(--text-muted) !important;
}
.stMetric [data-testid="stMetricValue"] {
    font-size: 1.4rem !important;
    font-weight: 700 !important;
    color: var(--text-h) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    border-bottom: 2px solid var(--border);
    background: transparent !important;
}
.stTabs [data-baseweb="tab"] {
    font-size: 0.88rem;
    font-weight: 600;
    padding: 0.6rem 1.2rem;
    color: var(--text-muted);
    border-bottom: 2px solid transparent;
    margin-bottom: -2px;
}
.stTabs [aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom-color: var(--accent) !important;
}

/* ── Streamlit native widgets — dark overrides ── */
/* Radio */
.stRadio > label { color: rgba(140,185,235,.52) !important; font-size: 11px !important; font-weight: 600 !important; text-transform: uppercase !important; letter-spacing: .08em !important; }
.stRadio [data-testid="stMarkdownContainer"] p { color: rgba(180,215,255,.78) !important; }
/* Multiselect / Select */
.stMultiSelect label, .stSelectbox label { color: rgba(140,185,235,.52) !important; font-size: 11px !important; font-weight: 600 !important; text-transform: uppercase !important; letter-spacing: .08em !important; }
/* Dataframes */
.stDataFrame { border: 1px solid rgba(59,130,246,.18) !important; border-radius: 8px !important; overflow: hidden; }
/* Dividers */
hr { border-color: rgba(59,130,246,.18) !important; }
/* Streamlit generic text */
p { color: rgba(180,215,255,.78); }
h1, h2, h3 { color: #fff !important; }
/* Selectbox dropdown */
[data-baseweb="select"] { background: rgba(255,255,255,.04) !important; border-color: rgba(59,130,246,.25) !important; }

/* ── Info badge (sidebar) ── */
.info-badge {
    background: var(--surface-3);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.6rem 0.8rem;
    font-size: 0.75rem;
    color: var(--text-muted);
    line-height: 1.55;
}
.info-badge strong { color: var(--text-body); }

/* ── Methodology box ── */
.method-box {
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    font-size: 0.82rem;
    color: var(--text-muted);
    line-height: 1.7;
    margin-top: 0.5rem;
}
.method-box h4 {
    color: var(--text-body);
    font-size: 0.82rem;
    font-weight: 700;
    margin: 0.8rem 0 0.3rem;
}
.method-box h4:first-child { margin-top: 0; }

/* ── Chart & data container borders ── */
[data-testid="stPlotlyChart"] {
    border: 1px solid var(--border);
    border-radius: 12px;
    background: var(--surface);
    padding: 4px;
    overflow: hidden;
}
[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow: hidden;
}

/* ── Footer ── */
.app-footer {
    margin-top: 0.5rem;
    padding-top: 0.75rem;
    padding-bottom: 0.75rem;
    border-top: 1px solid var(--border);
    font-size: 0.75rem;
    color: var(--text-faint);
    text-align: center;
    line-height: 1.8;
}
.app-footer a { color: var(--accent); text-decoration: none; }
.app-footer a:hover { text-decoration: underline; }
</style>
""", unsafe_allow_html=True)


# ── Python component helpers ───────────────────────────────────────────────────

def page_header(eyebrow: str, title: str, desc: str, badges: list[str] | None = None) -> None:
    badge_html = ""
    if badges:
        for b in badges:
            badge_html += f'<span style="display:inline-block;background:var(--accent-faint);color:var(--accent);border:1px solid var(--accent);border-radius:20px;padding:0.15rem 0.65rem;font-size:0.70rem;font-weight:600;text-transform:uppercase;letter-spacing:0.06em;margin-right:0.4rem;">{b}</span>'
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
    """Top navigation bar. Pass current='overview'|'city'|'tokyo'|'about' to highlight active tab."""
    def _link(label: str, href: str, key: str) -> str:
        active = ' nav-active' if key == current else ''
        return f'<a href="{href}" target="_self" class="nav-lnk{active}">{label}</a>'

    st.markdown(f"""
<style>
.app-nav {{
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 0 36px;
    height: 72px;
    background: rgba(8,12,22,0.97);
    border-bottom: 1px solid rgba(59,130,246,.18);
    position: sticky;
    top: 0;
    z-index: 9999;
    margin-bottom: 0;
}}
.app-nav .nav-logo {{
    font-size: 15px;
    font-weight: 800;
    letter-spacing: .22em;
    text-transform: uppercase;
    color: rgba(255,255,255,.95);
    text-decoration: none;
    margin-right: 20px;
    white-space: nowrap;
}}
.app-nav .nav-lnk {{
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: .11em;
    color: rgba(160,200,240,.65);
    text-decoration: none;
    white-space: nowrap;
    padding: 5px 14px;
    border: 1px solid rgba(59,130,246,.25);
    border-radius: 4px;
    background: rgba(59,130,246,.05);
    transition: color .15s, border-color .15s, background .15s;
}}
.app-nav .nav-lnk:hover {{
    color: rgba(255,255,255,.95);
    border-color: rgba(96,165,250,.70);
    background: rgba(59,130,246,.15);
}}
.app-nav .nav-lnk.nav-active {{
    color: #fff;
    border-color: #3B82F6;
    background: rgba(59,130,246,.22);
}}
/* Remove gap between nav and hero only */
div[data-testid="stVerticalBlock"] {{ gap: 0 !important; }}
div[data-testid="stMarkdownContainer"]:has(.app-nav) {{ margin-bottom: 0 !important; }}
</style>
<div class="app-nav">
  <a class="nav-logo" href="/" target="_self">Japan RE</a>
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
