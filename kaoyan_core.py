# -*- coding: utf-8 -*-
"""
考研打卡核心逻辑（CLI 和 Web 共用）
"""

import json
from datetime import date, datetime, timedelta
from pathlib import Path

APP_DIR = Path.home() / ".kaoyan_checkin"
DATA_FILE = APP_DIR / "records.json"

PHASES = [
    ("\u9636\u6bb5\u4e00\uff1a\u57fa\u7840\u94fa\u57ab\u671f",   "2026-08-01", "2026-12-31"),
    ("\u9636\u6bb5\u4e8c\uff1a\u5f3a\u5316\u5920\u5b9e\u671f",   "2027-01-01", "2027-06-30"),
    ("\u9636\u6bb5\u4e09\uff1a\u9ec4\u91d1\u6691\u5047",          "2027-07-01", "2027-09-30"),
    ("\u9636\u6bb5\u56db\uff1a\u771f\u9898\u590d\u76d8\u63d0\u5347", "2027-10-01", "2027-11-20"),
    ("\u9636\u6bb5\u4e94\uff1a\u7b14\u8bd5\u51b2\u523a",          "2027-11-21", "2027-12-31"),
]

SUBJECTS = ["\u6570\u5b66\u4e8c", "\u82f1\u8bed\u4e8c", "408", "\u653f\u6cbb"]

PHASE_TASKS = {
    "\u9636\u6bb5\u4e00\uff1a\u57fa\u7840\u94fa\u57ab\u671f":   ["\u9ad8\u6570+\u7ebf\u4ee3\u57fa\u7840", "660\u9898", "408\u7b2c\u4e00\u8f6e", "\u5355\u8bcd\u79ef\u7d2f"],
    "\u9636\u6bb5\u4e8c\uff1a\u5f3a\u5316\u5920\u5b9e\u671f":   ["660\u4e8c\u5237+330", "\u9605\u8bfb\u771f\u9898\u7cbe\u8bfb", "408\u7b2c\u4e8c\u8f6e", ""],
    "\u9636\u6bb5\u4e09\uff1a\u9ec4\u91d1\u6691\u5047":          ["\u771f\u98982005-2024", "\u7ffb\u8bd1/\u65b0\u9898\u578b", "408\u771f\u9898", "\u653f\u6cbb\u542f\u52a8"],
    "\u9636\u6bb5\u56db\uff1a\u771f\u9898\u590d\u76d8\u63d0\u5347": ["\u4e8c\u5237\u771f\u9898+\u6a21\u62df", "\u4f5c\u6587\u6a21\u677f", "\u4e09\u5237 408", "\u8096\u516b\u9009\u62e9\u9898"],
    "\u9636\u6bb5\u4e94\uff1a\u7b14\u8bd5\u51b2\u523a":          ["\u4fdd\u6301\u624b\u611f", "\u5168\u771f\u6a21\u62df", "\u9650\u65f6\u8bad\u7ec3", "\u8096\u56db\u80cc\u8bf5"],
}

PHASE_COLORS = {
    "\u9636\u6bb5\u4e00\uff1a\u57fa\u7840\u94fa\u57ab\u671f":   "#0EA5E9",
    "\u9636\u6bb5\u4e8c\uff1a\u5f3a\u5316\u5920\u5b9e\u671f":   "#3B82F6",
    "\u9636\u6bb5\u4e09\uff1a\u9ec4\u91d1\u6691\u5047":          "#F59E0B",
    "\u9636\u6bb5\u56db\uff1a\u771f\u9898\u590d\u76d8\u63d0\u5347": "#10B981",
    "\u9636\u6bb5\u4e94\uff1a\u7b14\u8bd5\u51b2\u523a":          "#EF4444",
}

SUBJECT_COLORS = {
    "\u6570\u5b66\u4e8c": "#3B82F6",
    "\u82f1\u8bed\u4e8c": "#A855F7",
    "408":    "#10B981",
    "\u653f\u6cbb":   "#EF4444",
}

SUBJECT_ICONS = {
    "\u6570\u5b66\u4e8c": "M",
    "\u82f1\u8bed\u4e8c": "E",
    "408":    "C",
    "\u653f\u6cbb":   "P",
}

# ============================================================
# 数据层
# ============================================================
def ensure_app_dir():
    APP_DIR.mkdir(parents=True, exist_ok=True)

def load_records() -> dict:
    ensure_app_dir()
    if not DATA_FILE.exists():
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def save_records(records: dict):
    ensure_app_dir()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

# ============================================================
# 工具函数
# ============================================================
def today_str() -> str:
    return date.today().isoformat()

def str_to_date(s: str) -> date:
    return date.fromisoformat(s)

def get_current_phase(today: date = None) -> tuple:
    if today is None:
        today = date.today()
    for name, start, end in PHASES:
        if str_to_date(start) <= today <= str_to_date(end):
            return name, start, end
    return ("\u7b14\u8bd5\u5df2\u7ed3\u675f", "2027-12-31", "2027-12-31")

def streak_days(records: dict) -> int:
    if not records:
        return 0
    today = date.today()
    streak = 0
    d = today
    if today_str() not in records:
        d = today - timedelta(days=1)
    while d.isoformat() in records:
        streak += 1
        d -= timedelta(days=1)
    return streak

def total_days(records: dict) -> int:
    return len(records)

def week_stats(records: dict):
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    result = []
    for i in range(7):
        d = monday + timedelta(days=i)
        key = d.isoformat()
        if key in records:
            r = records[key]
            tasks_done = sum(1 for s in SUBJECTS if r.get(s))
            result.append({
                "date": d.isoformat(),
                "weekday": d.strftime("%a"),
                "weekday_cn": ["\u5468\u4e00","\u5468\u4e8c","\u5468\u4e09","\u5468\u56db","\u5468\u4e94","\u5468\u516d","\u5468\u65e5"][i],
                "tasks_done": tasks_done,
                "is_today": d == today,
                "is_future": d > today,
                "note": r.get("note", ""),
            })
        else:
            result.append({
                "date": d.isoformat(),
                "weekday": d.strftime("%a"),
                "weekday_cn": ["\u5468\u4e00","\u5468\u4e8c","\u5468\u4e09","\u5468\u56db","\u5468\u4e94","\u5468\u516d","\u5468\u65e5"][i],
                "tasks_done": 0,
                "is_today": d == today,
                "is_future": d > today,
                "note": "",
            })
    return result, monday, today

def phase_progress(phase_name: str, start: str, end: str, records: dict):
    start_d = str_to_date(start)
    end_d   = str_to_date(end)
    today   = date.today()
    # 阶段总长度
    phase_full_length = (end_d - start_d).days + 1
    # 当前已过天数（含今天）：裁到 [start_d, today]
    if today < start_d:
        elapsed = 0
        elapsed_end = start_d - timedelta(days=1)
    elif today > end_d:
        elapsed = phase_full_length
        elapsed_end = end_d
    else:
        elapsed = (today - start_d).days + 1
        elapsed_end = today
    # 打卡统计：只统计到 elapsed_end（含）为止
    count = 0
    subject_done = {s: 0 for s in SUBJECTS}
    d = start_d
    while d <= elapsed_end:
        key = d.isoformat()
        if key in records:
            count += 1
            for s in SUBJECTS:
                if records[key].get(s):
                    subject_done[s] += 1
        d += timedelta(days=1)
    # 进度条 = 打卡率（已打卡天数 / 阶段总天数）
    time_pct = elapsed / phase_full_length * 100 if phase_full_length > 0 else 0
    checkin_pct = count / elapsed * 100 if elapsed > 0 else 0
    bar_pct = count / phase_full_length * 100 if phase_full_length > 0 else 0
    return {
        "done": count,
        "total": phase_full_length,        # 阶段总天数
        "elapsed": elapsed,                # 已过天数
        "subject_done": subject_done,
        "time_pct": time_pct,              # 时间进度
        "checkin_pct": checkin_pct,        # 打卡率（相对已过天数）
        "pct": bar_pct,                   # 进度条 = 打卡率（done/total）
    }

def get_full_state() -> dict:
    """返回给前端的完整状态"""
    records = load_records()
    today = today_str()
    phase_name, phase_start, phase_end = get_current_phase()
    today_record = records.get(today, {s: False for s in SUBJECTS})
    today_record.setdefault("note", "")

    # 周统计
    week, monday, today_d = week_stats(records)

    # 阶段进度
    phases_data = []
    for p_name, start, end in PHASES:
        s_d, e_d = str_to_date(start), str_to_date(end)
        prog = phase_progress(p_name, start, end, records)
        if s_d <= today_d <= e_d:
            marker = "current"
        elif e_d < today_d:
            marker = "past"
        else:
            marker = "future"
        phases_data.append({
            "name": p_name,
            "start": start,
            "end": end,
            "color": PHASE_COLORS.get(p_name, "#6B7280"),
            "marker": marker,
            # 未来阶段：置零展示
            "done": 0 if marker == "future" else prog["done"],
            "elapsed": 0 if marker == "future" else prog["elapsed"],
            "subject_done": {s: 0 for s in SUBJECTS} if marker == "future" else prog["subject_done"],
            "time_pct": 0 if marker == "future" else prog["time_pct"],
            "checkin_pct": 0 if marker == "future" else prog["checkin_pct"],
            "total": prog["total"],
            "pct": 0 if marker == "future" else prog["pct"],
        })

    # 各科完成率
    subj_counts = {s: sum(1 for r in records.values() if r.get(s)) for s in SUBJECTS}
    total = total_days(records)

    # 最近 90 天日历
    calendar = []
    for i in range(89, -1, -1):
        d = today_d - timedelta(days=i)
        key = d.isoformat()
        is_today = (d == today_d)
        if key in records:
            r = records[key]
            tasks_done = sum(1 for s in SUBJECTS if r.get(s))
            calendar.append({
                "date": key,
                "tasks_done": tasks_done,
                "level": tasks_done,  # 0-4
                "is_today": is_today,
            })
        else:
            calendar.append({
                "date": key,
                "tasks_done": 0,
                "level": 0,
                "is_today": is_today,
            })

    return {
        "today": today,
        "today_weekday": today_d.strftime("%A"),
        "current_phase": {
            "name": phase_name,
            "start": phase_start,
            "end": phase_end,
            "color": PHASE_COLORS.get(phase_name, "#6B7280"),
            "tasks": PHASE_TASKS.get(phase_name, []),
        },
        "today_record": today_record,
        "subjects": [
            {
                "name": s,
                "color": SUBJECT_COLORS[s],
                "icon": SUBJECT_ICONS[s],
                "done": today_record.get(s, False),
            } for s in SUBJECTS
        ],
        "stats": {
            "total_days": total,
            "streak": streak_days(records),
        },
        "week": week,
        "phases": phases_data,
        "subject_stats": [
            {
                "name": s,
                "color": SUBJECT_COLORS[s],
                "icon": SUBJECT_ICONS[s],
                "done_count": subj_counts[s],
                "total_count": total,
                "pct": subj_counts[s] / total * 100 if total > 0 else 0,
            } for s in SUBJECTS
        ],
        "calendar": calendar,
        "all_records": records,  # 详情用
    }

def update_today(subjects_done: dict, note: str = "") -> dict:
    """更新今日打卡，返回新状态"""
    records = load_records()
    today = today_str()
    if today not in records:
        records[today] = {s: False for s in SUBJECTS}
        records[today]["note"] = ""
    records[today].update(subjects_done)
    if note is not None:
        records[today]["note"] = note
    records[today]["checkin_time"] = datetime.now().strftime("%H:%M")
    save_records(records)
    return get_full_state()

def delete_today() -> dict:
    records = load_records()
    today = today_str()
    if today in records:
        del records[today]
        save_records(records)
    return get_full_state()
