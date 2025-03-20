#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MacOS上で指定ウィンドウのスクリーンショット撮影、キー押下後にROI選択でクロップしPDFにまとめるサンプル
"""

import subprocess
import time
import os
from pynput.keyboard import Controller, Key
import cv2
from PIL import Image

# ======================
# 設定項目
# ======================

time.sleep(3)

# ※ 以下のWINDOW_IDは対象ウィンドウのIDに置き換えてください。
WINDOW_ID = "47"  # 例：対象ウィンドウのID（文字列でも整数でもOK）
ITERATIONS = 18       # スクリーンショット取得＆キー押下の回数
SPECIFIED_KEY = Key.right  # 押下するキー（例としてスペースキー）
OUTPUT_DIR = "screenshots"  # 一時的に保存するフォルダ名

# ======================
# スクリーンショット撮影＆キー押下処理
# ======================

# キーボード操作用のコントローラ
keyboard = Controller()

# 保存用ディレクトリの作成
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# 撮影したスクリーンショットのファイルパスを保存するリスト
screenshot_files = []

for i in range(ITERATIONS):
    filename = os.path.join(OUTPUT_DIR, f"screenshot_{i+1}.png")
    print(f"[{i+1}/{ITERATIONS}] ウィンドウID {WINDOW_ID} のスクリーンショットを撮影: {filename}")
    # MacOSのscreencaptureコマンドを使用して、指定ウィンドウのスクリーンショットを撮影
    # -l オプションでウィンドウIDを指定
    subprocess.run(["screencapture", "-l", str(WINDOW_ID), filename])
    screenshot_files.append(filename)
    
    # 指定キー（ここではスペースキー）を押下する処理
    print(f"キー {SPECIFIED_KEY} を押下します。")
    keyboard.press(SPECIFIED_KEY)
    keyboard.release(SPECIFIED_KEY)
    
    # 次の撮影までの待機（必要に応じて調整）
    time.sleep(1)

# ======================
# ROI選択（クロップ領域指定）処理
# ======================
# OpenCVのselectROIを使用して、最初のスクリーンショットからクロップする領域をユーザーに指定してもらう
print("ROI選択ウィンドウを表示します。クロップしたい領域をドラッグして選択し、Enterキーを押してください。")
img = cv2.imread(screenshot_files[0])
# ウィンドウタイトル「ROI選択」でROI選択用のGUIを表示（Tkは使用していません）
r = cv2.selectROI("ROI選択", img, showCrosshair=True, fromCenter=False)
cv2.destroyAllWindows()
x, y, w, h = map(int, r)
print(f"選択した領域： x={x}, y={y}, w={w}, h={h}")

# ======================
# クロップ処理とPDF作成
# ======================
cropped_images = []

for file in screenshot_files:
    # PILで画像を開く
    image = Image.open(file)
    # ROIでクロップ（左上座標(x,y)から右下座標(x+w, y+h)）
    cropped = image.crop((x, y, x+w, y+h))
    # PDF作成のためRGBモードに変換
    cropped_images.append(cropped.convert("RGB"))

# クロップ後の画像を1つのPDFにまとめる
pdf_filename = "output.pdf"
if cropped_images:
    # 最初の画像を基準にして、残りをappend_imagesでPDFにまとめる
    cropped_images[0].save(pdf_filename, save_all=True, append_images=cropped_images[1:])
    print(f"PDFファイルが作成されました： {pdf_filename}")
else:
    print("クロップした画像が存在しません。")

# ======================
# 後処理（必要に応じて一時ファイル削除など）
# ======================
# 例：撮影した画像を削除する場合
# for file in screenshot_files:
#     os.remove(file)
# print("一時ファイルを削除しました。")
