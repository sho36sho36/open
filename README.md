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
- 🚀 必要な機能だけをプラグインとして追加
- 🛠 外部プラグインへの拡張を想定
- 🐍 Python製

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
    └─ External Plugins
```

---

## 🔌 Plugin System

FileFusionでは、ファイル形式ごとの処理をプラグインに分離します。

例えば、

```text
MIDI
 ↓
MIDI Plugin
 ↓
専用GUI
 ↓
落下ノーツ + 鍵盤
```

という構造にできます。

---

## 📋 対応予定

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
- MIDI
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

## 🚧 Version 1.0.0

v1.0.0では、ファイル形式そのものへの対応よりも、拡張可能なプラグイン基盤を実装しています。

現在含まれているもの：

- Core
- Plugin Manager
- Plugin API
- File Detector
- Viewer基盤
- GUI
- サンプルPlugin
- テスト

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

詳しくは、

`docs/PLUGIN.md`

を参照してください。

---

## 📜 License

MIT License