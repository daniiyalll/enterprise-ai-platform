"""
Prepare ML Dataset - Enterprise AI Platform (ML-048)
Transforms workflow_events.csv (raw event log) into a case-level dataset
suitable for training the WorkflowRiskModel (app/ai/prediction_model.py).

Each row = one workflow case (request), with numeric features and a
"risk" label (1 = case was Rejected, 0 = case was Approved).

Run: python prepare_ml_dataset.py
Output: workflow_risk_dataset.csv
"""

import pandas as pd

INPUT_CSV = "workflow_events.csv"
OUTPUT_CSV = "workflow_risk_dataset.csv"


def build_risk_dataset(input_csv: str) -> pd.DataFrame:
    df = pd.read_csv(input_csv)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    rows = []
    for case_id, group in df.groupby("case_id"):
        group = group.sort_values("timestamp")

        process_type = group["process_type"].iloc[0]
        department = group["department"].iloc[0]
        activities = group["activity"].tolist()

        num_steps = len(activities)
        duration_hours = (group["timestamp"].max() - group["timestamp"].min()).total_seconds() / 3600
        had_manager_approval = int("Manager Approval" in activities)
        had_compliance_check = int("Compliance Check" in activities)
        final_activity = activities[-1]
        risk = 1 if final_activity == "Rejected" else 0

        rows.append({
            "process_type": process_type,
            "department": department,
            "num_steps": num_steps,
            "duration_hours": round(duration_hours, 2),
            "had_manager_approval": had_manager_approval,
            "had_compliance_check": had_compliance_check,
            "risk": risk,
        })

    result = pd.DataFrame(rows)

    # Encode categorical columns as numbers (RandomForestClassifier needs numeric input)
    result["process_type"] = result["process_type"].astype("category").cat.codes
    result["department"] = result["department"].astype("category").cat.codes

    return result


if __name__ == "__main__":
    dataset = build_risk_dataset(INPUT_CSV)
    dataset.to_csv(OUTPUT_CSV, index=False)
    print(f"Built dataset with {len(dataset)} rows -> {OUTPUT_CSV}")
    print(f"Risk distribution:\n{dataset['risk'].value_counts()}")
    print(f"\nSample rows:\n{dataset.head()}")
