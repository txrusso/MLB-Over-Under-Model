import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

"""

This is a helper script to make model notebooks cleaner

Script to:
1. Build MLB totals bets from model predictions
2. Calculate per-bet profit/loss in units
3. Plot cumulative returns over time
4. Output ROI
Notes:
- A push occurs when actual_total == vegas_line
- ROI = total_profit / total_amount_risked
- Default stake is 1 unit per bet
"""

def american_odds_profit(stake, odds):
    # Return profit (not including wagered amount) for a winning bet.
    odds = float(odds)
    if odds > 0:
        return stake * (odds / 100)
    return stake * (100.0 / abs(odds))

def prepare_bets(df, threshold=0.5, stake=1.0) -> pd.DataFrame:
    bets = df.copy()
    bets["game_date"] = pd.to_datetime(bets["game_date"])
    bets = bets.sort_values("game_date").reset_index(drop=True)
    bets["edge"] = bets["pred_total"] - bets["vegas_line"]
    bets["bet"] = np.where(
        bets["edge"] > threshold, "over",
        np.where(bets["edge"] < -threshold, "under", "no_bet")
    )
    bets = bets[bets["bet"] != "no_bet"].copy()
    bets["odds"] = np.where(bets["bet"] == "over", bets["over_odds"], bets["under_odds"])
    bets["actual_side"] = np.where(
        bets["actual_total"] > bets["vegas_line"],
        "over",
        np.where(bets["actual_total"] < bets["vegas_line"], "under", "push"))
    bets["stake"] = stake

    def settle_bet(row):
        if row["actual_side"] == "push":
            return 0.0
        if row["bet"] == row["actual_side"]:
            return american_odds_profit(row["stake"], row["odds"])
        return -row["stake"]

    bets["profit"] = bets.apply(settle_bet, axis=1)
    bets["risked"] = np.where(bets["actual_side"] == "push", 0.0, bets["stake"])
    bets["cumulative_profit"] = bets["profit"].cumsum()
    return bets

def plot_returns(bets):
    plt.figure(figsize=(10, 6))
    plt.plot(bets["game_date"], bets["cumulative_profit"])
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return (Units)")
    plt.title("Cumulative Betting Returns Over Time")
    plt.xticks(rotation=45)
    plt.tight_layout()

def summarize_results(bets):
    total_profit = float(bets["profit"].sum())
    total_risked = float(bets["risked"].sum())
    wins = int((bets["profit"] > 0).sum())
    losses = int((bets["profit"] < 0).sum())
    
    return {
        "num_bets": int(len(bets)),
        "wins": wins,
        "losses": losses,
        "pushes": int((bets["actual_side"] == "push").sum()),
        "total_profit_units": total_profit,
        "total_risked_units": total_risked,
        "roi": total_profit / total_risked,
        "win_rate": wins / (wins + losses)
    }