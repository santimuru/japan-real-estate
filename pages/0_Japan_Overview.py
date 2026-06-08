"""
The Divergence -- Japan's real estate market is splitting in two.
"""
from __future__ import annotations

import numpy as np
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

from utils.styles import (
    inject_css, section_title, callout, kpi_card,
    footer, plotly_base, nav_top, is_dark,
)
from utils.prefecture_data import get_all_as_df

st.set_page_config(
    page_title="The Divergence · Japan RE",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed",
)
inject_css()
nav_top("overview")

PARQUET_PATH = Path(__file__).resolve().parent.parent / "data" / "prefecture_aggregates.parquet"


@st.cache_data(show_spinner=False, ttl=86400)
def load_japan_geojson():
    url = "https://raw.githubusercontent.com/dataofjapan/land/master/japan.geojson"
    return requests.get(url, timeout=20).json()


@st.cache_data(show_spinner=False)
def load_pref_df():
    df = get_all_as_df()
    df["pref_code_str"] = df["code"].astype(int).astype(str).str.zfill(2)

    agg = pd.read_parquet(PARQUET_PATH)
    agg["prefecture_code"] = agg["prefecture_code"].astype(str).str.zfill(2)

    for year in agg["tx_year"].unique():
        sl = agg[agg["tx_year"] == year][["prefecture_code", "median_ppm2"]]
        sl = sl.rename(columns={"median_ppm2": f"price_ppm2_{year}"})
        df = df.merge(sl, left_on="pref_code_str", right_on="prefecture_code", how="left")
        df = df.drop(columns=["prefecture_code"])

    years = sorted(agg["tx_year"].unique())
    first_yr, last_yr = years[0], years[-1]
    df["price_change_pct"] = (
        (df[f"price_ppm2_{last_yr}"] - df[f"price_ppm2_{first_yr}"]) /
        df[f"price_ppm2_{first_yr}"] * 100
    ).fillna(0)
    df["rank_latest"] = df[f"price_ppm2_{last_yr}"].rank(ascending=False).astype(int)
    return df, years


df, YEARS = load_pref_df()
LATEST   = YEARS[-1]
FIRST    = YEARS[0]
PCOL     = f"price_ppm2_{LATEST}"

# ── Hero stats ─────────────────────────────────────────────────────────────────
tokyo_price   = int(df.loc[df["name_en"] == "Tokyo", PCOL].iloc[0])
nat_median    = int(df[PCOL].median())
premium       = tokyo_price / nat_median
pop_declining = int((df["pop_change_pct"] < 0).sum())
akiya_avg     = df["akiya_rate_2023"].mean()
tokyo_growth  = df.loc[df["name_en"] == "Tokyo", "price_change_pct"].iloc[0]

components.html(f"""<!DOCTYPE html>
<html>
<head>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ background:#080808; font-family:system-ui,-apple-system,sans-serif; overflow:hidden; width:100%; }}

#bar {{
  height:3px;
  background:linear-gradient(90deg,#3B82F6,#8B5CF6,#10B981);
  background-size:200% 100%;
  animation:bar-shift 4s linear infinite;
}}
@keyframes bar-shift {{
  0%   {{ background-position:0% 0%; }}
  100% {{ background-position:200% 0%; }}
}}

#hero {{
  display:flex;
  height:297px;
  padding:32px 48px 28px;
  align-items:center;
  gap:56px;
}}

#left {{ flex:1; min-width:0; }}

.kicker {{
  font-size:9px; font-weight:700; text-transform:uppercase;
  letter-spacing:.20em; color:#3B82F6; margin-bottom:14px;
  display:flex; align-items:center; gap:10px;
}}
.kicker::before {{
  content:''; display:block; width:28px; height:1px;
  background:linear-gradient(90deg,#3B82F6,transparent);
  flex-shrink:0;
}}
.title-big {{
  font-size:clamp(52px,7vw,80px); font-weight:900; color:#fff;
  letter-spacing:-.04em; line-height:.86;
  text-shadow:0 0 60px rgba(59,130,246,.18);
  margin-bottom:18px;
}}
.title-sub {{
  font-size:13px; font-weight:400;
  color:rgba(200,225,255,.75);
  line-height:1.80;
  max-width:520px;
  border-left:2px solid rgba(59,130,246,.30);
  padding-left:14px;
}}
.title-sub strong {{ color:#fff; font-weight:600; }}

#right {{
  display:flex;
  flex-direction:column;
  gap:0;
  min-width:190px;
  flex-shrink:0;
}}
.sr-block {{
  padding:11px 0;
  border-bottom:1px solid rgba(255,255,255,.06);
}}
.sr-block:last-child {{ border-bottom:none; }}
.sn {{
  font-size:30px; font-weight:900; color:#3B82F6; line-height:1;
  text-shadow:0 0 20px rgba(59,130,246,.35);
}}
.sl {{
  font-size:8px; font-weight:600; text-transform:uppercase;
  letter-spacing:.10em; color:rgba(160,200,235,.38);
  margin-top:3px; line-height:1.4;
}}
</style>
</head>
<body>
<div id="bar"></div>
<div id="hero">
  <div id="left">
    <div class="kicker">Japan Real Estate · National Analysis · {FIRST}–{LATEST}</div>
    <div class="title-big">THE<br>DIVERGENCE</div>
    <div class="title-sub">
      Tokyo's median price is <strong>{premium:.1f}x the national median</strong> — and the gap is widening.
      <strong>{pop_declining} of 47 prefectures</strong> are losing population while a handful of metros absorb
      everyone leaving. Meanwhile, <strong>9 million homes sit vacant</strong> and uncounted.
      This is what a two-speed country looks like in the data.
    </div>
  </div>
  <div id="right">
    <div class="sr-block">
      <div class="sn">¥{tokyo_price // 10000}万</div>
      <div class="sl">Tokyo median /m²</div>
    </div>
    <div class="sr-block">
      <div class="sn">¥{nat_median // 10000}万</div>
      <div class="sl">National median /m²</div>
    </div>
    <div class="sr-block">
      <div class="sn">{premium:.1f}x</div>
      <div class="sl">Tokyo premium vs national</div>
    </div>
    <div class="sr-block">
      <div class="sn">{akiya_avg:.1f}%</div>
      <div class="sl">Avg national vacancy rate</div>
    </div>
  </div>
</div>
</body>
</html>""", height=300, scrolling=False)


# ══════════════════════════════════════════════════════════════════════════════
# ACT 1 — WHERE IS THE MONEY?
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="height:2px;background:linear-gradient(90deg,rgba(59,130,246,.35),transparent);margin:0 0 2rem;"></div>
""", unsafe_allow_html=True)

section_title("Act I — Where Is the Money?", f"Real transaction medians across all 47 prefectures · {LATEST} data")

st.markdown("""
<p style="color:rgba(200,225,255,.78);font-size:14px;line-height:1.85;max-width:720px;margin:0 0 1.5rem;">
Japan's property market is not one market. It is a handful of metropolitan cores surrounded by a vast landscape
of deflating assets. The choropleth below makes the geography undeniable.
</p>
""", unsafe_allow_html=True)

# Derived stats — 2025 only, YoY vs 2024
tokyo_yr  = int(df.loc[df["name_en"] == "Tokyo", PCOL].iloc[0])
nat_med   = int(df[PCOL].median())
cheapest  = df.loc[df[PCOL].idxmin()]
prem_yr   = tokyo_yr / nat_med

prev_col  = f"price_ppm2_{FIRST}"
df["yoy_pct"] = ((df[PCOL] - df[prev_col]) / df[prev_col] * 100).fillna(0)

def _tooltip_note(row):
    if row["name_en"] == "Tokyo":
        return "23 special wards · deep dive available"
    if row["is_major_metro"]:
        return f"Major metro · {row['region']} region"
    return row["region"] + " region"

df["tooltip_note"] = df.apply(_tooltip_note, axis=1)

map_col, rank_col = st.columns([3, 2])

with map_col:
    try:
        geojson = load_japan_geojson()
        base, _, _ = plotly_base(540, margin=dict(l=0, r=50, t=0, b=0))
        fig_map = px.choropleth_mapbox(
            df, geojson=geojson, locations="name_geo",
            featureidkey="properties.nam", color=PCOL,
            color_continuous_scale=["#1E293B", "#1D4ED8", "#3B82F6", "#60A5FA", "#BFDBFE"],
            mapbox_style="carto-darkmatter",
            center={"lat": 37.0, "lon": 137.0},
            zoom=4.0,
            opacity=0.82,
            hover_name="name_en",
            custom_data=["name_ja", "rank_latest", PCOL, "yoy_pct", "pop_2020", "tooltip_note"],
        )
        fig_map.update_traces(
            marker_line_color="rgba(96,165,250,0.40)",
            marker_line_width=0.6,
            hovertemplate="<extra></extra>",
        )
        # Highlight overlay trace: initially invisible, lit up on hover
        _n = len(df)
        fig_map.add_trace(go.Choroplethmapbox(
            geojson=geojson,
            locations=df["name_geo"].tolist(),
            featureidkey="properties.nam",
            z=[None] * _n,
            colorscale=[[0, "rgba(255,255,255,0.75)"], [1, "rgba(255,255,255,0.75)"]],
            zmin=0, zmax=1,
            showscale=False,
            marker_opacity=0.0,
            marker_line_color="rgba(255,255,255,0.95)",
            marker_line_width=2.5,
            hoverinfo="skip",
            name="_hl",
        ))
        fig_map.update_layout(
            **base,
            coloraxis_colorbar=dict(
                title=dict(text="¥/m²", font=dict(color="rgba(180,210,255,.75)", size=11)),
                tickformat=",.0f", thickness=10, len=0.55, y=0.5, x=1.0,
                tickfont=dict(color="rgba(180,210,255,.65)", size=10),
                tickcolor="rgba(180,210,255,.30)",
            ),
        )
        _map_cfg = {"scrollZoom": False, "doubleClick": "reset", "displayModeBar": False}
        _map_html = fig_map.to_html(
            include_plotlyjs="cdn", full_html=False,
            div_id="price-choropleth",
            config=_map_cfg,
        )
        _hover_js = """
<style>
#pchoro-tip {
  position:fixed; display:none; pointer-events:none; z-index:9999;
  background:rgba(8,12,20,0.97); border:1px solid rgba(70,130,255,.30);
  border-radius:10px; padding:14px 16px; min-width:220px; max-width:275px;
  box-shadow:0 12px 40px rgba(0,0,0,.65);
  font-family:system-ui,-apple-system,sans-serif;
}
</style>
<div id="pchoro-tip"></div>
<script>
(function () {
    var tip = document.getElementById('pchoro-tip');
    var _n = 47;

    function pos(e) {
        var x = e.clientX + 32, y = e.clientY - 120;
        if (x + 280 > window.innerWidth) x = e.clientX - 300;
        if (y < 8) y = e.clientY + 20;
        tip.style.left = x + 'px'; tip.style.top = y + 'px';
    }

    function bind(gd) {
        _n = (gd.data[0].locations || []).length || 47;

        gd.on('plotly_hover', function (ev) {
            if (!ev.points || !ev.points.length) return;
            var pt   = ev.points[0];
            var cd   = pt.customdata || [];
            var enm  = pt.hovertext || '';
            var jan  = cd[0] || '';
            var rnk  = cd[1] != null ? cd[1] : '';
            var prc  = cd[2] != null ? Math.round(cd[2]).toLocaleString('en') : '';
            var yoy  = cd[3] != null ? parseFloat(cd[3]) : null;
            var pop  = cd[4] != null ? parseFloat(cd[4]) : null;
            var note = cd[5] || '';
            var yoyStr = yoy != null ? (yoy >= 0 ? '+' : '') + yoy.toFixed(1) + '% YoY' : '';
            var yoyClr = yoy == null ? '#94A3B8' : yoy > 0 ? '#34D399' : '#F87171';

            tip.innerHTML =
              '<div style="margin-bottom:5px">' +
                '<span style="font-size:15px;font-weight:700;color:#fff">' + enm + '</span>' +
                '&nbsp;<span style="color:rgba(147,197,253,.65);font-size:12px">' + jan + '</span>' +
              '</div>' +
              '<div style="font-size:9px;color:rgba(147,197,253,.38);text-transform:uppercase;letter-spacing:.10em;margin-bottom:10px">' + note + '</div>' +
              '<div style="font-size:9px;color:rgba(147,197,253,.45);text-transform:uppercase;letter-spacing:.08em;margin-bottom:3px">Median ¥/m²</div>' +
              '<div style="margin-bottom:10px">' +
                '<span style="font-size:22px;font-weight:800;color:#60A5FA">¥' + prc + '</span>' +
                (yoyStr ? '&nbsp;<span style="font-size:12px;color:' + yoyClr + '">' + yoyStr + '</span>' : '') +
              '</div>' +
              '<span style="font-size:9px;color:rgba(147,197,253,.45);text-transform:uppercase;letter-spacing:.08em">Rank</span>&nbsp;' +
              '<span style="color:#93C5FD;font-weight:700;font-size:13px">#' + rnk + '</span>&nbsp;' +
              '<span style="font-size:9px;color:rgba(147,197,253,.38)">of 47</span>' +
              '&nbsp;&nbsp;<span style="color:rgba(147,197,253,.25)">·</span>&nbsp;&nbsp;' +
              '<span style="font-size:9px;color:rgba(147,197,253,.45);text-transform:uppercase;letter-spacing:.08em">Pop</span>&nbsp;' +
              '<span style="color:#93C5FD;font-size:12px">' + (pop != null ? pop.toFixed(1) + 'M' : 'n/a') + '</span>';

            pos(ev.event); tip.style.display = 'block';

            var idx = pt.pointIndex;
            var zH = new Array(_n).fill(null); zH[idx] = 1;
            Plotly.restyle(gd, {'z': [zH], 'marker.opacity': [0.90]}, [1]);
            Plotly.restyle(gd, {'marker.opacity': [0.14]}, [0]);
        });

        document.getElementById('price-choropleth').addEventListener('mousemove', function (e) {
            if (tip.style.display === 'block') pos(e);
        });

        gd.on('plotly_unhover', function () {
            tip.style.display = 'none';
            Plotly.restyle(gd, {'z': [new Array(_n).fill(null)], 'marker.opacity': [0.0]}, [1]);
            Plotly.restyle(gd, {'marker.opacity': [0.82]}, [0]);
        });
    }

    (function poll() {
        var gd = document.getElementById('price-choropleth');
        if (!gd || typeof gd.on !== 'function') { setTimeout(poll, 300); return; }
        bind(gd);
    })();
})();
</script>"""
        components.html(_map_html + _hover_js, height=555, scrolling=False)
    except Exception as exc:
        st.warning(f"Map unavailable: {exc}")

with rank_col:
    rank_pos = int(df.loc[df["name_en"] == "Tokyo", "rank_latest"].iloc[0])
    tokyo_yoy = float(df.loc[df["name_en"] == "Tokyo", "yoy_pct"].iloc[0])
    nat_yoy   = float(df["yoy_pct"].median())
    st.markdown(f"""
<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:1rem;">
  <div class="kpi">
    <div class="kpi-label">Tokyo median /m²</div>
    <div class="kpi-value kpi-value-accent">¥{tokyo_yr // 10000}万</div>
    <div class="kpi-sub">#{rank_pos} nationally · {tokyo_yoy:+.1f}% YoY</div>
  </div>
  <div class="kpi">
    <div class="kpi-label">National median</div>
    <div class="kpi-value">¥{nat_med // 10000}万</div>
    <div class="kpi-sub">{LATEST} · {nat_yoy:+.1f}% YoY</div>
  </div>
  <div class="kpi">
    <div class="kpi-label">Tokyo premium</div>
    <div class="kpi-value kpi-value-accent">{prem_yr:.1f}x</div>
    <div class="kpi-sub">vs national median</div>
  </div>
  <div class="kpi">
    <div class="kpi-label">Most affordable</div>
    <div class="kpi-value">{cheapest["name_en"]}</div>
    <div class="kpi-sub">¥{int(cheapest[PCOL]) // 10000}万/m²</div>
  </div>
</div>
""", unsafe_allow_html=True)

    section_title("All 47 prefectures ranked", f"Median ¥/m² · {LATEST}")
    ranked = df[["name_en", "name_ja", PCOL, "yoy_pct", "rank_latest"]].copy()
    ranked = ranked.rename(columns={"name_en": "Prefecture", "name_ja": "日本語"})
    ranked["¥/m²"]   = ranked[PCOL].apply(lambda x: f"¥{int(x) // 10000}万" if pd.notna(x) else "n/a")
    ranked["YoY"]    = ranked["yoy_pct"].apply(lambda x: f"{x:+.1f}%")
    ranked = ranked.sort_values("rank_latest")[["Prefecture", "日本語", "¥/m²", "YoY"]].reset_index(drop=True)
    ranked.index = ranked.index + 1
    st.dataframe(ranked, use_container_width=True, height=400)

gap_latest = df.loc[df["name_en"] == "Tokyo", PCOL].iloc[0] / df[PCOL].min()
callout(
    f"Tokyo trades at <strong>{gap_latest:.1f}x</strong> the cheapest prefecture in {LATEST}. "
    f"Tokyo grew <strong>{tokyo_yoy:+.1f}%</strong> YoY vs a national median of "
    f"<strong>{nat_yoy:+.1f}%</strong>. Capital concentration is not a forecast — "
    f"it is the current reality in the transaction data."
)


# ══════════════════════════════════════════════════════════════════════════════
# ACT 2 — THE SPLIT
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="height:2px;background:linear-gradient(90deg,rgba(59,130,246,.35),transparent);margin:2rem 0;"></div>
""", unsafe_allow_html=True)

section_title("Act II — The Split", f"Population change 2010-2020 vs price appreciation {FIRST}-{LATEST}")

st.markdown("""
<p style="color:rgba(200,225,255,.78);font-size:14px;line-height:1.85;max-width:720px;margin:0 0 1.5rem;">
The simplest question in regional economics: do people follow prices, or do prices follow people?
In Japan, the answer is both and neither. Population is shrinking almost everywhere — but prices
are rising almost everywhere too. What separates the fast from the slow is not demographics.
It is proximity to the capital.
</p>
""", unsafe_allow_html=True)

# Scatter stats
growing       = int((df["pop_change_pct"] > 0).sum())
declining     = int((df["pop_change_pct"] <= 0).sum())
avg_price_chg = df["price_change_pct"].mean()
m_coef, b_coef = np.polyfit(df["pop_change_pct"], df["price_change_pct"], 1)
corr   = df["pop_change_pct"].corr(df["price_change_pct"])
r_sq   = corr ** 2

c1, c2, c3, c4 = st.columns(4)
with c1: kpi_card("Prefectures declining",  f"{declining}/47",                "Population 2010-2020")
with c2: kpi_card("Prefectures growing",    f"{growing}/47",                  "Population 2010-2020")
with c3: kpi_card("Avg price growth",       f"+{avg_price_chg:.0f}%",         f"{FIRST}-{LATEST} national", accent=True)
with c4: kpi_card("Tokyo price growth",     f"+{tokyo_growth:.0f}%",          f"{FIRST}-{LATEST}", accent=True)

top3_growth = df.nlargest(3, "price_change_pct")[["name_en", "price_change_pct"]]
top3_str = ", ".join(
    f"<strong>{r['name_en']}</strong> (+{r['price_change_pct']:.0f}%)"
    for _, r in top3_growth.iterrows()
)
callout(
    f"Strongest price growth {FIRST}-{LATEST}: {top3_str}. "
    f"Bubbles are sized by {LATEST} median ¥/m² — the bigger the dot, the more expensive."
)

dark       = is_dark()
ann_bg     = "rgba(8,12,20,0.92)"
ann_border = "#2D3748"
ann_font   = "#E2E8F0"

sc_chart, sc_insight = st.columns([3, 1])

with sc_chart:
    base, grid, zero = plotly_base(460)
    fig_scatter = px.scatter(
        df,
        x="pop_change_pct",
        y="price_change_pct",
        color="is_major_metro",
        size=PCOL,
        size_max=28,
        color_discrete_map={True: "#3B82F6", False: "#475569"},
        labels={
            "pop_change_pct":   "Population change 2010-2020 (%)",
            "price_change_pct": f"Price appreciation {FIRST}-{LATEST} (%)",
            "is_major_metro":   "Major metro",
        },
        hover_name="name_en",
        hover_data={"pop_change_pct": ":.1f", "price_change_pct": ":.1f", PCOL: False},
    )
    x_range = [df["pop_change_pct"].min() - 0.5, df["pop_change_pct"].max() + 0.5]
    fig_scatter.add_scatter(
        x=x_range, y=[m_coef * x + b_coef for x in x_range],
        mode="lines", line=dict(color="#475569", dash="dot", width=1.5),
        showlegend=False,
    )
    label_mask = (
        df["is_major_metro"] |
        (df["price_change_pct"] == df["price_change_pct"].max()) |
        (df["price_change_pct"] == df["price_change_pct"].min())
    )
    for _, row in df[label_mask].iterrows():
        fig_scatter.add_annotation(
            x=row["pop_change_pct"], y=row["price_change_pct"],
            text=row["name_en"],
            showarrow=True, arrowhead=0, arrowwidth=1,
            arrowcolor=ann_border, ax=0, ay=-26,
            font=dict(size=9, color=ann_font),
            bgcolor=ann_bg, bordercolor=ann_border,
            borderwidth=1, borderpad=3,
        )
    fig_scatter.update_layout(
        **base,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    font=dict(color=ann_font)),
    )
    fig_scatter.update_xaxes(gridcolor=grid, zeroline=True, zerolinecolor=zero, ticksuffix="%")
    fig_scatter.update_yaxes(gridcolor=grid, zeroline=True, zerolinecolor=zero, ticksuffix="%")
    fig_scatter.add_hline(y=0, line_dash="dot", line_color=zero)
    fig_scatter.add_vline(x=0, line_dash="dot", line_color=zero)
    fig_scatter.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>Population change: %{x:.1f}%<br>Price growth: %{y:.0f}%<extra></extra>"
    )
    st.plotly_chart(fig_scatter, use_container_width=True,
                    config={"scrollZoom": False, "doubleClick": False, "displayModeBar": False})

with sc_insight:
    most_surprising = df[~df["is_major_metro"]].nlargest(3, "price_change_pct")[["name_en", "price_change_pct"]]
    st.markdown(f"""
<div style="padding:1.2rem;background:rgba(59,130,246,.06);border:1px solid rgba(59,130,246,.18);
border-radius:10px;margin-top:2.2rem;">
  <div style="font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:.12em;
  color:rgba(100,160,255,.55);margin-bottom:1rem;">Key Finding</div>
  <div style="font-size:26px;font-weight:900;color:#3B82F6;line-height:1;">R² = {r_sq:.2f}</div>
  <div style="font-size:11px;color:rgba(160,200,255,.55);margin-top:.4rem;line-height:1.6;">
    Population explains only {r_sq*100:.0f}% of price variation.
    Near-zero BoJ rates lifted all 47 prefectures regardless of demographics.
  </div>
  <div style="margin-top:1.2rem;padding-top:1rem;border-top:1px solid rgba(59,130,246,.15);">
    <div style="font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:.10em;
    color:rgba(100,160,255,.45);margin-bottom:.6rem;">Non-metro surprises</div>
    {"".join(f'<div style="font-size:12px;color:rgba(180,215,255,.70);margin-bottom:.3rem;"><strong style=color:#93C5FD>{r["name_en"]}</strong> +{r["price_change_pct"]:.0f}%</div>' for _, r in most_surprising.iterrows())}
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ACT 3 — THE GHOST TOWNS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="height:2px;background:linear-gradient(90deg,rgba(239,68,68,.35),transparent);margin:2rem 0;"></div>
""", unsafe_allow_html=True)

section_title("Act III — The Ghost Towns", "Japan's akiya (空き家) vacancy crisis · 2013 → 2023")

st.markdown("""
<p style="color:rgba(200,225,255,.78);font-size:14px;line-height:1.85;max-width:720px;margin:0 0 1.5rem;">
Akiya — literally "empty house" — is one of the most structurally unique problems in the global housing market.
Japan has more vacant homes than it has households in many of its prefectures. The homes are not abandoned
due to poverty or disaster. They are the accumulated inheritance of a country that built for growth and
then stopped growing. Cultural resistance to selling family property, high demolition costs,
and complex inheritance law have locked 9 million units out of the market.
</p>
""", unsafe_allow_html=True)

worst_row    = df.loc[df["akiya_rate_2023"].idxmax()]
avg_change   = (df["akiya_rate_2023"] - df["akiya_rate_2013"]).mean()
high_vacancy = int((df["akiya_rate_2023"] >= 20).sum())

c1, c2, c3, c4 = st.columns(4)
with c1: kpi_card("Vacant homes",        "9 million",                    "2023 Housing & Land Survey", accent=True)
with c2: kpi_card("National avg vacancy",f"{akiya_avg:.1f}%",            "2023")
with c3: kpi_card("Worst prefecture",    worst_row["name_en"],           f"{worst_row['akiya_rate_2023']:.1f}% vacancy", accent=True)
with c4: kpi_card("10-yr increase",      f"+{avg_change:.1f}pp",         "2013-2023 avg change")

top3_akiya = df.nlargest(3, "akiya_rate_2023")[["name_en", "akiya_rate_2023"]]
top3_str = ", ".join(
    f"<strong>{r['name_en']}</strong> ({r['akiya_rate_2023']:.1f}%)"
    for _, r in top3_akiya.iterrows()
)
callout(
    f"The hardest-hit prefectures — {top3_str} — are above 20% vacancy. "
    f"Urban prefectures have lower rates but growing absolute numbers as households shrink "
    f"and inheritances pile up with no buyers.",
    variant="neg",
)

col_map, col_bar = st.columns([3, 2])

try:
    geojson = load_japan_geojson()
    with col_map:
        base, _, _ = plotly_base(480, margin=dict(l=0, r=60, t=0, b=0))
        df["akiya_change"] = df["akiya_rate_2023"] - df["akiya_rate_2013"]
        fig_akiya = px.choropleth(
            df, geojson=geojson, locations="name_geo",
            featureidkey="properties.nam", color="akiya_rate_2023",
            color_continuous_scale=["#334155", "#7C2D12", "#DC2626", "#FCA5A5"],
            labels={"akiya_rate_2023": "Vacancy %"},
            hover_name="name_en",
            custom_data=["name_ja", "akiya_rate_2023", "akiya_rate_2013", "akiya_change"],
        )
        fig_akiya.update_traces(
            marker_line_color="rgba(252,165,165,0.30)",
            marker_line_width=0.5,
            hovertemplate=(
                "<span style='font-size:14px;font-weight:700;color:#fff'>%{hovertext}</span>"
                "  <span style='color:rgba(252,165,165,.55);font-size:12px'>%{customdata[0]}</span><br>"
                "<span style='color:rgba(252,165,165,.5);font-size:10px;text-transform:uppercase;"
                "letter-spacing:.08em'>Vacancy 2023</span><br>"
                "<span style='font-size:20px;font-weight:800;color:#EF4444'>"
                "%{customdata[1]:.1f}%</span><br>"
                "<span style='color:rgba(252,165,165,.5);font-size:10px'>2013: %{customdata[2]:.1f}%"
                " &nbsp;·&nbsp; change: %{customdata[3]:+.1f}pp</span>"
                "<extra></extra>"
            ),
        )
        fig_akiya.update_geos(
            visible=False,
            bgcolor="rgba(0,0,0,0)",
            projection_type="mercator",
            lonaxis_range=[122, 150],
            lataxis_range=[23, 46],
        )
        fig_akiya.update_layout(
            **base,
            coloraxis_colorbar=dict(
                title=dict(text="Vacancy %", font=dict(color="rgba(252,165,165,.75)", size=11)),
                ticksuffix="%", thickness=10, len=0.55, y=0.5, x=1.0,
                tickfont=dict(color="rgba(252,165,165,.65)", size=10),
                tickcolor="rgba(252,165,165,.30)",
            ),
        )
        st.plotly_chart(fig_akiya, use_container_width=True,
                        config={"scrollZoom": False, "doubleClick": False, "displayModeBar": False})
except Exception as exc:
    st.warning(f"Map unavailable: {exc}")

with col_bar:
    section_title("Top 15 by vacancy rate", "2023 Housing & Land Survey")
    top15 = df.nlargest(15, "akiya_rate_2023")[["name_en", "akiya_rate_2023"]].copy()
    base3, grid3, _ = plotly_base(480)
    fig_vac = px.bar(
        top15.sort_values("akiya_rate_2023"),
        x="akiya_rate_2023", y="name_en", orientation="h",
        color="akiya_rate_2023",
        color_continuous_scale=["#7C2D12", "#DC2626", "#FCA5A5"],
        labels={"akiya_rate_2023": "Vacancy rate (%)", "name_en": ""},
    )
    fig_vac.update_layout(**base3)
    fig_vac.update_coloraxes(showscale=False)
    fig_vac.update_xaxes(gridcolor=grid3, ticksuffix="%")
    fig_vac.update_traces(hovertemplate="%{y}<br>Vacancy: %{x:.1f}%<extra></extra>")
    st.plotly_chart(fig_vac, use_container_width=True,
                    config={"scrollZoom": False, "doubleClick": False, "displayModeBar": False})

# Region trend
section_title("Vacancy trend by region", "Average rate per region · 2013, 2018, 2023")

trend_data = []
for _, row in df.iterrows():
    for yr, col in [(2013, "akiya_rate_2013"), (2018, "akiya_rate_2018"), (2023, "akiya_rate_2023")]:
        trend_data.append({"region": row["region"], "year": yr, "akiya_rate": row[col]})
region_trend = (
    pd.DataFrame(trend_data)
    .groupby(["region", "year"])["akiya_rate"]
    .mean()
    .reset_index()
)

trend_col, trend_insight = st.columns([3, 1])

with trend_col:
    base4, grid4, _ = plotly_base(280)
    fig_trend = px.line(
        region_trend, x="year", y="akiya_rate", color="region", markers=True,
        labels={"year": "", "akiya_rate": "Avg vacancy (%)", "region": ""},
        color_discrete_sequence=["#3B82F6", "#F59E0B", "#EF4444", "#8B5CF6", "#10B981",
                                  "#EC4899", "#14B8A6", "#F97316"],
    )
    fig_trend.update_layout(
        **base4,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    font=dict(color="#E2E8F0")),
    )
    fig_trend.update_xaxes(showgrid=False, tickvals=[2013, 2018, 2023])
    fig_trend.update_yaxes(gridcolor=grid4, ticksuffix="%")
    fig_trend.update_traces(
        hovertemplate="%{fullData.name}<br>%{x}<br>Avg vacancy: %{y:.1f}%<extra></extra>"
    )
    st.plotly_chart(fig_trend, use_container_width=True,
                    config={"scrollZoom": False, "doubleClick": False, "displayModeBar": False})

with trend_insight:
    st.markdown(f"""
<div style="padding:1.2rem;background:rgba(239,68,68,.06);border:1px solid rgba(239,68,68,.20);
border-radius:10px;margin-top:2rem;">
  <div style="font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:.12em;
  color:rgba(255,100,100,.55);margin-bottom:1rem;">Projection</div>
  <div style="font-size:24px;font-weight:900;color:#EF4444;line-height:1;">&gt;20%</div>
  <div style="font-size:11px;color:rgba(255,180,180,.55);margin-top:.4rem;line-height:1.6;">
    National vacancy rate before 2035 if current +{avg_change:.1f}pp per-decade trend holds.
  </div>
  <div style="margin-top:1rem;padding-top:1rem;border-top:1px solid rgba(239,68,68,.15);
  font-size:11px;color:rgba(255,160,160,.50);line-height:1.7;">
    Every region accelerated after 2018. Some municipalities now pay buyers ¥1M+ to take akiya.
  </div>
</div>
""", unsafe_allow_html=True)

footer("The Divergence", "MLIT XIT001 API · Japan Housing and Land Survey · Statistics Bureau")
