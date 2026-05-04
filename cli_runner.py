def run_dual_dashboard(window=5, refresh=30):
    """Continuously refresh summary stats in terminal + save plot to PNG."""
    while True:
        os.system("clear")
        print("=== Sai Dual-Pane Dashboard ===")
        show_summary()

        # Save plot instead of showing
        if os.path.isfile(CSV_FILE):
            filename = f"profits_plot_window{window}.png"
            with open(CSV_FILE, newline="") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            if rows:
                timestamps = [r["timestamp"] for r in rows if "timestamp" in r]
                profits = [float(r["profit"]) for r in rows if "profit" in r and r["profit"]]
                avg_profits = rolling_average(profits, window=window)

                plt.figure(figsize=(8,4))
                plt.plot(timestamps, profits, marker="o", linestyle="-", color="blue", label="Profit")
                plt.plot(timestamps, avg_profits, linestyle="--", color="red", label=f"Rolling Avg ({window})")
                plt.title("Sai Trading Profits Over Time")
                plt.xlabel("Timestamp")
                plt.ylabel("Profit")
                plt.xticks(rotation=45)
                plt.legend()
                plt.tight_layout()
                plt.savefig(filename)
                plt.close()
                print(f"Plot saved as {filename}")

        print(f"Refreshing in {refresh} seconds...")
        time.sleep(refresh)

# Add to argparse section:
parser.add_argument("--dual-dashboard", action="store_true", help="Live summary in terminal + plot saved to PNG")

# In main:
elif args.dual_dashboard:
    run_dual_dashboard(window=args.window, refresh=args.refresh)
