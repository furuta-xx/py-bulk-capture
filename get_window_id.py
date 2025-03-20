#!/usr/bin/env python3
import Quartz

# オンスクリーンかつデスクトップ要素以外のウィンドウ情報を取得
options = Quartz.kCGWindowListOptionOnScreenOnly | Quartz.kCGWindowListExcludeDesktopElements
windowList = Quartz.CGWindowListCopyWindowInfo(options, Quartz.kCGNullWindowID)

for window in windowList:
    ownerName = window.get("kCGWindowOwnerName", "Unknown")
    windowNumber = window.get("kCGWindowNumber", None)
    bounds = window.get("kCGWindowBounds", {})
    print(f"ウィンドウID: {windowNumber}, アプリケーション: {ownerName}, 座標: {bounds}")
