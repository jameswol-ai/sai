# bot/main.py

import argparse
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

def run_bot(mode: str):
    """
    Core bot logic placeholder.
    Replace this with your actual implementation.
    """
    logging.info("Bot started in '%s' mode.", mode)

    # Example logic
    if mode == "demo":
        logging.info("Running demo mode...")
        print("✅ Bot is running successfully in demo mode!")
    else:
        logging.warning("Unknown mode provided. Defaulting to demo.")
        print("⚠️ Running default demo mode.")

def main():
    parser = argparse.ArgumentParser(description="Run the bot.")
    parser.add_argument(
        "--mode",
        type=str,
        default="demo",
        help="Mode to run the bot (e.g., demo, production, test)."
    )
    args = parser.parse_args()

    run_bot(args.mode)

if __name__ == "__main__":
    main()
