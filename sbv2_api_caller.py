import json
from urllib.request import Request, urlopen
import tempfile
import os
from playsound import playsound
from urllib.parse import urlencode
import yaml
import time


# リクエストヘッダー
headers = {
    "accept": "audio/wav"
}

# config.yamlからパラメータを読み込む
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

model_id = config["model_id"]
speaker_id = config["speaker_id"]
base_url = config["url"]

# speech_script.txtからテキストの配列を読み込む
with open("speech_script.txt", "r", encoding="utf-8") as f:
    text_array = f.read().split("\n")

# 各テキストに対してリクエストを送信
for text in text_array:
    # リクエストパラメータ
    params = {
        "text": text.strip().replace("\n", ""),  # 前後の空白を削除し、改行を取り除く
        "encoding": "utf-8",
        "model_id": model_id,
        "speaker_id": speaker_id,
        "sdp_ratio": 0.2,
        "noise": 0.6,
        "noisew": 0.8,
        "length": 1,
        "language": "JP",
        "auto_split": "true",
        "split_interval": 0.5,
        #"assist_text": None,
        "assist_text_weight": 1,
        "style": "Neutral",
        "style_weight": 10
    }

    # パラメータをURLエンコードして、URLに追加
    url = base_url + "/voice" + "?" + urlencode(params)

    # GETリクエストを作成
    req = Request(url, headers=headers, method="GET")

    print(f"Request URL: {req.full_url}")  # デバッグ: リクエストURLを出力

    try:
        # リクエストを送信し、レスポンスを取得
        with urlopen(req) as response:
            # レスポンスヘッダーを出力
            print(f"Response headers: {response.headers}")

            # 一時ファイルを作成して音声データを保存
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                temp_file.write(response.read())
                temp_file_path = temp_file.name

            # 音声ファイルを再生
            playsound(temp_file_path)

            # 一時ファイルを削除
            os.unlink(temp_file_path)
            time.sleep(0.2)

            print(f"Played audio for text '{text}'")
    except Exception as e:
        print(f"Error occurred for text '{text}': {str(e)}")