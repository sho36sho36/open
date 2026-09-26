# open 🇯🇵

さまざまなファイルを、ひとつのアプリで開くためのファイルビューアです。

「ファイルを開く」を、もっとシンプルに。

---

## ✨ Features

* 🖥️ GUIファイルビューア
* 🧩 プラグイン方式
* 🔍 拡張子による自動判定
* 🪟 ファイル種類ごとの専用GUI
* 🎵 MIDI再生・ピアノロール表示
* 🔊 音声再生
* 🖼️ 画像表示
* 🎬 動画再生
* 📝 テキスト・コード表示
* 📕 PDF表示
* 📦 圧縮ファイル表示・展開
* 📊 Office / OpenDocument対応
* 🗄️ データファイル表示
* 🔌 外部プラグイン対応

---

# 📂 対応ファイル

## 🎵 MIDI

対応拡張子:

```text
.mid
.midi
```

MIDIファイルを読み込み、ノートを視覚的に表示しながら再生できます。

---

## 🔊 Audio

対応拡張子:

```text
.wav
.mp3
.m4a
.aac
.flac
.ogg
.aiff
.aif
.au
```

音声ファイルを専用プレイヤーで再生できます。

---

## 🖼️ Image

対応拡張子:

```text
.png
.jpg
.jpeg
.gif
.bmp
.webp
.tiff
.tif
.ico
```

画像を表示できます。

---

## 🎬 Video

対応拡張子:

```text
.mp4
.mkv
.webm
.avi
.mov
.wmv
.flv
.mpeg
.mpg
.m4v
```

動画を専用Viewerで再生できます。

---

## 📝 Text / Code

テキストファイルやプログラムコードを表示できます。

対応例:

```text
.txt
.log
.csv
.tsv
.ini
.cfg
.conf
.properties
.md
.markdown

.py
.pyw
.js
.jsx
.ts
.tsx
.mjs
.cjs

.html
.htm
.css
.scss
.sass
.less

.json
.xml
.yaml
.yml
.toml

.c
.h
.cc
.cpp
.cxx
.hpp

.java
.kt
.kts
.cs
.go
.rs
.swift
.dart
.lua
.rb
.php
.r
.sql

.sh
.bash
.zsh
.bat
.cmd
.ps1

.asm
.v
.vhd
.vhdl
```

通常のテキストはそのまま表示し、コードは構文に合わせて色分けして表示します。

---

## 📕 PDF

対応拡張子:

```text
.pdf
```

PDFをページ単位で表示できます。

---

# 📦 Archive

対応拡張子:

```text
.zip
.7z
.tar
.gz
.bz2
.xz
.rar
.cab
```

Archive Pluginで圧縮ファイルの内容を確認できます。

対応形式はひとつのArchive Pluginにまとめています。

---

# 📊 Office / OpenDocument

## Spreadsheet

```text
.xlsx
.ods
```

複数シートをタブで切り替えて表示できます。

## Document

```text
.docx
.odt
.rtf
```

文書の内容を読み取り専用で表示できます。

## Presentation

```text
.pptx
.odp
```

スライドをタブ形式で確認できます。

### ❌ 対象外

旧バイナリOffice形式は対象外です。

```text
.xls
.doc
.ppt
```

---

# 🗄️ Data

v2.0.2でデータファイルに対応しました。

対応拡張子:

```text
.db
.sqlite
.sqlite3
.parquet
.jsonl
.ndjson
```

## SQLite

```text
.db
.sqlite
.sqlite3
```

SQLiteデータベースを読み取り専用で開けます。

* テーブル一覧
* テーブル選択
* データ表示
* 行数表示
* 列数表示

に対応しています。

## Parquet

```text
.parquet
```

Parquetデータを表形式で表示できます。

## JSON Lines / NDJSON

```text
.jsonl
.ndjson
```

1行1JSON形式のデータを読み込み、表形式で表示できます。

---

# 🧩 Plugin System

openでは、ファイル形式ごとの機能をPluginとして分離しています。

```text
ファイル
   ↓
FileDetector
   ↓
PluginManager
   ↓
対応するPlugin
   ↓
専用Viewer
```

各Pluginは独立しているため、新しいファイル形式を追加しやすい構造になっています。

---

# 🏗️ Architecture

```text
open/
│
├─ main.py
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
│  │  ├─ midi/
│  │  ├─ audio/
│  │  ├─ image/
│  │  ├─ video/
│  │  ├─ text/
│  │  ├─ pdf/
│  │  ├─ archive/
│  │  ├─ office/
│  │  └─ data/
│  │
│  └─ external/
│
└─ tests/
```

---

# 🔌 External Plugins

`plugins/external/` にPluginを配置することで、標準Pluginとは別に機能を追加できます。

基本的なPlugin:

```python
from core.plugin import FilePlugin


class ExamplePlugin(FilePlugin):

    name = "Example Plugin"
    version = "1.0.0"

    extensions = [
        ".example"
    ]

    def create_viewer(
        self,
        file_info,
        parent=None
    ):
        ...
```

---

# 🛠️ Technologies

openは主に以下の技術を使用しています。

* Python
* PySide6
* mido
* python-rtmidi
* PyMuPDF
* openpyxl
* python-docx
* python-pptx
* odfpy
* py7zr
* rarfile
* pyarrow

---

# 📦 Installation

Pythonをインストールした環境で、

```powershell
py -m pip install -r requirements.txt
```

実行:

```powershell
py main.py
```

---

# 🧪 Tests

テストを実行:

```powershell
py -m unittest discover
```

---

# 🗺️ Roadmap

| Version    | 内容                  | 主な拡張子                                                    |
| ---------- | ------------------- | -------------------------------------------------------- |
| **v1.0.0** | 🧩 Plugin Framework | —                                                        |
| **v1.0.1** | 🎵 MIDI             | `.mid` `.midi`                                           |
| **v1.1.0** | 🔊 Audio            | `.wav` `.mp3` `.flac` `.ogg`                             |
| **v1.2.0** | 🖼️ Image           | `.png` `.jpg` `.gif` `.webp`                             |
| **v1.3.0** | 🎬 Video            | `.mp4` `.mkv` `.webm` `.avi`                             |
| **v1.4.0** | 📝 Text / Code      | `.txt` `.py` `.js` `.json` ...                           |
| **v1.5.0** | 📕 PDF              | `.pdf`                                                   |
| **v1.6.0** | 📦 Archive          | `.zip`                                                   |
| **v2.0.0** | 📊 Office           | `.xlsx` `.ods` `.docx` `.odt` `.rtf` `.pptx` `.odp`      |
| **v2.0.1** | 📦 Archive拡張        | `.7z` `.tar` `.gz` `.bz2` `.xz` `.rar` `.cab`            |
| **v2.0.2** | 🗄️ Data            | `.db` `.sqlite` `.sqlite3` `.parquet` `.jsonl` `.ndjson` |
| **v2.1.0** | 🧊 3D               | `.obj` `.stl` `.glb` `.gltf` `.ply` `.3ds` `.dae`        |
| **v2.2.0** | 🎨 Design / Vector  | `.svg` `.eps` `.ai` `.psd` `.xcf` `.kra`                 |

---

# 📚 Version History

## v2.0.2

🗄️ Data Pluginを追加。

* SQLite対応
* Parquet対応
* JSONL対応
* NDJSON対応
* 表形式Viewer
* SQLiteテーブル選択
* 読み取り専用表示
* 大量データ向け読み込み上限

## v2.0.1

📦 Archive Pluginを拡張。

* `.7z`
* `.tar`
* `.gz`
* `.bz2`
* `.xz`
* `.rar`
* `.cab`

に対応。

## v2.0.0

📊 Office / OpenDocument対応を追加。

* Spreadsheet
* Document
* Presentation

に対応。

## v1.6.0

📦 Archive Pluginを追加。

## v1.5.0

📕 PDF Pluginを追加。

## v1.4.0

📝 Text / Code Pluginを追加。

## v1.3.0

🎬 Video Pluginを追加。

## v1.2.0

🖼️ Image Pluginを追加。

## v1.1.0

🔊 Audio Pluginを追加。

## v1.0.1

🎵 MIDI Pluginを追加。

## v1.0.0

🧩 Plugin Frameworkを完成。

---

# 📄 License

MIT License
