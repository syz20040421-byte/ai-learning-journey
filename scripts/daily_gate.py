#!/usr/bin/env python3
"""每日判重闸门 — 保证「一天只推一次任务」。

被 Windows 登录触发器和 Hermes cron 双路调用，用文件锁 + 日期标记去重。

退出码:
    0  = 应该跑（已抢到今天的锁）
    10 = 今天已经跑过了，跳过
    11 = 今天是休息日，跳过
    1  = 出错

用法:
    python daily_gate.py            # 检查并抢锁
    python daily_gate.py --check    # 只检查不抢锁
    python daily_gate.py --release  # 释放今天的锁（调试用）
    python daily_gate.py --status   # 打印状态
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
STATE_DIR = BASE / "state"
PROGRESS = BASE / "progress.json"

EXIT_RUN = 0
EXIT_ALREADY_RAN = 10
EXIT_REST_DAY = 11
EXIT_ERROR = 1

WEEKDAY_NAMES = [
    "monday", "tuesday", "wednesday", "thursday",
    "friday", "saturday", "sunday",
]


def today_str() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def marker_path(date: str) -> Path:
    return STATE_DIR / f"ran_{date}.marker"


def load_progress() -> dict:
    if not PROGRESS.exists():
        return {}
    try:
        return json.loads(PROGRESS.read_text(encoding="utf-8"))
    except Exception:
        return {}


def rest_day() -> str:
    prog = load_progress()
    return (prog.get("student", {}) or {}).get("rest_day", "saturday").lower()


def is_rest_day(date: str | None = None) -> bool:
    d = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
    return WEEKDAY_NAMES[d.weekday()] == rest_day()


def cleanup_old_markers(keep_days: int = 30) -> None:
    """删掉 30 天前的标记文件，避免目录膨胀。"""
    cutoff = datetime.now() - timedelta(days=keep_days)
    for p in STATE_DIR.glob("ran_*.marker"):
        try:
            stamp = p.stem.replace("ran_", "")
            if datetime.strptime(stamp, "%Y-%m-%d") < cutoff:
                p.unlink()
        except Exception:
            continue


def acquire(date: str) -> bool:
    """原子抢锁。O_CREAT|O_EXCL 保证并发下只有一个赢家。"""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    path = marker_path(date)
    try:
        fd = os.open(str(path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        return False
    try:
        payload = json.dumps(
            {
                "date": date,
                "acquired_at": datetime.now().isoformat(timespec="seconds"),
                "pid": os.getpid(),
            },
            ensure_ascii=False,
        )
        os.write(fd, payload.encode("utf-8"))
    finally:
        os.close(fd)
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="只检查不抢锁")
    ap.add_argument("--release", action="store_true", help="释放今天的锁")
    ap.add_argument("--status", action="store_true", help="打印状态")
    ap.add_argument("--date", help="覆盖日期（测试用，YYYY-MM-DD）")
    ap.add_argument(
        "--ignore-rest-day", action="store_true", help="忽略休息日判断"
    )
    args = ap.parse_args()

    date = args.date or today_str()

    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)

        if args.release:
            p = marker_path(date)
            if p.exists():
                p.unlink()
                print(f"已释放 {date} 的锁")
            else:
                print(f"{date} 没有锁")
            return 0

        if args.status:
            prog = load_progress()
            cur = prog.get("current", {})
            streak = prog.get("streak", {})
            print(f"日期:       {date}")
            print(f"休息日:     {rest_day()}  (今天{'是' if is_rest_day(date) else '不是'})")
            print(f"今天已跑:   {'是' if marker_path(date).exists() else '否'}")
            print(f"当前周:     第 {cur.get('week', '?')} 周")
            print(f"阶段:       {cur.get('phase', '?')}")
            print(f"摸底完成:   {'是' if cur.get('baseline_test_done') else '否'}")
            print(f"连续打卡:   {streak.get('current', 0)} 天")
            markers = sorted(STATE_DIR.glob("ran_*.marker"))
            print(f"历史标记:   {len(markers)} 个")
            return 0

        if is_rest_day(date) and not args.ignore_rest_day:
            print(f"SKIP_REST_DAY {date} 是休息日（{rest_day()}）")
            return EXIT_REST_DAY

        if args.check:
            if marker_path(date).exists():
                print(f"ALREADY_RAN {date}")
                return EXIT_ALREADY_RAN
            print(f"SHOULD_RUN {date}")
            return EXIT_RUN

        if acquire(date):
            cleanup_old_markers()
            print(f"LOCK_ACQUIRED {date}")
            return EXIT_RUN

        print(f"ALREADY_RAN {date}")
        return EXIT_ALREADY_RAN

    except Exception as e:  # noqa: BLE001
        print(f"ERROR {type(e).__name__}: {e}", file=sys.stderr)
        return EXIT_ERROR


if __name__ == "__main__":
    sys.exit(main())
