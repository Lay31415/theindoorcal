#!/usr/bin/env python

import datetime
from icalendar import Calendar
import requests

# 今日の日付取得
today = datetime.date.today()

# 任意の日付で実行（デバッグ用）
# today = datetime.date(2022,11,19)

# カレンダー取得
url = "https://calendar.google.com/calendar/ical/theindoorgame@gmail.com/public/basic.ics"
res = requests.get(url)
ical = res.text

# カレンダーオブジェクト読み込み
calendar = Calendar.from_ical(ical)

# メッセージ格納変数
messages_allday = []
messages_hourly = []

# EVENT毎に処理
for event in calendar.walk('VEVENT'):
    # イベントの日付をdatetime型に変換
    dtstart = event.decoded('DTSTART')
    dtend = event.decoded('DTEND')

    if (type(dtstart) is datetime.date or type(dtend) is datetime.date):
        # 終日イベント
        # 開始日・終了日の取得
        start_day = dtstart
        end_day = dtend
        
        if ((start_day <= today) and (end_day >= today)):
            # 今日がイベント期間中なら
            # メッセージ作成
            message = dtstart.strftime('【%m/%d')
            message += '' if end_day <= today + datetime.timedelta(1) else dtend.strftime('～%m/%d')
            message += '】' + event['SUMMARY']
            messages_allday.append(message)
    else:
        # 時刻設定イベント
        # 開始日・終了日の取得
        start_day = dtstart.date()
        end_day = dtend.date()
        # 時刻をUTCからJSTへ変換
        dtstart = dtstart.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
        dtend = dtend.astimezone(datetime.timezone(datetime.timedelta(hours=9)))

        if ((start_day <= today) and (end_day >= today)):
            # 今日がイベント期間中なら
            # メッセージ作成
            message = dtstart.strftime('%H:%M～') if start_day == today else dtstart.strftime('%m/%d %H:%M～')
            message += dtend.strftime('%H:%M') if end_day == today else dtend.strftime('%m/%d %H:%M')
            message += '：' + event['SUMMARY']
            messages_hourly.append(message)

# メッセージを終日イベント→時刻イベントの順に（文字列ソートしつつ）結合
messages = []
messages.extend(sorted(messages_allday))
messages.extend(sorted(messages_hourly))

# メッセージ出力
for m in messages:
    print(m)