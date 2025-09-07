# relief_optimizer.py
# ============================================================
# Relief Allocation Logic (Reusable for CLI + Streamlit)
# 災害救援資源配分ロジック（CLI と Streamlit 共通利用）
# ============================================================

import pandas as pd


# ------------------------------------------------------------
# 1. Optimize Relief Allocation (India dataset CSV)
# ------------------------------------------------------------
def optimize_relief_allocation(input_csv: str, budget: int, output_csv: str = None) -> pd.DataFrame:
    """
    Allocate relief resources proportionally to impact score.

    Args:
        input_csv (str): Path to cleaned flood dataset (must include 'state' & 'human_fatality').
        budget (int): Total relief units available.
        output_csv (str, optional): Save results to CSV if provided.

    Returns:
        pd.DataFrame: Allocation results with columns:
            state, impact_score, allocated, percent
    """
    df = pd.read_csv(input_csv)

    # Impact score = fatalities + (optional) economic loss
    df["impact_score"] = df["human_fatality"] + df.get("economic_loss", 0)

    total_score = df["impact_score"].sum()

    if total_score == 0:
        df["allocated"] = 0
        df["percent"] = 0
    else:
        df["allocated"] = (df["impact_score"] / total_score * budget).round().astype(int)
        df["percent"] = (df["allocated"] / budget * 100).round(1)

    result = df[["state", "impact_score", "allocated", "percent"]]

    if output_csv:
        result.to_csv(output_csv, index=False)

    return result


# ------------------------------------------------------------
# 2. Allocate Relief (filtered by year range, dynamic)
# ------------------------------------------------------------
def allocate_relief(df: pd.DataFrame, start_year: int, end_year: int, total_resources: int) -> pd.DataFrame:
    """
    Allocate resources based on fatalities across selected years.

    Args:
        df (pd.DataFrame): Flood dataset (must include 'year', 'state', 'human_fatality').
        start_year (int): Start year of filter.
        end_year (int): End year of filter.
        total_resources (int): Relief units to distribute.

    Returns:
        pd.DataFrame: Allocation results with columns:
            state, need_units, allocated_units
    """
    df_filtered = df[(df["year"] >= start_year) & (df["year"] <= end_year)].copy()

    if "human_fatality" not in df_filtered.columns or df_filtered.empty:
        return pd.DataFrame()

    state_needs = (
        df_filtered.groupby("state")["human_fatality"]
        .sum()
        .reset_index()
        .rename(columns={"human_fatality": "need_units"})
    )

    total_need = state_needs["need_units"].sum()
    if total_need == 0:
        state_needs["allocated_units"] = 0
    else:
        state_needs["allocated_units"] = (
            state_needs["need_units"] / total_need * total_resources
        ).round().astype(int)

    return state_needs.sort_values("allocated_units", ascending=False).reset_index(drop=True)
