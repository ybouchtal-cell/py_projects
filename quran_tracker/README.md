# 📖 Quran Tracker

A desktop app for tracking Quran memorization and revision progress, built with Python and [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter).

## Features

- **Add Surah** — log a newly memorized surah, with duplicate protection
- **Revision** — record repetitions for a surah you're reviewing, with an undo option
- **Daily Quests** — get a suggested daily task and log progress against it
- **Progress** — view all tracked surahs and their stats in a table

## Tech stack

- Python 3
- CustomTkinter — GUI
- Pandas — progress data stored and manipulated as CSV
- JSON — surah reference data

## Project structure

```
quran_tracker/
├── GUI.py              # app entry point and all windows
├── quran_f.py          # core logic: add/read/update progress data
├── Table.py            # progress table view
└── data/
    ├── surahs.json      # surah reference list
    └── quran.csv        # user progress (generated at runtime)
```

## Running it

```bash
pip install customtkinter pandas
python GUI.py
```

## What I learned building this

- Structuring a multi-window Tkinter/CustomTkinter app (`CTk` main window + `CTkToplevel` popups) and passing state between them
- Separating GUI code from data logic (`GUI.py` vs `quran_f.py`) instead of mixing them
- Reading/writing structured data with `pandas` and `JSON`
- Building small reusable UI helper methods (`create_button`, `create_label`, `option_menu`) instead of repeating widget setup
- Iterating on layout and styling: consistent spacing, a shared color/font system, and avoiding UI state bugs (e.g. stale labels not being cleared)

## Motivation

Built this to stay consistent with my own Quran memorization and revision — wanted a lightweight tracker that fit how I actually review surahs, instead of a generic habit-tracker app.