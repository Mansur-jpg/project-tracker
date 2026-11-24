from data_loader import DataLoader
from analyzer import Analyzer
from charts import ChartBuilder


def main():
    df = DataLoader("../data/project_tasks_data.csv").load()
    print(f"Загружено строк: {len(df)}")
    print(f"Колонки: {list(df.columns)}\n")

    analyzer = Analyzer(df)

    s = analyzer.summary()
    print("=== КЛЮЧЕВЫЕ ВЫВОДЫ ===")
    print(f"Всего задач:               {s['total_tasks']}")
    print(f"Выполнено (Done):          {s['done_pct']}%")
    print(f"В очереди (Todo):          {s['todo_pct']}%")
    print(f"Просрочено (Overdue):      {s['overdue_count']}")
    print(f"Высокий риск (High):       {s['high_risk_count']}")
    print(f"Средняя переработка:       {s['overrun_mean']} ч")
    print(f"Лидер по коммитам:         {s['top_commits_project']}")
    print(f"Худшая переработка:        {s['worst_overrun_project']}")

    ChartBuilder(analyzer).build_all()


if __name__ == "__main__":
    main()
