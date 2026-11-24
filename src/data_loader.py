import pandas as pd


class DataLoader:
    """Загружает CSV, чистит, приводит типы, вычисляет риск."""

    def __init__(self, path: str, today: str = "2026-11-23"):
        self.path = path
        self.today = pd.Timestamp(today)  # фиксируем "сегодня" для воспроизводимости
        self.df: pd.DataFrame | None = None

    def load(self) -> pd.DataFrame:
        # sep=',' — стандарт; utf-8 — без BOM
        df = pd.read_csv(self.path, sep=",", encoding="utf-8")

        # даты — ISO, парсим напрямую
        df["deadline"] = pd.to_datetime(df["deadline"], errors="coerce")

        # часы — числа; на всякий случай приводим и заполняем пропуски
        for col in ["estimated_hours", "actual_hours"]:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)

        # счётчики GitHub — целые
        for col in ["github_commits", "github_open_issues"]:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

        # строковые — убираем пробелы
        for col in ["project_name", "priority", "status", "task_title"]:
            df[col] = df[col].astype(str).str.strip()

        # вычисляем риск
        df["risk_level"] = df.apply(self._calc_risk, axis=1)

        # вычисляем переработку (факт - план) только там, где факт есть
        df["overrun_hours"] = df.apply(
            lambda r: r["actual_hours"] - r["estimated_hours"]
            if r["actual_hours"] > 0 else 0.0,
            axis=1,
        )

        self.df = df
        return df

    def _calc_risk(self, row) -> str:
        """Риск: смотрим на статус и близость дедлайна к 'сегодня'."""
        if pd.isna(row["deadline"]):
            return "Unknown"
        if row["status"] == "Done":
            return "Low"
        days_left = (row["deadline"] - self.today).days
        if days_left < 0:
            return "Overdue"     # уже просрочено
        if days_left < 7:
            return "High"
        if days_left < 14:
            return "Medium"
        return "Low"
