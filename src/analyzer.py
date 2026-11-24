import pandas as pd


class Analyzer:
    """Считает метрики. Никакой отрисовки."""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def status_by_project(self) -> pd.DataFrame:
        return pd.crosstab(self.df["project_name"], self.df["status"])

    def priority_by_project(self) -> pd.DataFrame:
        return pd.crosstab(self.df["project_name"], self.df["priority"])

    def risk_by_project(self) -> pd.DataFrame:
        return pd.crosstab(self.df["project_name"], self.df["risk_level"])

    def github_stats(self) -> pd.DataFrame:
        return (self.df.groupby("project_name")[["github_commits", "github_open_issues"]]
                .sum().reset_index())

    def deadline_load(self) -> pd.Series:
        return (self.df.dropna(subset=["deadline"])
                .groupby(self.df["deadline"].dt.date)
                .size())

    def plan_vs_fact(self) -> pd.DataFrame:
        """Суммарные план и факт часы по проектам + переработка."""
        return (self.df.groupby("project_name")
                .agg(
                    plan=("estimated_hours", "sum"),
                    fact=("actual_hours", "sum"),
                    overrun=("overrun_hours", "sum"),
                )
                .reset_index())

    def overrun_by_priority(self) -> pd.DataFrame:
        """Средняя переработка по приоритетам (только там, где факт > 0)."""
        df = self.df[self.df["actual_hours"] > 0]
        return (df.groupby("priority")["overrun_hours"].mean()
                .reset_index().sort_values("overrun_hours", ascending=False))

    def summary(self) -> dict:
        total = len(self.df)
        done = (self.df["status"] == "Done").sum()
        todo = (self.df["status"] == "Todo").sum()
        overdue = (self.df["risk_level"] == "Overdue").sum()
        high = (self.df["risk_level"] == "High").sum()
        overrun_mean = self.df.loc[self.df["actual_hours"] > 0, "overrun_hours"].mean()
        return {
            "total_tasks": total,
            "done_pct": round(done / total * 100, 1),
            "todo_pct": round(todo / total * 100, 1),
            "overdue_count": overdue,
            "high_risk_count": high,
            "overrun_mean": round(overrun_mean, 2),
            "top_commits_project": self.df.groupby("project_name")["github_commits"].sum().idxmax(),
            "worst_overrun_project": self.plan_vs_fact().sort_values("overrun", ascending=False).iloc[0]["project_name"],
        }
