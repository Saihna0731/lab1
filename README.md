# AI Лаборатори — Хайлтын алгоритмууд (BFS, DFS, GBFS, A*)

Grid World дээр дөрвөн хайлтын алгоритмыг нэг интерфейсээр хэрэгжүүлж,
heuristic функцүүдийг харьцуулан benchmark хийх лабораторийн репо.

## Орчин

| Хэрэгсэл | Хувилбар |
|----------|----------|
| Python   | 3.14.2 (шаардлага: 3.11+) |
| Git      | 2.52.0 (шаардлага: 2.40+) |
| JupyterLab | 4.6.3 |

## Суулгах

```bash
# 1. Репог хуулах
git clone <repo-url>
cd "AI jyugyou"

# 2. Виртуал орчин
py -3.14 -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux / macOS

# 3. Хамаарал
pip install -r requirements.txt

# 4. Jupyter kernel бүртгэх
python -m ipykernel install --user --name ai-search-lab --display-name "Python (AI Search Lab)"
```

## Ажиллуулах

```bash
.venv\Scripts\jupyter lab       # JupyterLab нээх
.venv\Scripts\pytest -v         # Тест ажиллуулах
```

Notebook дотор kernel-ээ **Python (AI Search Lab)** болгож сонгоно.

## Бүтэц

```
.
├── src/            # Алгоритмын код (Search интерфейс, BFS/DFS/GBFS/A*)
├── tests/          # pytest тестүүд
├── notebooks/      # Шинжилгээ, benchmark, график
├── results/        # Benchmark үр дүн (git-д ордоггүй)
├── figures/        # График (git-д ордоггүй)
└── docs/           # Баримт бичиг, commit convention
```

## Хөгжүүлэлтийн дүрэм

Commit болон branch-ийн дүрмийг [docs/COMMIT_CONVENTION.md](docs/COMMIT_CONVENTION.md)-с үзнэ үү.
