import json
from urllib.request import Request, urlopen
import tempfile
import os
from playsound import playsound
from urllib.parse import urlencode
import yaml
import time
import argparse
import datetime

# リクエストヘッダー
headers = {
    "accept": "audio/wav"
}

# コマンドライン引数のパーサーを作成
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--save", action="store_true", help="Save WAV files")
args = parser.parse_args()

# config.yamlからパラメータを読み込む
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

model_id = config["model_id"]
speaker_id = config["speaker_id"]
base_url = config["url"]
save_path = config.get("path", "~/Downloads")  # デフォルトは~/Downloads

# speech_script.txtからテキストの配列を読み込む
with open("speech_script.txt", "r", encoding="utf-8") as f:
    text_array = f.read().split("\n")

# wavファイルを保存する場合、ディレクトリを作成
if args.save:
    now = datetime.datetime.now()
    dir_name = f"sbv2_{now.strftime('%Y%m%d_%H%M_%S')}"
    save_dir = os.path.join(os.path.expanduser(save_path), dir_name)
    os.makedirs(save_dir, exist_ok=True)

# 各テキストに対してリクエストを送信
for i, text in enumerate(text_array, start=1):
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

            # wavファイルを保存する場合
            if args.save:
                save_file = os.path.join(save_dir, f"speech_{i:03d}.wav")
                os.rename(temp_file_path, save_file)
                print(f"Saved audio to {save_file}")
            else:
                # 一時ファイルを削除
                os.unlink(temp_file_path)

            time.sleep(0.2)

            print(f"Played audio for text '{text}'")
    except Exception as e:
        print(f"Error occurred for text '{text}': {str(e)}")