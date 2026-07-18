# ============================================================
# SAI AI Forex Bot v5.0
# Unified Single File Streamlit Edition
# Login + Database + AI Trading Core
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
import requests
from pathlib import Path
from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler

import pandas as pd
import numpy as np

try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except Exception:
    PLOTLY_AVAILABLE = False


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
    handlers=[
        RotatingFileHandler(
            "sai_app.log",
            maxBytes=5_000_000,
            backupCount=3
        )
    ],
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger("SAI")



# ============================================================
# DATABASE CORE
# ============================================================

def database(path):

    return sqlite3.connect(
        path,
        check_same_thread=False
    )



def password_hash(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()



def initialize_database():


    # USERS

    conn = database(USER_DB)

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
                password_hash("admin123"),
                "admin",
                "admin@sai.ai"
            )
        )


    conn.commit()
    conn.close()



    # TRADING DATABASE

    conn = database(TRADING_DB)


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


    CREATE TABLE IF NOT EXISTS balance(

        username TEXT PRIMARY KEY,
        amount REAL

    );


    CREATE TABLE IF NOT EXISTS orders(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        time TEXT,
        symbol TEXT,
        units INTEGER,
        action TEXT,
        price REAL,
        status TEXT

    );


    CREATE TABLE IF NOT EXISTS logs(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        time TEXT,
        message TEXT

    );


    """)


    conn.commit()
    conn.close()



initialize_database()



# ============================================================
# USER MANAGEMENT
# ============================================================


def authenticate(username,password):

    conn = database(USER_DB)

    row = conn.execute(
        """
        SELECT role
        FROM users
        WHERE username=?
        AND password=?
        """,
        (
            username,
            password_hash(password)
        )
    ).fetchone()


    conn.close()


    if row:

        return True,row[0]


    return False,None




def register(username,password,email=""):


    try:

        conn=database(USER_DB)


        conn.execute(
            """
            INSERT INTO users
            VALUES(?,?,?,?)
            """,
            (
                username,
                password_hash(password),
                "user",
                email
            )
        )


        conn.commit()
        conn.close()


        return True


    except Exception:

        return False




def users_list():

    conn=database(USER_DB)

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

    conn=database(USER_DB)

    conn.execute(
        "DELETE FROM users WHERE username=?",
        (username,)
    )

    conn.commit()
    conn.close()



# ============================================================
# SESSION ENGINE
# ============================================================


SESSION_DEFAULTS={


"logged":False,

"username":"",

"role":"",

"balance":10000.0,

"bot_running":False,

"auto_trade":False,

"risk":5,

"history":[],

"signals":[],

"logs":[],

"queue":queue.Queue(),

"thread":None,

"stop_event":None


}



for key,value in SESSION_DEFAULTS.items():

    if key not in st.session_state:

        st.session_state[key]=value



# ============================================================
# LOGIN UI
# ============================================================


def login_screen():


    st.title(
        "🔐 SAI AI Forex Intelligence"
    )


    tab1,tab2=st.tabs(
        [
            "Login",
            "Register"
        ]
    )


    with tab1:


        username=st.text_input(
            "Username"
        )


        password=st.text_input(
            "Password",
            type="password"
        )


        if st.button(
            "Login"
        ):


            ok,role=authenticate(
                username,
                password
            )


            if ok:


                st.session_state.logged=True

                st.session_state.username=username

                st.session_state.role=role

                st.rerun()


            else:

                st.error(
                    "Invalid login"
                )



    with tab2:


        username=st.text_input(
            "New Username"
        )


        password=st.text_input(
            "New Password",
            type="password"
        )


        email=st.text_input(
            "Email"
        )


        if st.button(
            "Create Account"
        ):


            if register(
                username,
                password,
                email
            ):

                st.success(
                    "Account created"
                )

            else:

                st.error(
                    "Username already exists"
                )




if not st.session_state.logged:

    login_screen()

    st.stop()



# ============================================================
# LOGOUT
# ============================================================


def logout():

    st.session_state.clear()

    st.rerun()