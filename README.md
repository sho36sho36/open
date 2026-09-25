# FileFusion

**Python製の軽量・プラグイン方式ファイルビューア／プレイヤー**

さまざまな拡張子のファイルを、専用のGUIで表示・再生・操作できるアプリケーションを目指します。

> 「ファイルを開く」を、もっと自由に。

---

## ✨ Features

- 🖥 軽量なデスクトップGUI
- 🔌 プラグイン方式
- 📂 拡張子による自動判定
- 🧩 ファイル形式ごとの専用GUI
- 🎵 MIDIファイルの再生・表示
- 🎹 ピアノロール形式のMIDI表示
- ⚡ 軽量なMIDI再生エンジン
- 🚀 必要な機能だけをプラグインとして追加
- 🛠 外部プラグインへの拡張を想定
- 🐍 Python製

---

## 🎵 MIDI Plugin

FileFusion v1.0.1では、MIDIプラグインを追加しました。

`.mid` / `.midi` ファイルを開くと、専用のMIDIビューアが表示されます。

### 主な機能

- 🎹 ピアノロール表示
- 🎵 MIDI再生
- ⏯ 再生・一時停止・停止
- ⏩ シーク
- 🎚 MIDI出力デバイス選択
- 🎼 ノート・ベロシティ表示
- ⚡ 軽量な再生処理
- 🧵 GUIとMIDI再生を分離した非同期再生
- 📈 再生時間に基づいた安定したタイミング制御

MIDI再生中もGUIが重くなりにくいように設計しています。

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
│   └─ Main Window
│
└─ Plugins
    ├─ Built-in Plugins
    │   ├─ Example
    │   └─ MIDI
    │
    └─ External Plugins
```

---

## 🔌 Plugin System

FileFusionでは、ファイル形式ごとの処理をプラグインに分離します。

例えばMIDIの場合、

```text
MIDI File
    ↓
MIDI Plugin
    ↓
MIDI Parser
    ↓
MIDI Viewer
    ↓
ピアノロール + MIDI再生
```

という構造になっています。

プラグインを追加することで、FileFusion本体を大きく変更せずに新しいファイル形式へ対応できます。

---

## 📋 対応状況

### 🎵 現在対応

#### MIDI

- MID
- MIDI

MIDI以外のファイル形式については、今後プラグインとして追加していく予定です。

---

## 🗺️ 対応予定

### Web

- HTML
- MHTML
- CSS
- XSL
- Markdown

### 文書

- TXT
- DOC
- DOCX
- XLS
- XLSX
- PPT
- PPTX
- RTF
- PDF

### 画像

- BMP
- GIF
- ICO
- JPG
- PNG
- TIFF
- WebP

### 音声

- AAC
- AIFF
- AU
- M4A
- MP3
- WAV
- WMA

### 動画

- 3GP
- AVI
- FLV
- MOV
- MPEG
- MP4
- WebM
- WMV

### アーカイブ

- 7Z
- BZ2
- GZ
- LZH
- RAR
- TAR
- ZIP

### その他

今後さらに追加予定です。

---

## 🚧 Version 1.0.1

v1.0.1では、FileFusionのプラグイン基盤にMIDI対応を追加しました。

### v1.0.0

- Core
- Plugin Manager
- Plugin API
- File Detector
- Viewer基盤
- GUI
- サンプルPlugin
- テスト

### v1.0.1

- MIDI Plugin
- MIDI Parser
- MIDI Player
- MIDI Viewer
- ピアノロール表示
- MIDI再生
- MIDI出力デバイス選択
- シーク・一時停止・停止
- 再生処理の軽量化
- 再生タイミングの安定化

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

FileFusionでは、外部プラグインを追加できる構造を目指しています。

プラグインの開発方法については、

`docs/PLUGIN.md`

を参照してください。

---

## 📁 Project Structure

```text
open/
├─ main.py
├─ requirements.txt
├─ README.md
│
├─ core/
│   ├─ application.py
│   ├─ plugin.py
│   ├─ plugin_manager.py
│   ├─ file_info.py
│   ├─ file_detector.py
│   ├─ viewer.py
│   └─ exceptions.py
│
├─ ui/
│   ├─ main_window.py
│   └─ widgets/
│
├─ plugins/
│   └─ builtin/
│       ├─ example/
│       └─ midi/
│
├─ tests/
│
└─ docs/
    └─ PLUGIN.md
```

---

## 🛠️ Technology

- Python
- PySide6
- Mido
- python-rtmidi

---

## 📜 License

MIT License