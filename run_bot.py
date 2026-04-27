# run_bot.py
"""
Standalone runner for the SAI trading bot.
Provides CLI flags for status, sandbox, live trading, and config loading.
"""

import argparse
import yaml
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
    parser.add_argument(
        "--config",
        type=str,
        help="Path to YAML/JSON config file (e.g., configs/dev.yaml)."
    )

    args = parser.parse_args()

    # Load config if provided
    config = None
    if args.config:
        print(f"Loading config from {args.config}...")
        if args.config.endswith(".yaml") or args.config.endswith(".yml"):
            with open(args.config, "r") as f:
                config = yaml.safe_load(f)
        elif args.config.endswith(".json"):
            import json
            with open(args.config, "r") as f:
                config = json.load(f)
        else:
            print("Unsupported config format. Use YAML or JSON.")

    # Handle modes
    if args.status:
        print("SAI Bot Status: Ready ✅")
        if config:
            print("Loaded Config Keys:", list(config.keys()))
    elif args.sandbox:
        print("Starting SAI bot in sandbox mode...")
        run_bot(mode="sandbox", config=config)
    elif args.live:
        print("Starting SAI bot in LIVE mode ⚡")
        run_bot(mode="live", config=config)
    else:
        print("No mode specified. Use --status, --sandbox, or --live.")

if __name__ == "__main__":
    main()
