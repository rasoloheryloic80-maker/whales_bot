# whales_bot
 30
 31
 32
 33
 34
 35
 36
 37
 38
 39
 40
 41
 42
 43
 44
 45
 46
 47
 48
 49
 50
 51
 52
 53
 54
 55
 56
 57
 58
 59
 60
 61
 62
 63
 64
 65
 66
import streamlit as st
        self.data['SMA_50'] = ta.trend.SMAIndicator(close_prices, window=50).sma_indicator()
        macd_obj = ta.trend.MACD(close_prices)
        self.data['MACD'] = macd_obj.macd()
        self.data['MACD_Signal'] = macd_obj.macd_signal()
        return True

    def generate_signals(self):
        self.data['Signal'] = 0
        self.data.loc[self.data['RSI'] < 30, 'Signal'] = 1
        self.data.loc[self.data['RSI'] > 70, 'Signal'] = -1

    def create_dashboard(self):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.data.index, y=self.data['Close'], mode='lines', name='Prix', line=dict(color='#00D9FF', width=2)))
        fig.add_trace(go.Scatter(x=self.data.index, y=self.data['SMA_20'], mode='lines', name='SMA 20', line=dict(color='#FFD700', width=1, dash='dash')))
        fig.update_layout(template='plotly_dark', height=600, plot_bgcolor='#0a0e27', paper_bgcolor='#0a0e27', title=f'WhalesBot - {self.ticker}')
        return fig

# Interface Streamlit
st.set_page_config(page_title="WhalesBot", layout="wide")
st.title("🐋 WhalesBot - Analyse Quantitative")

with st.sidebar:
    st.header("⚙️ Configuration")
    ticker = st.text_input("Ticker (AAPL, GOOGL, etc)", "AAPL").upper()
    period = st.selectbox("Période", ["1mo", "3mo", "6mo", "1y", "2y", "5y"])
    
    if st.button("🔄 Analyser", use_container_width=True):
        bot = WhalesBot(ticker, period)
        if bot.download_data():
            bot.calculate_indicators()
            bot.generate_signals()
            fig = bot.create_dashboard()
            st.plotly_chart(fig, use_container_width=True)
            st.success("✅ Analyse complétée !")
        else:
            st.error("❌ Erreur : Ticker invalide")
yfinance==0.2.32
pandas==2.0.3
ta==0.10.2
plotly==5.17.0
streamlit==1.28.1
numpy==1.24.3
[theme]
primaryColor = "#00D9FF"
backgroundColor = "#0a0e27"
secondaryBackgroundColor = "#1a1f3a"
textColor = "#ffffff"
font = "monospace"

[server]
headless = true
runOnSave = true
