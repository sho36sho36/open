# FileFusion

**Python製の軽量・プラグイン方式ファイルビューア／プレイヤー**

さまざまな拡張子のファイルを、専用のGUIで表示・再生・操作できるアプリケーションを目指します。

> 「ファイルを開く」を、もっと自由に。

---

## ✨ Features

* 🖥 軽量なデスクトップGUI
* 🔌 プラグイン方式
* 📂 拡張子による自動判定
* 🧩 ファイル形式ごとの専用GUI
* 🎵 音声ファイルの再生
* 🎹 MIDIファイルのピアノロール表示・再生
* 🚀 必要な機能だけをプラグインとして追加
* 🛠 外部プラグインへの拡張を想定
* 🐍 Python製

---

## 🏗 Architecture

```text
FileFusion
│
├─ Core
│   ├─ File Detector
│   ├─ Plugin Manager
│   ├─ Plugin API
│   └─ Viewer System
│
├─ UI
│
└─ Plugins
    ├─ Built-in Plugins
    │   ├─ MIDI Plugin
    │   └─ Audio Plugin
    │
    └─ External Plugins
```

FileFusionでは、ファイル形式ごとの処理をプラグインとして分離しています。

---

## 🔌 Plugin System

FileFusionは、拡張子に応じて対応するプラグインを自動的に選択します。

### 🎹 MIDI

MIDIは通常の音声ファイルとは異なり、演奏情報を扱うため専用プラグインとして実装されています。

```text
MIDI
 ↓
MIDI Plugin
 ↓
MIDI解析
 ↓
ピアノロール
 ↓
MIDI再生
```

### 🎵 通常の音声

WAVやMP3などの一般的な音声形式は、共通のAudio Pluginで処理します。

```text
WAV / MP3 / M4A / ...
        ↓
   Audio Plugin
        ↓
  共通Audio Viewer
        ↓
 再生・一時停止・停止
      シーク・音量
```

この方式により、音声形式ごとに個別のプラグインを作る必要がありません。

---

## 🎹 MIDI Plugin

現在、MIDIファイルに対応しています。

### 対応拡張子

* `.mid`
* `.midi`

### 主な機能

* 🎹 ピアノロール表示
* 🎵 ノート表示
* ▶ 再生
* ⏸ 一時停止
* ⏹ 停止
* ⏩ 再生位置操作
* 🔊 MIDI出力選択
* 🎼 鍵盤表示
* 🚀 大きなMIDIファイルを考慮した描画最適化

---

## 🎵 Audio Plugin

一般的な音声ファイルを1つの共通プラグインで扱います。

### 対応拡張子

* `.wav`
* `.mp3`
* `.m4a`
* `.aac`
* `.flac`
* `.ogg`
* `.aiff`
* `.aif`
* `.au`

### 主な機能

* ▶ 再生
* ⏸ 一時停止
* ⏹ 停止
* ⏩ シーク
* 🔊 音量調整
* ⏱ 再生時間表示
* 📊 ファイル形式・サイズ表示

Audio Pluginは **PySide6 Qt Multimedia** を利用して音声を再生します。

---

## 📋 対応予定

### Web

* HTML
* MHTML
* CSS
* XSL
* Markdown

### 文書

* TXT
* DOC
* DOCX
* XLS
* XLSX
* PPT
* PPTX
* RTF
* PDF

### 画像

* BMP
* GIF
* ICO
* JPG
* PNG
* TIFF
* WebP

### 音声

* AAC
* AIFF
* AU
* M4A
* MIDI
* MP3
* WAV
* WMA
* FLAC
* OGG

### 動画

* 3GP
* AVI
* FLV
* MOV
* MPEG
* MP4
* WebM
* WMV

### アーカイブ

* 7Z
* BZ2
* GZ
* LZH
* RAR
* TAR
* ZIP

### その他

今後さらに追加予定です。

---

## 🏗 Project Structure

```text
open/
├─ main.py
├─ requirements.txt
├─ README.md
│
├─ core/
│  ├─ application.py
│  ├─ plugin.py
│  ├─ plugin_manager.py
│  ├─ file_info.py
│  ├─ file_detector.py
│  ├─ viewer.py
│  └─ exceptions.py
│
├─ ui/
│  ├─ main_window.py
│  └─ widgets/
│
├─ plugins/
│  ├─ builtin/
│  │  ├─ example/
│  │  ├─ midi/
│  │  │  ├─ plugin.py
│  │  │  ├─ midi_parser.py
│  │  │  ├─ midi_player.py
│  │  │  └─ midi_viewer.py
│  │  │
│  │  └─ audio/
│  │     ├─ plugin.py
│  │     └─ audio_viewer.py
│  │
│  └─ external/
│
├─ tests/
│
└─ docs/
   └─ PLUGIN.md
```

---

## 🛠️ Technologies

FileFusionは以下の技術を使用しています。

* Python
* PySide6
* Qt Multimedia
* Mido
* python-rtmidi

---

## 🚧 Version History

### v1.1.0

**Audio Plugin追加**

* 共通Audio Pluginを追加
* WAV / MP3などの音声ファイルに対応
* 再生・一時停止・停止
* シーク
* 音量調整
* 再生時間表示
* Qt Multimediaによる音声再生

### v1.0.1

**MIDI Plugin追加**

* MIDIファイル対応
* MIDI解析
* ピアノロール表示
* MIDI再生
* MIDI出力選択

### v1.0.0

**Initial Release**

* Core
* Plugin Manager
* Plugin API
* File Detector
* Viewer基盤
* GUI
* サンプルPlugin
* テスト

---

## 📦 Installation

```bash
pip install -r requirements.txt
```

---

## ▶ Run

```bash
python main.py
```

---

## 🧪 Test

```bash
python -m pytest
```

---

## 🧩 Plugin Development

プラグイン開発については、

`docs/PLUGIN.md`

を参照してください。

---

## 📜 License

MIT License
