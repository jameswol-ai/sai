# ============================================================
# MARKET ENGINE
# ============================================================

EAST_AFRICA = {

    "UGX":3800,
    "KES":130,
    "TZS":2600,
    "RWF":1350,
    "BIF":2900,
    "SSP":1600,
    "ETB":56

}


GLOBAL = {

    "USD":1,
    "EUR":0.92,
    "GBP":0.78,
    "JPY":145

}



ALL_MARKETS = {
    **EAST_AFRICA,
    **GLOBAL
}



def generate_market():

    prices={}


    for symbol,value in ALL_MARKETS.items():

        movement=random.uniform(
            -0.5,
            0.5
        )


        prices[symbol]=round(
            value+movement,
            4
        )


    return prices



# ============================================================
# PRICE HISTORY ENGINE
# ============================================================


def save_price_history(prices):

    user=st.session_state.username


    conn=database(TRADING_DB)


    for symbol,value in prices.items():

        conn.execute(
            """
            INSERT INTO trades
            (
            username,
            time,
            symbol,
            action,
            price,
            pnl
            )

            VALUES(?,?,?,?,?,?)
            """,
            (
                user,
                datetime.now().isoformat(),
                symbol,
                "MARKET",
                value,
                0
            )
        )


    conn.commit()

    conn.close()



# ============================================================
# AI SIGNAL ENGINE
# ============================================================


def ai_prediction():

    confidence=random.randint(
        50,
        99
    )


    score=random.randint(
        -100,
        100
    )


    if score > 35:

        decision="BUY"


    elif score < -35:

        decision="SELL"


    else:

        decision="HOLD"



    return {

        "signal":decision,

        "confidence":confidence,

        "score":score

    }




# ============================================================
# TECHNICAL INDICATORS
# ============================================================


def calculate_rsi(series,period=14):


    delta=series.diff()


    gain=delta.clip(
        lower=0
    )


    loss=-delta.clip(
        upper=0
    )


    avg_gain=gain.mean()

    avg_loss=loss.mean()


    if avg_loss==0:

        return 100


    rs=avg_gain/avg_loss


    return round(
        100-(100/(1+rs)),
        2
    )




def moving_average(series,period):

    return series.rolling(
        period
    ).mean()




# ============================================================
# FORECAST ENGINE
# ============================================================


def forecast_price(history):


    if len(history)<5:

        return None



    values=np.array(
        history
    )


    trend=np.polyfit(
        range(len(values)),
        values,
        1
    )


    future=np.polyval(
        trend,
        len(values)+1
    )


    return round(
        float(future),
        4
    )



# ============================================================
# AI TRADING LOGIC
# ============================================================


def create_trade(symbol,action,price):


    pnl=random.uniform(
        -100,
        250
    )


    user=st.session_state.username



    conn=database(TRADING_DB)



    conn.execute(
        """
        INSERT INTO trades
        (
        username,
        time,
        symbol,
        action,
        price,
        pnl
        )

        VALUES(?,?,?,?,?,?)
        """,
        (

            user,

            datetime.now().isoformat(),

            symbol,

            action,

            price,

            pnl

        )
    )



    conn.execute(
        """
        INSERT OR REPLACE INTO balance
        VALUES(?,?)
        """,
        (

        user,

        st.session_state.balance+pnl

        )
    )


    conn.commit()

    conn.close()



    st.session_state.balance += pnl



# ============================================================
# TRADING ACCOUNT
# ============================================================


def load_balance():


    conn=database(TRADING_DB)


    row=conn.execute(
        """
        SELECT amount
        FROM balance
        WHERE username=?
        """,
        (
            st.session_state.username,
        )
    ).fetchone()


    conn.close()



    if row:

        return row[0]


    return 10000.0




st.session_state.balance = load_balance()



# ============================================================
# BOT AUTONOMOUS LOOP
# ============================================================


def bot_worker():


    while not st.session_state.stop_event.is_set():


        prices=generate_market()


        brain=ai_prediction()



        if brain["signal"]!="HOLD":


            st.session_state.queue.put(

                {

                "symbol":"UGX",

                "action":brain["signal"],

                "price":prices["UGX"],

                "confidence":brain["confidence"]

                }

            )


        time.sleep(5)





def start_bot():


    if st.session_state.bot_running:

        return



    st.session_state.stop_event=threading.Event()



    thread=threading.Thread(

        target=bot_worker,

        daemon=True

    )


    st.session_state.thread=thread


    st.session_state.bot_running=True


    thread.start()





def stop_bot():


    if st.session_state.bot_running:


        st.session_state.stop_event.set()


        st.session_state.bot_running=False



# ============================================================
# LOAD TRADE HISTORY
# ============================================================


def trade_history():


    conn=database(TRADING_DB)



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
# TELEGRAM ALERT SUPPORT
# ============================================================


def send_alert(message):

    try:

        token=st.secrets.get(
            "TELEGRAM_TOKEN"
        )


        chat=st.secrets.get(
            "TELEGRAM_CHAT_ID"
        )


        if token and chat:


            requests.post(

                f"https://api.telegram.org/bot{token}/sendMessage",

                json={

                "chat_id":chat,

                "text":message

                }

            )


    except Exception as e:

        logger.error(e)