"""
Process Mining Service - Enterprise AI Platform (ML-048)
Uses PM4Py to discover the actual process flow from workflow_events.csv,
find common paths, bottlenecks, and process variants.
"""

import pandas as pd
import pm4py


def load_event_log(csv_path: str):
    """
    Loads workflow_events.csv and converts it into a PM4Py-compatible event log.
    Expected columns: case_id, activity, timestamp (plus any extra columns).
    """
    df = pd.read_csv(csv_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    df = df.rename(columns={
        "case_id": "case:concept:name",
        "activity": "concept:name",
        "timestamp": "time:timestamp",
    })

    event_log = pm4py.format_dataframe(
        df,
        case_id="case:concept:name",
        activity_key="concept:name",
        timestamp_key="time:timestamp",
    )
    return event_log


def discover_process_map(csv_path: str):
    """
    Discovers the process map (directly-follows graph) from the event log.
    Returns basic stats: number of cases, activities, and the most frequent paths.
    """
    log = load_event_log(csv_path)

    num_cases = log["case:concept:name"].nunique()
    activities = log["concept:name"].unique().tolist()

    dfg, start_activities, end_activities = pm4py.discover_dfg(log)

    top_transitions = sorted(dfg.items(), key=lambda x: x[1], reverse=True)[:10]

    return {
        "total_cases": num_cases,
        "activities": activities,
        "start_activities": start_activities,
        "end_activities": end_activities,
        "top_transitions": [
            {"from": a, "to": b, "count": count}
            for (a, b), count in top_transitions
        ],
    }


def find_bottlenecks(csv_path: str, top_n: int = 5):
    """
    Calculates average time spent between consecutive activities per case,
    to highlight which transitions take the longest (likely bottlenecks).
    """
    df = pd.read_csv(csv_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values(["case_id", "timestamp"])

    df["next_activity"] = df.groupby("case_id")["activity"].shift(-1)
    df["next_timestamp"] = df.groupby("case_id")["timestamp"].shift(-1)
    df["duration_hours"] = (df["next_timestamp"] - df["timestamp"]).dt.total_seconds() / 3600

    transition_durations = (
        df.dropna(subset=["next_activity"])
        .groupby(["activity", "next_activity"])["duration_hours"]
        .mean()
        .sort_values(ascending=False)
        .head(top_n)
    )

    return [
        {"from": a, "to": b, "avg_hours": round(hours, 2)}
        for (a, b), hours in transition_durations.items()
    ]


def get_case_performance(csv_path: str):
    """
    Computes per-case duration and activity-count stats — how long a typical
    case takes end-to-end, and how much variation there is across cases.
    """
    df = pd.read_csv(csv_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    case_stats = df.groupby("case_id").agg(
        start=("timestamp", "min"),
        end=("timestamp", "max"),
        num_activities=("activity", "count"),
    )
    case_stats["duration_hours"] = (
        (case_stats["end"] - case_stats["start"]).dt.total_seconds() / 3600
    )

    return {
        "total_cases": int(case_stats.shape[0]),
        "avg_case_duration_hours": round(case_stats["duration_hours"].mean(), 2),
        "min_case_duration_hours": round(case_stats["duration_hours"].min(), 2),
        "max_case_duration_hours": round(case_stats["duration_hours"].max(), 2),
        "avg_activities_per_case": round(case_stats["num_activities"].mean(), 2),
    }


def get_frequent_paths(csv_path: str, top_n: int = 5):
    """
    Ranks each case's full activity sequence (its 'variant') by how often
    that exact path occurs — the most common ways a case actually flows.
    """
    df = pd.read_csv(csv_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values(["case_id", "timestamp"])

    variants = (
        df.groupby("case_id")["activity"]
        .apply(lambda acts: " -> ".join(acts))
    )

    variant_counts = variants.value_counts().head(top_n)

    return [
        {"path": path, "case_count": int(count)}
        for path, count in variant_counts.items()
    ]


def get_summary_report(csv_path: str):
    """
    One-call summary combining process discovery, bottlenecks, case
    performance, and the most frequent paths — meant to back a single
    dashboard-style "process mining summary" endpoint.
    """
    process_map = discover_process_map(csv_path)
    bottlenecks = find_bottlenecks(csv_path)
    performance = get_case_performance(csv_path)
    frequent_paths = get_frequent_paths(csv_path)

    return {
        "total_cases": process_map["total_cases"],
        "activities": process_map["activities"],
        "performance": performance,
        "top_bottlenecks": bottlenecks,
        "frequent_paths": frequent_paths,
        "start_activities": process_map["start_activities"],
        "end_activities": process_map["end_activities"],
    }


if __name__ == "__main__":
    result = discover_process_map("workflow_events.csv")
    print("Total cases:", result["total_cases"])
    print("Activities:", result["activities"])
    print("\nTop transitions:")
    for t in result["top_transitions"]:
        print(f"  {t['from']} -> {t['to']}  ({t['count']} times)")

    print("\nBottlenecks (slowest transitions):")
    for b in find_bottlenecks("workflow_events.csv"):
        print(f"  {b['from']} -> {b['to']}  (avg {b['avg_hours']} hours)")
