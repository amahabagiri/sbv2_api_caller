import json
from urllib.request import Request, urlopen
import tempfile
import os
from playsound import playsound
from urllib.parse import urlencode

# APIのエンドポイントURL
base_url = "http://127.0.0.1:5000/voice"

# リクエストヘッダー
headers = {
    "accept": "audio/wav"
}

# テキストの配列
text_array = ["こんにちは。私の名前はあかねです。今年で20歳です。", "泣いちゃいます", "好きな食べ物は魚です。"]

# 各テキストに対してリクエストを送信
for text in text_array:
    # リクエストパラメータ
    params = {
        "text": text,
        "encoding": "utf-8",
        "model_id": 3,
        "speaker_id": 0,
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
    url = base_url + "?" + urlencode(params)

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

            print(f"Played audio for text '{text}'")
    except Exception as e:
        print(f"Error occurred for text '{text}': {str(e)}")