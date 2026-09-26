# open

**Python製の軽量・プラグイン方式ファイルビューア／プレイヤー**

さまざまな拡張子のファイルを、専用のGUIで表示・再生・操作できるアプリケーションを目指します。

> 「ファイルを開く」を、もっと自由に。

---

## ✨ Features

* 🖥️ 軽量なデスクトップGUI
* 🔌 プラグイン方式
* 📂 拡張子による自動判定
* 🧩 ファイル形式ごとの専用GUI
* 🎵 音声ファイルの再生
* 🎹 MIDIファイルのピアノロール表示・再生
* 🖼️ 画像表示
* 🎬 動画再生
* 📝 テキスト・ソースコード表示
* 📄 PDF表示
* 📦 アーカイブ表示・展開
* 📊 Office / OpenDocument対応
* 🚀 必要な機能だけをプラグインとして追加
* 🛠️ 外部プラグインへの拡張を想定
* 🐍 Python製

---

## 🏗️ Architecture

```text
open
│
├─ Core
│  ├─ File Detector
│  ├─ Plugin Manager
│  ├─ Plugin API
│  ├─ File Information
│  └─ Viewer System
│
├─ UI
│  ├─ Main Window
│  └─ Widgets
│
└─ Plugins
   ├─ Built-in Plugins
   │  ├─ Example
   │  ├─ MIDI
   │  ├─ Audio
   │  ├─ Image
   │  ├─ Video
   │  ├─ Text
   │  ├─ PDF
   │  ├─ Archive
   │  └─ Office
   │
   └─ External Plugins
```

`open` では、ファイル形式ごとの処理をプラグインとして分離しています。

ファイルを開くと、拡張子をもとに対応するプラグインを自動的に検索し、そのプラグインが専用のViewerを作成します。

```text
ファイル
  ↓
File Detector
  ↓
Plugin Manager
  ↓
対応Plugin
  ↓
専用Viewer
  ↓
表示・再生・操作
```

---

## 🔌 Plugin System

`open` は、同じ表示・再生方式を必要とするファイル形式を、できるだけ1つのプラグインにまとめる設計です。

例えば音声ファイルの場合、

```text
WAV / MP3 / M4A / FLAC / OGG / ...
                    ↓
              Audio Plugin
                    ↓
             Audio Viewer
                    ↓
       再生・一時停止・停止
          シーク・音量調整
```

という構成になっています。

ファイル形式ごとに個別のプラグインを作る必要はありません。

---

## 🎹 MIDI Plugin

MIDIファイルを専用のMIDI Pluginで処理します。

### 対応拡張子

* `.mid`
* `.midi`

### 主な機能

* 🎹 ピアノロール表示
* 🎵 ノート表示
* ▶️ 再生
* ⏸️ 一時停止
* ⏹️ 停止
* ⏩ 再生位置操作
* 🔊 MIDI出力選択
* 🎼 鍵盤表示
* 🚀 大きなMIDIファイルを考慮した描画最適化

---

## 🎵 Audio Plugin

一般的な音声ファイルを1つの共通Audio Pluginで処理します。

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

* ▶️ 再生
* ⏸️ 一時停止
* ⏹️ 停止
* ⏩ シーク
* 🔊 音量調整
* ⏱️ 再生時間表示
* 📊 ファイル形式・サイズ表示

Audio Pluginは **PySide6 Qt Multimedia** を利用して音声を再生します。

---

## 🖼️ Image Plugin

画像ファイルを共通のImage Viewerで表示します。

### 対応拡張子

* `.png`
* `.jpg`
* `.jpeg`
* `.gif`
* `.bmp`
* `.webp`
* `.tiff`
* `.tif`
* `.ico`

---

## 🎬 Video Plugin

動画ファイルを共通のVideo Viewerで再生します。

### 対応拡張子

* `.mp4`
* `.mkv`
* `.webm`
* `.avi`
* `.mov`
* `.wmv`
* `.flv`
* `.mpeg`
* `.mpg`
* `.m4v`

---

## 📝 Text / Code Plugin

テキストファイルやソースコードを表示します。

通常のテキストはそのまま表示し、ソースコードは種類に応じた色分け表示を行います。

### Text

* `.txt`
* `.log`
* `.csv`
* `.tsv`
* `.ini`
* `.cfg`
* `.conf`
* `.properties`
* `.md`
* `.markdown`

### Web

* `.html`
* `.htm`
* `.css`
* `.scss`
* `.sass`
* `.less`

### Data / Configuration

* `.json`
* `.xml`
* `.yaml`
* `.yml`
* `.toml`

### Programming

* `.py`
* `.pyw`
* `.js`
* `.jsx`
* `.ts`
* `.tsx`
* `.mjs`
* `.cjs`
* `.c`
* `.h`
* `.cc`
* `.cpp`
* `.cxx`
* `.hpp`
* `.java`
* `.kt`
* `.kts`
* `.cs`
* `.go`
* `.rs`
* `.swift`
* `.dart`
* `.lua`
* `.rb`
* `.php`
* `.r`
* `.sql`

### Shell / Script

* `.sh`
* `.bash`
* `.zsh`
* `.bat`
* `.cmd`
* `.ps1`

### Other

* `.asm`
* `.v`
* `.vhd`
* `.vhdl`

---

## 📄 PDF Plugin

PDFファイルを表示します。

### 対応拡張子

* `.pdf`

PDFのページをViewer上で表示できます。

---

## 📦 Archive Plugin

圧縮・アーカイブファイルを共通のArchive Viewerで扱います。

### 対応拡張子

* `.zip`
* `.7z`
* `.tar`
* `.gz`
* `.bz2`
* `.xz`
* `.rar`
* `.cab`

### 主な機能

* 📂 アーカイブ内ファイル一覧
* 📁 フォルダー表示
* 📊 ファイルサイズ表示
* 🏷️ ファイル種類表示
* 📤 アーカイブの展開
* 🔄 再読み込み

形式によって内部の処理方式は異なりますが、ユーザーからは共通のArchive Viewerとして扱える設計になっています。

---

## 📊 Office / OpenDocument Plugin

Microsoft OfficeおよびOpenDocument形式のファイルを表示します。

### 📊 Spreadsheet

**対応拡張子**

* `.xlsx`
* `.ods`

複数シートをタブで表示できます。

### 📝 Document

**対応拡張子**

* `.docx`
* `.odt`
* `.rtf`

### 📽️ Presentation

**対応拡張子**

* `.pptx`
* `.odp`

PowerPoint / OpenDocument Presentationのスライドをタブ形式で確認できます。

### ❌ 対象外の旧Office形式

以下の旧バイナリOffice形式は対象外です。

* `.xls`
* `.doc`
* `.ppt`

`open` では、現在のOffice / OpenDocument形式を中心に対応しています。

---

## 📋 対応形式一覧

| Plugin           | 拡張子                                                                                                         |
| ---------------- | ----------------------------------------------------------------------------------------------------------- |
| 🎹 MIDI          | `.mid` `.midi`                                                                                              |
| 🎵 Audio         | `.wav` `.mp3` `.m4a` `.aac` `.flac` `.ogg` `.aiff` `.aif` `.au`                                             |
| 🖼️ Image        | `.png` `.jpg` `.jpeg` `.gif` `.bmp` `.webp` `.tiff` `.tif` `.ico`                                           |
| 🎬 Video         | `.mp4` `.mkv` `.webm` `.avi` `.mov` `.wmv` `.flv` `.mpeg` `.mpg` `.m4v`                                     |
| 📝 Text / Code   | `.txt` `.log` `.csv` `.tsv` `.md` `.json` `.xml` `.yaml` `.yml` `.toml` `.py` `.js` `.ts` `.html` `.css` など |
| 📄 PDF           | `.pdf`                                                                                                      |
| 📦 Archive       | `.zip` `.7z` `.tar` `.gz` `.bz2` `.xz` `.rar` `.cab`                                                        |
| 📊 Spreadsheet   | `.xlsx` `.ods`                                                                                              |
| 📝 Document      | `.docx` `.odt` `.rtf`                                                                                       |
| 📽️ Presentation | `.pptx` `.odp`                                                                                              |

---

## 🏗️ Project Structure

```text
open/
│
├─ main.py
├─ requirements.txt
├─ README.md
│
├─ core/
│  ├─ __init__.py
│  ├─ application.py
│  ├─ plugin.py
│  ├─ plugin_manager.py
│  ├─ file_info.py
│  ├─ file_detector.py
│  ├─ viewer.py
│  └─ exceptions.py
│
├─ ui/
│  ├─ __init__.py
│  ├─ main_window.py
│  └─ widgets/
│     ├─ __init__.py
│     └─ welcome.py
│
├─ plugins/
│  ├─ __init__.py
│  │
│  ├─ builtin/
│  │  ├─ __init__.py
│  │  │
│  │  ├─ example/
│  │  │  ├─ __init__.py
│  │  │  └─ plugin.py
│  │  │
│  │  ├─ midi/
│  │  │  ├─ __init__.py
│  │  │  ├─ plugin.py
│  │  │  ├─ midi_parser.py
│  │  │  ├─ midi_player.py
│  │  │  └─ midi_viewer.py
│  │  │
│  │  ├─ audio/
│  │  │  ├─ __init__.py
│  │  │  ├─ plugin.py
│  │  │  └─ audio_viewer.py
│  │  │
│  │  ├─ image/
│  │  │  ├─ __init__.py
│  │  │  ├─ plugin.py
│  │  │  └─ image_viewer.py
│  │  │
│  │  ├─ video/
│  │  │  ├─ __init__.py
│  │  │  ├─ plugin.py
│  │  │  └─ video_viewer.py
│  │  │
│  │  ├─ text/
│  │  │  ├─ __init__.py
│  │  │  ├─ plugin.py
│  │  │  └─ text_viewer.py
│  │  │
│  │  ├─ pdf/
│  │  │  ├─ __init__.py
│  │  │  ├─ plugin.py
│  │  │  └─ pdf_viewer.py
│  │  │
│  │  ├─ archive/
│  │  │  ├─ __init__.py
│  │  │  ├─ plugin.py
│  │  │  └─ archive_viewer.py
│  │  │
│  │  └─ office/
│  │     ├─ __init__.py
│  │     ├─ plugin.py
│  │     └─ office_viewer.py
│  │
│  └─ external/
│
├─ tests/
│  ├─ __init__.py
│  ├─ test_file_detector.py
│  └─ test_plugin.py
│
└─ docs/
   └─ PLUGIN.md
```

---

## 🛠️ Technologies

`open` は以下の技術を使用しています。

* Python
* PySide6
* Qt Multimedia
* Mido
* python-rtmidi
* PyMuPDF
* openpyxl
* python-docx
* python-pptx
* odfpy
* py7zr
* rarfile

---

## 🚧 Roadmap

今後も、同じ表示方式・操作方式のファイル形式をまとめてプラグインとして追加していく予定です。

| Version    | 内容                 | 主な拡張子                                                    |
| ---------- | ------------------ | -------------------------------------------------------- |
| **v2.0.0** | 📊 Office          | `.xlsx` `.ods` `.docx` `.odt` `.rtf` `.pptx` `.odp`      |
| **v2.0.1** | 📦 Archive拡張       | `.7z` `.tar` `.gz` `.bz2` `.xz` `.rar` `.cab`            |
| **v2.0.2** | 🗄️ Data           | `.db` `.sqlite` `.sqlite3` `.parquet` `.jsonl` `.ndjson` |
| **v2.1.0** | 🧊 3D              | `.obj` `.stl` `.glb` `.gltf` `.ply` `.3ds` `.dae`        |
| **v2.2.0** | 🎨 Design / Vector | `.svg` `.eps` `.ai` `.psd` `.xcf` `.kra`                 |

---

## 🚧 Future Ideas

今後の候補:

* 📚 電子書籍
* 💬 字幕
* 💿 ディスクイメージ
* 🗄️ データベース
* 🧊 3Dモデル
* 🎨 デザインファイル
* 📐 CAD
* 🔬 科学データ
* 🔌 外部Plugin APIの拡張
* 🌐 Web版

---

## 📜 Version History

### v2.0.1

**📦 Archive Plugin拡張**

* 7Z対応
* TAR対応
* GZ対応
* BZ2対応
* XZ対応
* RAR対応
* CAB形式の検出対応
* Archive Viewerを拡張
* アーカイブ形式ごとの共通Viewer化

### v2.0.0

**📊 Office / OpenDocument Plugin追加**

#### Spreadsheet

* `.xlsx`
* `.ods`

#### Document

* `.docx`
* `.odt`
* `.rtf`

#### Presentation

* `.pptx`
* `.odp`

#### 主な機能

* 複数シートのタブ表示
* PowerPointスライドのタブ表示
* OpenDocument対応
* 日本語ファイルの表示
* 読み取り専用ビューア
* 再読み込み機能

旧バイナリOffice形式の `.xls` `.doc` `.ppt` は対象外です。

### v1.6.0

**📦 Archive Plugin追加**

* ZIPファイル対応
* アーカイブ内ファイル一覧
* フォルダー表示
* ファイルサイズ表示
* ファイル種類表示
* アーカイブ展開
* 再読み込み

### v1.5.0

**📄 PDF Plugin追加**

* PDFファイル対応
* PDFページ表示
* PDF Viewer追加

### v1.4.0

**📝 Text / Code Plugin追加**

* テキストファイル対応
* ソースコード対応
* コードの色分け表示
* 各種設定ファイル対応
* Webファイル対応
* プログラミング言語対応

### v1.3.0

**🎬 Video Plugin追加**

* 動画ファイル対応
* 共通Video Viewer追加
* 動画再生
* 再生操作

### v1.2.0

**🖼️ Image Plugin追加**

* 画像ファイル対応
* PNG
* JPEG
* GIF
* BMP
* WebP
* TIFF
* ICO
* 共通Image Viewer追加

### v1.1.0

**🎵 Audio Plugin追加**

* 共通Audio Pluginを追加
* WAV / MP3などの音声ファイルに対応
* 再生
* 一時停止
* 停止
* シーク
* 音量調整
* 再生時間表示
* Qt Multimediaによる音声再生

### v1.0.1

**🎹 MIDI Plugin追加**

* MIDIファイル対応
* MIDI解析
* ピアノロール表示
* MIDI再生
* MIDI出力選択
* 鍵盤表示

### v1.0.0

**🎉 Initial Release**

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

リポジトリを取得したあと、必要なライブラリをインストールします。

```bash
pip install -r requirements.txt
```

---

## ▶️ Run

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

外部プラグインの開発については、

```text
docs/PLUGIN.md
```

を参照してください。

`open` はプラグインを追加することで、新しいファイル形式や機能を拡張できる設計になっています。

---

## 📄 License

MIT License
