import os
import sys
from playsound import playsound
import yaml
import argparse
import time

# コマンドライン引数のパーサーを作成
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input_dir", type=str, required=True, help="Input directory containing WAV files")
args = parser.parse_args()

# config.yamlからパラメータを読み込む
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# 指定されたディレクトリのパスを取得
wav_dir = os.path.expanduser(args.input_dir)

# wavファイルのパスを取得
wav_files = [f for f in os.listdir(wav_dir) if f.endswith(".wav")]

if not wav_files:
    print(f"No WAV files found in the directory: {wav_dir}")
    sys.exit(1)

# wavファイルを連番順にソート
wav_files.sort(key=lambda x: int(x.split("_")[1].split(".")[0]))

# 各wavファイルを順番に再生
for wav_file in wav_files:
    wav_path = os.path.join(wav_dir, wav_file)
    print(f"Playing {wav_file}")
    playsound(wav_path)
    time.sleep(0.3)