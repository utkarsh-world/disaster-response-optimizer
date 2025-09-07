# relief_optimizer_test.py
# ============================================================
# Quick CLI test for relief allocation logic (bilingual output)
# ============================================================

from relief_optimizer import optimize_relief_allocation

INPUT_FILE = "data/clean/flood_cleaned.csv"   # India dataset
OUTPUT_FILE = "data/clean/relief_allocation_2019_2023.csv"
BUDGET = 3000   # total relief units to distribute

if __name__ == "__main__":
    result = optimize_relief_allocation(INPUT_FILE, BUDGET, OUTPUT_FILE)

    print("\n=== Relief Allocation Optimizer / 救援配分最適化 ===")
    print(f"Total Budget: {BUDGET} units / 総予算: {BUDGET} ユニット\n")

    print(f"{'State':<20} {'Impact':<10} {'Allocated':<10} {'%':<6} | "
          f"{'州':<10} {'影響度':<10} {'割当':<10} {'割合 %':<6}")
    print("-" * 80)

    for _, row in result.iterrows():
        print(f"{row['state']:<20} {row['impact_score']:<10.0f} "
              f"{row['allocated']:<10.0f} {row['percent']:<6.1f} | "
              f"{row['state']:<10} {row['impact_score']:<10.0f} "
              f"{row['allocated']:<10.0f} {row['percent']:<6.1f}")

    print(f"\nSaved allocation table → {OUTPUT_FILE}")
