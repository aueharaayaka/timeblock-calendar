#!/usr/bin/env python3
"""
TimeBlock data.json → Google Calendar CSV コンバーター

使い方:
  python3 convert_to_gcal.py                      # data.json → calendar.csv
  python3 convert_to_gcal.py input.json           # カスタム入力ファイル
  python3 convert_to_gcal.py input.json out.csv   # カスタム入力・出力ファイル
"""

import json
import csv
import sys
from datetime import datetime, timedelta


def load_blocks(json_path: str) -> list[dict]:
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    return data.get("blocks", [])


def block_to_gcal_row(block: dict) -> dict:
    """1ブロックをGoogleカレンダーCSVの1行に変換する"""
    date_str = block["date"]          # "YYYY-MM-DD"
    start_h = block.get("startH", 0)
    start_m = block.get("startM", 0)
    duration = block.get("durationMin", 0)

    start_dt = datetime.strptime(date_str, "%Y-%m-%d").replace(
        hour=start_h, minute=start_m
    )
    end_dt = start_dt + timedelta(minutes=duration)

    return {
        "Subject":       block.get("title", ""),
        "Start Date":    start_dt.strftime("%m/%d/%Y"),
        "Start Time":    start_dt.strftime("%I:%M %p"),
        "End Date":      end_dt.strftime("%m/%d/%Y"),
        "End Time":      end_dt.strftime("%I:%M %p"),
        "All Day Event": "False",
        "Description":   "",
        "Location":      "",
        "Private":       "False",
    }


def convert(json_path: str, csv_path: str) -> int:
    blocks = load_blocks(json_path)
    rows = [block_to_gcal_row(b) for b in blocks]

    fieldnames = [
        "Subject", "Start Date", "Start Time",
        "End Date", "End Time", "All Day Event",
        "Description", "Location", "Private",
    ]

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return len(rows)


if __name__ == "__main__":
    json_file = sys.argv[1] if len(sys.argv) > 1 else "data.json"
    csv_file  = sys.argv[2] if len(sys.argv) > 2 else "calendar.csv"

    count = convert(json_file, csv_file)
    print(f"{count} 件のイベントを {csv_file} に書き出しました。")
