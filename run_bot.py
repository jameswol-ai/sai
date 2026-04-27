# run_bot.py
"""
Standalone runner for the SAI trading bot.
Provides CLI flags for status, sandbox, and live trading.
"""

import argparse
from sai.bot.main import run_bot

def main():
    parser = argparse.ArgumentParser(
        description="Run the SAI trading bot with configurable modes."
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Print bot status without running trades."
    )
    parser.add_argument(
        "--sandbox",
        action="store_true",
        help="Run trades in sandbox mode (no real execution)."
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Run trades in live mode (real execution)."
    )

    args = parser.parse_args()

    if args.status:
        print("SAI Bot Status: Ready ✅")
        # You could expand this to show configs, model info, etc.
    elif args.sandbox:
        print("Starting SAI bot in sandbox mode...")
        run_bot(mode="sandbox")
    elif args.live:
        print("Starting SAI bot in LIVE mode ⚡")
        run_bot(mode="live")
    else:
        print("No mode specified. Use --status, --sandbox, or --live.")

if __name__ == "__main__":
    main()
