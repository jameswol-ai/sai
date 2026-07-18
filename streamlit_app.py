# ============================================================
# SAI AI Forex Bot v5.0
# Single File Streamlit Edition
# Login + User Management + AI Trading Dashboard
# ============================================================

import streamlit as st
import sqlite3
import hashlib
import random
import threading
import queue
import time
import logging
import warnings
from pathlib import Path
from datetime import datetime, timedelta

import pandas as pd
import numpy as np
import requests


# ============================================================
# STREAMLIT CONFIG
# ============================================================

st.set_page_config(
    page_title="SAI AI Forex Intelligence",
    page_icon="📈",
    layout="wide"
)


BASE_DIR = Path(__file__).parent

USER_DB = BASE_DIR / "sai_users.db"
TRADING_DB = BASE_DIR / "sai_trading.db"


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger("SAI")


# ============================================================
# OPTIONAL PLOTLY
# ============================================================

try:
    import plotly.graph_objects as go
    PLOTLY = True

except Exception:
    PLOTLY = False



# ============================================================
# DATABASE CORE
# ============================================================

def db(path):

    return sqlite3.connect(
        path,
        check_same_thread=False
    )



def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()



def init_databases():

    conn = db(USER_DB)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS users(

        username TEXT PRIMARY KEY,
        password TEXT,
        role TEXT,
        email TEXT

    )
    """)


    count = conn.execute(
        "SELECT COUNT(*) FROM users"
    ).fetchone()[0]


    if count == 0:

        conn.execute(
            """
            INSERT INTO users
            VALUES(?,?,?,?)
            """,
            (
                "admin",
                hash_password("admin123"),
                "admin",
                "admin@sai.ai"
            )
        )


    conn.commit()
    conn.close()



    conn = db(TRADING_DB)


    conn.executescript("""

    CREATE TABLE IF NOT EXISTS trades(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        time TEXT,
        symbol TEXT,
        action TEXT,
        price REAL,
        pnl REAL

    );


    CREATE TABLE IF NOT EXISTS account(

        username TEXT PRIMARY KEY,
        balance REAL,
        equity REAL

    );


    CREATE TABLE IF NOT EXISTS market(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        time TEXT,
        currency TEXT,
        rate REAL

    );

    """)


    conn.commit()
    conn.close()



init_databases()



# ============================================================
# USER MANAGEMENT
# ============================================================

def authenticate(username,password):

    conn=db(USER_DB)

    row=conn.execute(
        """
        SELECT role
        FROM users
        WHERE username=?
        AND password=?
        """,
        (
            username,
            hash_password(password)
        )
    ).fetchone()


    conn.close()


    if row:

        return True,row[0]


    return False,None




def register(username,password,email=""):

    try:

        conn=db(USER_DB)

        conn.execute(
            """
            INSERT INTO users
            VALUES(?,?,?,?)
            """,
            (
                username,
                hash_password(password),
                "user",
                email
            )
        )


        conn.commit()
        conn.close()

        return True


    except Exception:

        return False




def users():

    conn=db(USER_DB)

    data=pd.read_sql(
        """
        SELECT username,role,email
        FROM users
        """,
        conn
    )

    conn.close()

    return data



def delete_user(username):

    conn=db(USER_DB)

    conn.execute(
        "DELETE FROM users WHERE username=?",
        (username,)
    )

    conn.commit()
    conn.close()



# ============================================================
# SESSION STATE
# ============================================================

defaults={

    "login":False,

    "username":"",
    "role":"",

    "balance":10000.0,

    "bot_running":False,

    "auto_trade":False,

    "risk":5,

    "signals":[],

    "history":[],

    "bot_queue":queue.Queue(),

    "thread":None,

    "stop":None

}



for key,value in defaults.items():

    if key not in st.session_state:

        st.session_state[key]=value



# ============================================================
# LOGIN UI
# ============================================================

def login_screen():


    st.title(
        "🔐 SAI AI Forex Login"
    )


    tab1,tab2=st.tabs(
        [
            "Login",
            "Register"
        ]
    )


    with tab1:


        user=st.text_input(
            "Username"
        )


        password=st.text_input(
            "Password",
            type="password"
        )


        if st.button("Login"):


            ok,role=authenticate(
                user,
                password
            )


            if ok:

                st.session_state.login=True

                st.session_state.username=user

                st.session_state.role=role

                st.rerun()


            else:

                st.error(
                    "Invalid login"
                )



    with tab2:


        new_user=st.text_input(
            "New username"
        )


        new_pass=st.text_input(
            "New password",
            type="password"
        )


        email=st.text_input(
            "Email"
        )


        if st.button(
            "Create account"
        ):


            if register(
                new_user,
                new_pass,
                email
            ):

                st.success(
                    "Account created"
                )

            else:

                st.error(
                    "Username already exists"
                )



if not st.session_state.login:

    login_screen()

    st.stop()


# ============================================================
# END PART 1
# ============================================================

# ============================================================
# MARKET ENGINE
# ============================================================


CURRENCIES = {

    "UGX":3800,
    "KES":130,
    "TZS":2600,
    "RWF":1350,
    "BIF":2900,
    "SSP":1600,
    "ETB":57,
    "USD":1,
    "EUR":0.92,
    "GBP":0.78,
    "JPY":145

}



def simulated_market():

    prices={}

    for currency,value in CURRENCIES.items():

        if currency=="USD":

            prices[currency]=1

        else:

            movement=random.uniform(
                -0.01,
                0.01
            )

            prices[currency]=round(
                value+(value*movement),
                2
            )

    return prices




@st.cache_data(
    ttl=10
)
def live_market():

    try:

        url=(
            "https://api.frankfurter.app/latest"
            "?from=USD&to=EUR,GBP,JPY"
        )


        response=requests.get(
            url,
            timeout=5
        )


        data=response.json()

        rates=data.get(
            "rates",
            {}
        )


        rates["USD"]=1


        local=simulated_market()


        for k,v in rates.items():

            local[k]=v


        return local


    except Exception:


        return simulated_market()




# ============================================================
# MARKET HISTORY DATABASE
# ============================================================


def save_market(prices):

    conn=db(TRADING_DB)


    for currency,rate in prices.items():

        conn.execute(
            """
            INSERT INTO market
            VALUES(
            NULL,?,?,?,?
            )
            """,
            (
                st.session_state.username,
                datetime.now().isoformat(),
                currency,
                rate
            )
        )


    conn.commit()
    conn.close()




def load_market(currency):

    conn=db(TRADING_DB)


    df=pd.read_sql(
        """
        SELECT time,rate
        FROM market
        WHERE username=?
        AND currency=?
        ORDER BY id
        """,
        conn,
        params=(
            st.session_state.username,
            currency
        )
    )


    conn.close()


    if not df.empty:

        df["time"]=pd.to_datetime(
            df["time"]
        )


    return df



# ============================================================
# AI SIGNAL ENGINE
# ============================================================


def moving_average(values,period):

    if len(values)<period:

        return None

    return np.mean(
        values[-period:]
    )




def calculate_rsi(values,period=14):

    if len(values)<=period:

        return 50


    delta=np.diff(values)


    gain=np.maximum(
        delta,
        0
    )


    loss=np.maximum(
        -delta,
        0
    )


    avg_gain=np.mean(
        gain[-period:]
    )


    avg_loss=np.mean(
        loss[-period:]
    )


    if avg_loss==0:

        return 100


    rs=avg_gain/avg_loss


    return (
        100 -
        (100/(1+rs))
    )




def ai_predict(currency):


    history=load_market(
        currency
    )


    if history.empty:

        return {

            "signal":"HOLD",
            "confidence":0,
            "forecast":None

        }



    prices=list(
        history.rate
    )


    current=prices[-1]


    sma20=moving_average(
        prices,
        20
    )


    sma50=moving_average(
        prices,
        50
    )


    rsi=calculate_rsi(
        prices
    )


    score=0


    if sma20 and sma50:


        if sma20>sma50:

            score+=40

        else:

            score-=40



    if rsi<30:

        score+=30


    elif rsi>70:

        score-=30



    score+=random.randint(
        -20,
        20
    )



    if score>30:

        action="BUY"


    elif score<-30:

        action="SELL"


    else:

        action="HOLD"



    confidence=min(
        abs(score),
        100
    )



    forecast=current*(

        1+
        random.uniform(
            -0.01,
            0.01
        )

    )


    return {

        "signal":action,

        "confidence":confidence,

        "forecast":round(
            forecast,
            2
        ),

        "rsi":round(
            rsi,
            2
        )

    }




# ============================================================
# AI MULTI CURRENCY ANALYSIS
# ============================================================


def run_ai_engine(prices):


    results={}


    for currency in prices:

        results[currency]=ai_predict(
            currency
        )


    return results



# ============================================================
# FORECAST ENGINE
# ============================================================


def simple_forecast(currency,days=7):


    history=load_market(
        currency
    )


    if history.empty:

        return []


    last=float(
        history.rate.iloc[-1]
    )


    forecast=[]


    for i in range(days):


        change=random.uniform(
            -0.005,
            0.005
        )


        last=last*(1+change)


        forecast.append(
            round(last,2)
        )


    return forecast



# ============================================================
# END PART 2
# ============================================================

# ============================================================
# ACCOUNT ENGINE
# ============================================================


def load_account():

    conn=db(TRADING_DB)


    row=conn.execute(
        """
        SELECT balance,equity
        FROM account
        WHERE username=?
        """,
        (
            st.session_state.username,
        )
    ).fetchone()


    conn.close()


    if row:

        return {

            "balance":row[0],
            "equity":row[1]

        }


    return {

        "balance":10000.0,
        "equity":10000.0

    }




def save_account(balance,equity):


    conn=db(TRADING_DB)


    conn.execute(
        """
        INSERT OR REPLACE INTO account
        VALUES(?,?,?)
        """,
        (
            st.session_state.username,
            balance,
            equity
        )
    )


    conn.commit()
    conn.close()



# ============================================================
# TRADING ENGINE
# ============================================================


def execute_trade(symbol,action,price):


    account=load_account()


    pnl=random.uniform(
        -100,
        200
    )


    if action=="SELL":

        pnl=-pnl



    new_balance=(

        account["balance"]
        +
        pnl

    )


    save_account(
        new_balance,
        new_balance
    )



    conn=db(TRADING_DB)


    conn.execute(
        """
        INSERT INTO trades
        VALUES(NULL,?,?,?,?,?,?)
        """,
        (
            st.session_state.username,

            datetime.now().isoformat(),

            symbol,

            action,

            price,

            pnl
        )
    )


    conn.commit()

    conn.close()



    st.session_state.balance=new_balance



    return pnl




def trade_history():

    conn=db(TRADING_DB)


    df=pd.read_sql(
        """
        SELECT *
        FROM trades
        WHERE username=?
        ORDER BY id DESC
        """,
        conn,
        params=[
            st.session_state.username
        ]
    )


    conn.close()


    return df




# ============================================================
# RISK MANAGEMENT
# ============================================================


def position_size(balance,risk):


    amount=(

        balance*
        risk/100

    )


    return round(
        amount,
        2
    )




# ============================================================
# AUTONOMOUS BOT LOOP
# ============================================================


def bot_worker(stop_event):


    while not stop_event.is_set():


        try:


            prices=live_market()


            save_market(
                prices
            )


            ai=run_ai_engine(
                prices
            )



            for currency,data in ai.items():


                if data["signal"]!="HOLD":


                    signal={

                        "currency":currency,

                        "action":data["signal"],

                        "confidence":data["confidence"],

                        "price":prices[currency],

                        "time":datetime.now()

                    }


                    st.session_state.bot_queue.put(
                        signal
                    )



                    if st.session_state.auto_trade:


                        execute_trade(

                            currency,

                            data["signal"],

                            prices[currency]

                        )



        except Exception as e:


            logger.error(
                str(e)
            )



        time.sleep(10)




def start_bot():


    if st.session_state.bot_running:

        return



    stop_event=threading.Event()


    thread=threading.Thread(

        target=bot_worker,

        args=(stop_event,),

        daemon=True

    )


    st.session_state.stop=stop_event

    st.session_state.thread=thread

    st.session_state.bot_running=True


    thread.start()





def stop_bot():


    if st.session_state.stop:


        st.session_state.stop.set()



    st.session_state.bot_running=False





# ============================================================
# QUEUE READER
# ============================================================


def get_signals():


    signals=[]


    while not st.session_state.bot_queue.empty():


        signals.append(

            st.session_state.bot_queue.get()

        )


    return signals



# ============================================================
# INITIAL MARKET LOAD
# ============================================================


prices=live_market()


save_market(
    prices
)


account=load_account()


st.session_state.balance=account["balance"]



# ============================================================
# END PART 3
# ============================================================

# ============================================================
# PART 4 - STREAMLIT DASHBOARD UI
# ============================================================


# ============================================================
# SIDEBAR CONTROL PANEL
# ============================================================

with st.sidebar:


    st.title("⚙️ SAI Control Center")


    st.write(
        f"👤 {st.session_state.username}"
    )


    st.write(
        f"Role: {st.session_state.role}"
    )


    st.divider()



    st.session_state.risk = st.slider(

        "Risk Level %",

        1,

        20,

        st.session_state.risk

    )



    st.session_state.auto_trade = st.checkbox(

        "Enable AI Auto Trading",

        value=st.session_state.auto_trade

    )



    if st.button(
        "▶ Start AI Bot"
    ):

        start_bot()



    if st.button(
        "⏹ Stop AI Bot"
    ):

        stop_bot()



    st.divider()



    if st.session_state.role=="admin":


        st.subheader(
            "👥 Users"
        )


        st.dataframe(
            users(),
            hide_index=True
        )



    if st.button(
        "🚪 Logout"
    ):

        st.session_state.clear()

        st.rerun()





# ============================================================
# HEADER
# ============================================================


st.title(
    "📈 SAI Autonomous Forex Intelligence"
)


st.caption(
    "East Africa AI Market Analysis System"
)



# ============================================================
# TOP METRICS
# ============================================================


account=load_account()


m1,m2,m3,m4=st.columns(4)



m1.metric(

    "Balance",

    f"${account['balance']:,.2f}"

)


m2.metric(

    "Bot Status",

    "RUNNING"
    if st.session_state.bot_running
    else
    "STOPPED"

)


m3.metric(

    "Risk",

    f"{st.session_state.risk}%"

)


m4.metric(

    "Currency Models",

    len(CURRENCIES)

)




# ============================================================
# DASHBOARD TABS
# ============================================================


tabs=st.tabs(

    [

        "🌍 Market",

        "🧠 AI Brain",

        "📊 Forecast",

        "💹 Trading",

        "📜 History",

        "⚙ System"

    ]

)



# ============================================================
# MARKET TAB
# ============================================================

with tabs[0]:


    st.subheader(
        "🌍 Live Currency Market"
    )


    prices=live_market()


    save_market(
        prices
    )



    df=pd.DataFrame(

        {

        "Currency":prices.keys(),

        "Rate":prices.values()

        }

    )


    if PLOTLY:


        fig=go.Figure()


        fig.add_trace(

            go.Bar(

                x=df["Currency"],

                y=df["Rate"]

            )

        )


        st.plotly_chart(

            fig,

            use_container_width=True

        )


    else:

        st.bar_chart(

            df.set_index(
                "Currency"
            )

        )





    cols=st.columns(4)



    for index,(cur,rate) in enumerate(prices.items()):


        with cols[index%4]:


            st.metric(

                cur,

                rate

            )




# ============================================================
# AI BRAIN TAB
# ============================================================

with tabs[1]:


    st.subheader(
        "🧠 SAI AI Decision Engine"
    )


    prices=live_market()


    ai_results=run_ai_engine(
        prices
    )


    rows=[]


    for cur,result in ai_results.items():


        rows.append(

            {

            "Currency":cur,

            "Signal":result["signal"],

            "Confidence":
            f"{result['confidence']}%",

            "RSI":
            result.get("rsi",0),

            "Forecast":
            result["forecast"]

            }

        )


    ai_df=pd.DataFrame(rows)


    st.dataframe(

        ai_df,

        use_container_width=True

    )



    for row in rows:


        if row["Signal"]=="BUY":

            st.success(

                f"🟢 BUY {row['Currency']}"

            )


        elif row["Signal"]=="SELL":

            st.error(

                f"🔴 SELL {row['Currency']}"

            )





# ============================================================
# FORECAST TAB
# ============================================================

with tabs[2]:


    st.subheader(
        "🔮 AI Forecast Engine"
    )


    currency=st.selectbox(

        "Select Currency",

        list(CURRENCIES.keys())

    )


    days=st.slider(

        "Forecast Days",

        1,

        30,

        7

    )



    forecast=simple_forecast(

        currency,

        days

    )



    forecast_df=pd.DataFrame(

        {

        "Day":
        range(1,days+1),

        "Forecast":
        forecast

        }

    )


    st.line_chart(

        forecast_df.set_index(
            "Day"
        )

    )



    st.dataframe(

        forecast_df,

        hide_index=True

    )





# ============================================================
# TRADING TAB
# ============================================================

with tabs[3]:


    st.subheader(
        "💹 Manual AI Trading"
    )


    symbol=st.selectbox(

        "Currency",

        list(CURRENCIES.keys())

    )



    action=st.selectbox(

        "Action",

        [

        "BUY",

        "SELL"

        ]

    )



    price=live_market()[symbol]



    st.write(

        "Current Price:",

        price

    )



    if st.button(
        "Execute Trade"
    ):


        pnl=execute_trade(

            symbol,

            action,

            price

        )


        st.success(

            f"Trade executed PnL ${pnl:.2f}"

        )




# ============================================================
# HISTORY TAB
# ============================================================

with tabs[4]:


    st.subheader(
        "📜 Trading History"
    )


    history=trade_history()



    st.dataframe(

        history,

        use_container_width=True

    )



    if not history.empty:


        st.metric(

            "Total Trades",

            len(history)

        )


        st.metric(

            "Total PnL",

            f"${history.pnl.sum():.2f}"

        )





# ============================================================
# SYSTEM TAB
# ============================================================

with tabs[5]:


    st.subheader(
        "⚙ System Information"
    )


    st.write(

        {

        "Version":
        "SAI AI Forex Bot v5.0",

        "Engine":
        "Streamlit Single File",

        "Database":
        "SQLite",

        "AI":
        "Signal + Forecast Engine",

        "Region":
        "East Africa"

        }

    )



# ============================================================
# FOOTER
# ============================================================


st.divider()


st.caption(

    "SAI AI Forex Intelligence v5.0 | Autonomous Trading Simulation"

)

