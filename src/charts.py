import os
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams["font.family"] = "DejaVu Sans"
sns.set_theme(style="whitegrid", palette="muted")


class ChartBuilder:
    def __init__(self, analyzer, out_dir="charts"):
        self.a = analyzer
        self.out_dir = out_dir
        os.makedirs(out_dir, exist_ok=True)

    def _save(self, fig, name):
        path = os.path.join(self.out_dir, name)
        fig.tight_layout()
        fig.savefig(path, dpi=150)
        plt.close(fig)
        print(f"  ✓ {path}")

    def status_by_project(self):
        data = self.a.status_by_project()
        fig, ax = plt.subplots(figsize=(10, 6))
        data.plot(kind="bar", stacked=True, ax=ax, colormap="viridis")
        ax.set_title("Статусы задач по проектам")
        ax.set_xlabel("Проект")
        ax.set_ylabel("Количество задач")
        ax.legend(title="Статус", bbox_to_anchor=(1.02, 1), loc="upper left")
        self._save(fig, "01_status_by_project.png")

    def priority_by_project(self):
        data = self.a.priority_by_project()
        fig, ax = plt.subplots(figsize=(10, 6))
        data.plot(kind="bar", ax=ax, colormap="coolwarm")
        ax.set_title("Приоритеты задач по проектам")
        ax.set_xlabel("Проект")
        ax.set_ylabel("Количество задач")
        ax.legend(title="Приоритет")
        self._save(fig, "02_priority_by_project.png")

    def risk_by_project(self):
        data = self.a.risk_by_project()
        fig, ax = plt.subplots(figsize=(10, 6))
        data.plot(kind="bar", stacked=True, ax=ax, colormap="RdYlGn_r")
        ax.set_title("Уровень риска по проектам")
        ax.set_xlabel("Проект")
        ax.set_ylabel("Количество задач")
        ax.legend(title="Риск")
        self._save(fig, "03_risk_by_project.png")

    def github_stats(self):
        data = self.a.github_stats()
        fig, ax = plt.subplots(figsize=(10, 6))
        x = range(len(data))
        w = 0.4
        ax.bar([i - w / 2 for i in x], data["github_commits"], w,
               label="Коммиты", color="#4C72B0")
        ax.bar([i + w / 2 for i in x], data["github_open_issues"], w,
               label="Открытые issues", color="#DD8452")
        ax.set_xticks(list(x))
        ax.set_xticklabels(data["project_name"], rotation=15)
        ax.set_title("GitHub-активность по проектам")
        ax.set_ylabel("Количество")
        ax.legend()
        self._save(fig, "04_github_stats.png")

    def deadline_load(self):
        data = self.a.deadline_load()
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.bar([str(d) for d in data.index], data.values, color="#55A868")
        ax.set_title("Нагрузка по датам дедлайнов")
        ax.set_xlabel("Дата дедлайна")
        ax.set_ylabel("Количество задач")
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
        self._save(fig, "05_deadline_load.png")

    def plan_vs_fact(self):
        """Новый график: план vs факт часов по проектам."""
        data = self.a.plan_vs_fact()
        fig, ax = plt.subplots(figsize=(10, 6))
        x = range(len(data))
        w = 0.35
        ax.bar([i - w / 2 for i in x], data["plan"], w,
               label="План (часы)", color="#4C72B0")
        ax.bar([i + w / 2 for i in x], data["fact"], w,
               label="Факт (часы)", color="#DD8452")
        ax.set_xticks(list(x))
        ax.set_xticklabels(data["project_name"], rotation=15)
        ax.set_title("План vs Факт часов по проектам")
        ax.set_ylabel("Часы")
        ax.legend()
        self._save(fig, "06_plan_vs_fact.png")

    def overrun_by_priority(self):
        
        data = self.a.overrun_by_priority()
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x="priority", y="overrun_hours", data=data,
                    ax=ax, palette="coolwarm")
        ax.axhline(0, color="gray", linewidth=0.8, linestyle="--")
        ax.set_title("Средняя переработка по приоритетам (часы)")
        ax.set_xlabel("Приоритет")
        ax.set_ylabel("Средняя переработка, ч")
        for i, v in enumerate(data["overrun_hours"]):
            ax.text(i, v, f"{v:+.2f}", ha="center",
                    va="bottom" if v >= 0 else "top")
        self._save(fig, "07_overrun_by_priority.png")

    def overrun_by_priority(self):
        """Новый график: средняя переработка по приоритетам."""
        data = self.a.overrun_by_priority()
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(
            x="priority", y="overrun_hours", data=data,
            hue="priority",          # ← добавили: красим по приоритету
            palette="coolwarm",
            legend=False,            # ← и отключаем легенду (она избыточна)
            ax=ax,
        )
        ax.axhline(0, color="gray", linewidth=0.8, linestyle="--")
        ax.set_title("Средняя переработка по приоритетам (часы)")
        ax.set_xlabel("Приоритет")
        ax.set_ylabel("Средняя переработка, ч")
        for i, v in enumerate(data["overrun_hours"]):
            ax.text(i, v, f"{v:+.2f}", ha="center",
                    va="bottom" if v >= 0 else "top")
        self._save(fig, "07_overrun_by_priority.png")
    
    def build_all(self):
        print("Строим графики...")
        self.status_by_project()
        self.priority_by_project()
        self.risk_by_project()
        self.github_stats()
        self.deadline_load()
        self.plan_vs_fact()
        self.overrun_by_priority()
        print("Готово.")
