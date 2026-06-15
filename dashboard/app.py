# ============================================================
# StockVision — Volatility Intelligence Dashboard
# Run: streamlit run dashboard/app.py
# ============================================================
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine, text
import calendar, os, sys

# ── Path setup ────────────────────────────────────────────────
script_dir   = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.insert(0, project_root)
import config

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title = "StockVision — Volatility Intelligence",
    page_icon  = "📈",
    layout     = "wide",
    initial_sidebar_state = "expanded"
)

# ── DB connection (cached — created once) ─────────────────────
@st.cache_resource
def get_engine():
    return create_engine(
        f"mysql+pymysql://{config.DB_CONFIG['user']}:{config.DB_CONFIG['password']}"
        f"@{config.DB_CONFIG['host']}:{config.DB_CONFIG['port']}/{config.DB_CONFIG['database']}"
    )

engine = get_engine()

# ── Data loaders (cached per session) ────────────────────────
@st.cache_data
def load_vol():
    return pd.read_sql("SELECT * FROM stock_volatility",  engine)

@st.cache_data
def load_rr():
    return pd.read_sql("SELECT * FROM stock_risk_return", engine)

@st.cache_data
def load_seasonality():
    df = pd.read_sql(
        "SELECT market, MONTH(trade_date) AS mn, ROUND(AVG(daily_return)*100,4) AS avg_ret "
        "FROM stock_features WHERE daily_return IS NOT NULL "
        "GROUP BY market, MONTH(trade_date) ORDER BY market, mn",
        engine
    )
    df['month'] = df['mn'].apply(lambda x: calendar.month_abbr[x])
    return df

@st.cache_data
def load_trend(ticker):
    return pd.read_sql(
        "SELECT trade_date, close_price, ma_50, ma_200 "
        "FROM stock_features WHERE ticker = %(t)s ORDER BY trade_date",
        engine, params={'t': ticker}, parse_dates=['trade_date']
    )

vol = load_vol()
rr  = load_rr()

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.title("📈 StockVision")
    st.caption("Volatility Intelligence for Traders")
    st.divider()

    market_sel  = st.selectbox("Market", ["Both", "India", "US"])
    sector_sel  = st.multiselect("Sector",
                                  sorted(vol['sector'].unique()),
                                  default=sorted(vol['sector'].unique()))
    cat_sel     = st.multiselect("Volatility Category",
                                  ["High", "Medium", "Low"],
                                  default=["High", "Medium", "Low"])
    st.divider()
    st.caption("📅 2010 – 2024  ·  80 stocks  ·  India & US")

# ── Filter helper ─────────────────────────────────────────────
def filt(df):
    m = df['sector'].isin(sector_sel)
    if 'volatility_category' in df.columns:          # ← only filter if column exists
        m = m & df['volatility_category'].isin(cat_sel)
    if market_sel != "Both":
        m = m & (df['market'] == market_sel)
    return df[m]

vf = filt(vol)
rf = filt(rr)

COLOR = {'India': '#EF553B', 'US': '#636EFA'}

# ══════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════
t1, t2, t3, t4 = st.tabs([
    "📊 Overview", "⚖️ Risk & Return", "🔗 Correlations", "🔍 Stock Deep Dive"
])

# ─────────────────────────────────────────────────────────────
# TAB 1 — OVERVIEW
# ─────────────────────────────────────────────────────────────
with t1:
    st.header("Market Overview")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Stocks shown",        len(vf))
    c2.metric("Avg volatility",      f"{vf['ann_volatility_pct'].mean():.1f}%"
                                     if len(vf) else "—")

    if len(vf):
        mv = vf.nlargest(1, 'ann_volatility_pct').iloc[0]
        c3.metric("Most volatile", mv['ticker'], f"{mv['ann_volatility_pct']:.1f}%")
        bc = rf.nlargest(1, 'cagr_pct').iloc[0] if len(rf) else None
        c4.metric("Highest CAGR", bc['ticker'] if bc is not None else "—",
                  f"{bc['cagr_pct']:.1f}%" if bc is not None else "")

    st.divider()

    if len(vf) == 0:
        st.warning("No stocks match the current filters.")
    else:
        top = vf.nlargest(15, 'ann_volatility_pct').sort_values('ann_volatility_pct')
        fig = px.bar(top, x='ann_volatility_pct', y='ticker', color='market',
                     orientation='h', text='ann_volatility_pct',
                     color_discrete_map=COLOR,
                     title='Top 15 Most Volatile Stocks',
                     labels={'ann_volatility_pct': 'Annualised Volatility (%)', 'ticker': ''})
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(height=500, plot_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Full Volatility Rankings")
        st.dataframe(
            vf[['ticker','company_name','market','sector',
                'ann_volatility_pct','avg_atr_pct',
                'max_drawdown_pct','volatility_rank','volatility_category']]
            .sort_values('volatility_rank').reset_index(drop=True),
            use_container_width=True, hide_index=True
        )

# ─────────────────────────────────────────────────────────────
# TAB 2 — RISK & RETURN
# ─────────────────────────────────────────────────────────────
with t2:
    st.header("Risk vs Return")

    if len(rf):
        rp = rf.copy()
        rp['drawdown_size'] = rp['max_drawdown_pct'].abs()
        fig = px.scatter(
            rp, x='ann_volatility_pct', y='cagr_pct',
            color='market', size='drawdown_size', size_max=25,
            hover_data=['ticker','company_name','sector','sharpe_ratio'],
            color_discrete_map=COLOR,
            labels={'ann_volatility_pct': 'Annualised Volatility (%)',
                    'cagr_pct': 'CAGR (%)', 'drawdown_size': 'Max Drawdown (%)'},
            title='Risk vs Return — Bubble Size = Max Drawdown'
        )
        fig.update_layout(height=500, plot_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data for current filters.")

    st.divider()
    st.subheader("Sector Volatility Comparison")
    sv = vf.groupby(['market','sector'])['ann_volatility_pct'].mean().round(2).reset_index()
    fig2 = px.bar(sv, x='sector', y='ann_volatility_pct', color='market',
                  barmode='group', color_discrete_map=COLOR,
                  title='Average Annualised Volatility by Sector',
                  labels={'ann_volatility_pct': 'Avg Volatility (%)', 'sector': ''})
    fig2.update_layout(height=400, plot_bgcolor='white', xaxis_tickangle=-30)
    st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    st.subheader("Monthly Seasonality")
    seas = load_seasonality()
    if market_sel != "Both":
        seas = seas[seas['market'] == market_sel]
    fig3 = px.line(seas, x='month', y='avg_ret', color='market',
                   markers=True, color_discrete_map=COLOR,
                   labels={'avg_ret': 'Avg Daily Return (%)', 'month': 'Month'},
                   title='Average Daily Return by Month')
    fig3.add_hline(y=0, line_dash='dash', line_color='gray', opacity=0.4)
    fig3.update_layout(height=380, plot_bgcolor='white')
    st.plotly_chart(fig3, use_container_width=True)

# ─────────────────────────────────────────────────────────────
# TAB 3 — CORRELATIONS
# ─────────────────────────────────────────────────────────────
with t3:
    st.header("Return Correlations")
    mkt = st.radio("Market", ["India", "US"], horizontal=True)

    corr_file = os.path.join(project_root, 'data', 'processed',
                             f'corr_{mkt.lower()}.csv')
    if os.path.exists(corr_file):
        corr = pd.read_csv(corr_file, index_col=0)
        fig  = px.imshow(corr, color_continuous_scale='RdBu_r',
                         zmin=-1, zmax=1, aspect='auto',
                         title=f'Daily Return Correlation — {mkt} Stocks')
        fig.update_layout(height=650)
        st.plotly_chart(fig, use_container_width=True)

        avg = corr.values[~np.eye(len(corr), dtype=bool)].mean()
        st.info(f"Average pairwise correlation across {mkt} stocks: **{avg:.3f}**")
    else:
        st.warning("Correlation file not found. Run Phase 7 Cell 5 to generate it.")

# ─────────────────────────────────────────────────────────────
# TAB 4 — STOCK DEEP DIVE
# ─────────────────────────────────────────────────────────────
with t4:
    st.header("Stock Deep Dive")

    options = sorted(vol['ticker'].tolist())
    sel     = st.selectbox("Select a stock", options)

    if sel:
        vi = vol[vol['ticker'] == sel].iloc[0]
        ri = rr[rr['ticker']  == sel]

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("CAGR",            f"{ri['cagr_pct'].values[0]:.1f}%"
                                     if len(ri) else "—")
        c2.metric("Sharpe Ratio",    f"{ri['sharpe_ratio'].values[0]:.2f}"
                                     if len(ri) else "—")
        c3.metric("Ann. Volatility", f"{vi['ann_volatility_pct']:.1f}%")
        c4.metric("Max Drawdown",    f"{vi['max_drawdown_pct']:.1f}%")
        c5.metric("Avg ATR",         f"{vi['avg_atr_pct']:.2f}%")

        st.caption(f"**{vi['company_name']}**  ·  {vi['market']}  ·  "
                   f"{vi['sector']}  ·  Category: **{vi['volatility_category']}**")

        st.divider()
        df_t = load_trend(sel)
        if len(df_t):
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_t['trade_date'], y=df_t['close_price'],
                                     name='Close',
                                     line=dict(color='#636EFA', width=1.5)))
            fig.add_trace(go.Scatter(x=df_t['trade_date'], y=df_t['ma_50'],
                                     name='MA 50',
                                     line=dict(color='#FFA15A', width=1.5, dash='dot')))
            fig.add_trace(go.Scatter(x=df_t['trade_date'], y=df_t['ma_200'],
                                     name='MA 200',
                                     line=dict(color='#EF553B', width=1.5, dash='dash')))
            fig.update_layout(
                title=f'{sel} — Price Trend with MA50 & MA200 (2010–2024)',
                height=470, plot_bgcolor='white', hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)