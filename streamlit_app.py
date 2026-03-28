import streamlit as st
import yfinance as yf
import pandas as pd
import ta
import plotly.graph_objects as go

st.set_page_config(page_title="WhalesBot", layout="wide")

st.markdown("""
<style>
body { background-color: #0a0e27; color: #ffffff; }
.stApp { background-color: #0a0e27; }
</style>
""", unsafe_allow_html=True)

st.title("🐋 WhalesBot - Analyse Quantitative")

with st.sidebar:
    st.header("⚙️ Configuration")
    ticker = st.text_input("Ticker (AAPL, GOOGL, MSFT...)", "AAPL").upper()
    period = st.selectbox("Période", ["1mo", "3mo", "6mo", "1y", "2y", "5y"])
    
    if st.button("🔄 Analyser", use_container_width=True):
        st.session_state.analyze = True

if 'analyze' in st.session_state:
    with st.spinner("📊 Analyse en cours..."): 
        try:
            df = yf.download(ticker, period=period, progress=False)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            
            close_prices = df['Close'].squeeze()
            df['RSI'] = ta.momentum.RSIIndicator(close_prices, window=14).rsi()
            df['SMA_20'] = ta.trend.SMAIndicator(close_prices, window=20).sma_indicator()
            df['SMA_50'] = ta.trend.SMAIndicator(close_prices, window=50).sma_indicator()
            
            macd_obj = ta.trend.MACD(close_prices)
            df['MACD'] = macd_obj.macd()
            df['MACD_Signal'] = macd_obj.macd_signal()
            
            df['Signal'] = 0
            df.loc[df['RSI'] < 30, 'Signal'] = 1
            df.loc[df['RSI'] > 70, 'Signal'] = -1
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("💰 Prix", f"${df['Close'].iloc[-1]:.2f}")
            with col2:
                variation = ((df['Close'].iloc[-1] - df['Close'].iloc[0]) / df['Close'].iloc[0] * 100)
                st.metric("📈 Variation", f"{variation:.2f}%")
            with col3:
                st.metric("📊 RSI", f"{df['RSI'].iloc[-1]:.2f}")
            with col4:
                signal = df['Signal'].iloc[-1]
                signal_text = "🟢 ACHAT" if signal == 1 else "🔴 VENTE" if signal == -1 else "⚪ NEUTRE"
                st.metric("🎯 Signal", signal_text)
            
            st.markdown("---")
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Prix', line=dict(color='#00D9FF', width=2)))
            fig.add_trace(go.Scatter(x=df.index, y=df['SMA_20'], mode='lines', name='SMA 20', line=dict(color='#FFD700', width=1, dash='dash')))
            fig.add_trace(go.Scatter(x=df.index, y=df['SMA_50'], mode='lines', name='SMA 50', line=dict(color='#FF6B6B', width=1, dash='dash')))
            
            buy_signals = df[df['Signal'] == 1]
            sell_signals = df[df['Signal'] == -1]
            
            fig.add_trace(go.Scatter(x=buy_signals.index, y=buy_signals['Close'], mode='markers', name='ACHAT', marker=dict(size=12, color='#00FF00', symbol='triangle-up')))
            fig.add_trace(go.Scatter(x=sell_signals.index, y=sell_signals['Close'], mode='markers', name='VENTE', marker=dict(size=12, color='#FF0000', symbol='triangle-down')))
            
            fig.update_layout(template='plotly_dark', height=600, plot_bgcolor='#0a0e27', paper_bgcolor='#0a0e27', title=f'{ticker}', hovermode='x unified')
            st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("📈 Indicateurs")
            col_rsi, col_macd = st.columns(2)
            
            with col_rsi:
                fig_rsi = go.Figure()
                fig_rsi.add_trace(go.Scatter(x=df.index, y=df['RSI'], mode='lines', name='RSI', line=dict(color='#00D9FF', width=2)))
                fig_rsi.add_hline(y=70, line_dash="dash", line_color="red")
                fig_rsi.add_hline(y=30, line_dash="dash", line_color="green")
                fig_rsi.update_layout(template='plotly_dark', height=300, plot_bgcolor='#0a0e27', paper_bgcolor='#0a0e27', title='RSI (14)')
                st.plotly_chart(fig_rsi, use_container_width=True)
            
            with col_macd:
                fig_macd = go.Figure()
                fig_macd.add_trace(go.Scatter(x=df.index, y=df['MACD'], mode='lines', name='MACD', line=dict(color='#00D9FF', width=2)))
                fig_macd.add_trace(go.Scatter(x=df.index, y=df['MACD_Signal'], mode='lines', name='Signal', line=dict(color='#FFD700', width=2)))
                fig_macd.update_layout(template='plotly_dark', height=300, plot_bgcolor='#0a0e27', paper_bgcolor='#0a0e27', title='MACD')
                st.plotly_chart(fig_macd, use_container_width=True)
            
            st.subheader("📋 Données")
            display_data = df[['Close', 'RSI', 'SMA_20', 'MACD', 'Signal']].tail(20).copy()
            display_data.columns = ['Prix', 'RSI', 'SMA 20', 'MACD', 'Signal']
            display_data['Signal'] = display_data['Signal'].map({1: '🟢 ACHAT', -1: '🔴 VENTE', 0: '⚪ NEUTRE'})
            st.dataframe(display_data, use_container_width=True)
            
            st.success("✅ Analyse complétée !")
        except Exception as e:
            st.error(f"❌ Erreur : {e}")
else:
    st.info("👈 Entrez un ticker et cliquez sur 'Analyser' pour commencer")