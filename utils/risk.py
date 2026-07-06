def calculate_position_size(equity, risk_pct, entry, stop_loss, pair_rate):
    risk_amount = equity * (risk_pct / 100.0)
    stop_distance = abs(entry - stop_loss)
    if stop_distance == 0 or pair_rate == 0:
        return 0.0
    stop_loss_usd = stop_distance / pair_rate
    units = risk_amount / stop_loss_usd
    return round(units, 2)
