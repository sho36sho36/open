# open 📂

さまざまなファイルを、ひとつのアプリで開くための
Windows向けファイルビューアーです。

プラグイン方式を採用しており、対応ファイル形式を
あとから追加できる設計になっています。

---

## ✨ v3.0.0

v3.0.0では、ファイルをより快適に扱うための
5つの主要機能を追加しました。

### 📑 タブ機能

複数のファイルを同時に開いて、タブで切り替えられます。

- 複数ファイルを同時に表示
- タブ切り替え
- タブを閉じる
- タブの並べ替え
- 同じファイルを重複して開かない

### 🖱 ドラッグ＆ドロップ

Windowsのエクスプローラーからファイルを
openのウィンドウへドラッグ＆ドロップできます。

複数ファイルの同時ドロップにも対応しています。

### 📁 ファイルブラウザ

アプリ内からフォルダを移動し、ファイルを探せます。

- フォルダ移動
- 親フォルダへ移動
- フォルダ選択
- ファイル一覧
- ファイルのダブルクリックで開く
- ファイル一覧の更新

### 🔎 ファイル検索

現在のフォルダ以下を検索できます。

大量のファイルの中から目的のファイルを
すばやく見つけることができます。

### 🧾 エラーログ

アプリの動作状況やエラーをログファイルへ記録します。

ログファイル:

```text
logs/open.log
```

---

# 📂 対応ファイル

openではプラグインによってさまざまなファイル形式に対応しています。

## 🎵 Audio

- `.wav`
- `.mp3`
- `.m4a`
- `.aac`
- `.flac`
- `.ogg`
- `.aiff`
- `.aif`
- `.au`

## 🎹 MIDI

- `.mid`
- `.midi`

## 🖼 Image

- `.png`
- `.jpg`
- `.jpeg`
- `.gif`
- `.bmp`
- `.webp`
- `.tiff`
- `.tif`
- `.ico`

## 🎬 Video

- `.mp4`
- `.mkv`
- `.webm`
- `.avi`
- `.mov`
- `.wmv`
- `.flv`
- `.mpeg`
- `.mpg`
- `.m4v`

## 📝 Text / Code

多数のテキスト・プログラムファイルに対応しています。

例:

- `.txt`
- `.md`
- `.py`
- `.pyw`
- `.js`
- `.jsx`
- `.ts`
- `.tsx`
- `.mjs`
- `.cjs`
- `.html`
- `.css`
- `.json`
- `.xml`
- `.yaml`
- `.yml`
- `.toml`
- `.ini`
- `.cfg`
- `.conf`
- `.c`
- `.cpp`
- `.h`
- `.hpp`
- `.java`
- `.cs`
- `.go`
- `.rs`
- `.php`
- `.rb`
- `.swift`
- `.kt`
- `.sh`
- `.bat`
- `.cmd`
- `.ps1`
- `.asm`
- `.v`
- `.vhd`
- `.vhdl`

## 📄 PDF

- `.pdf`

## 📦 Archive

- `.zip`
- `.7z`
- `.tar`
- `.gz`
- `.bz2`
- `.xz`
- `.rar`
- `.cab`

## 📊 Office / OpenDocument

- `.xlsx`
- `.ods`
- `.docx`
- `.odt`
- `.rtf`
- `.pptx`
- `.odp`

## 🗄 Data

- `.db`
- `.sqlite`
- `.sqlite3`
- `.parquet`
- `.jsonl`
- `.ndjson`

## 🧊 3D

- `.obj`
- `.stl`
- `.glb`
- `.gltf`
- `.ply`
- `.3ds`
- `.dae`

## 🎨 Design / Vector

- `.svg`
- `.eps`
- `.ai`
- `.psd`
- `.xcf`
- `.kra`

---

# 🔌 プラグインシステム

openはプラグイン方式でファイル形式を追加できます。

基本的な構造:

```text
plugins/
└── builtin/
    └── example/
        └── plugin.py
```

プラグインは `FilePlugin` を継承して作成します。

```python
from core.plugin import FilePlugin


class ExamplePlugin(FilePlugin):
    name = "Example Plugin"
    version = "1.0.0"
    description = "Example plugin"
    extensions = [".example"]

    def create_viewer(self, file_info, parent=None):
        ...
```

詳しいプラグイン開発方法については、

```text
docs/PLUGIN.md
```

を参照してください。

---

# 🏗 Architecture

```text
open/
├── main.py
├── requirements.txt
├── README.md
│
├── core/
│   ├── __init__.py
│   ├── application.py
│   ├── exceptions.py
│   ├── file_detector.py
│   ├── file_info.py
│   ├── plugin.py
│   ├── plugin_manager.py
│   └── viewer.py
│
├── ui/
│   ├── __init__.py
│   ├── main_window.py
│   └── widgets/
│       ├── __init__.py
│       └── welcome.py
│
├── plugins/
│   ├── __init__.py
│   └── builtin/
│       ├── example/
│       ├── midi/
│       ├── audio/
│       ├── image/
│       ├── video/
│       ├── text/
│       ├── pdf/
│       ├── archive/
│       ├── office/
│       ├── data/
│       ├── 3d/
│       └── design/
│
├── tests/
│   ├── __init__.py
│   ├── test_file_detector.py
│   └── test_plugin.py
│
├── docs/
│   └── PLUGIN.md
│
└── logs/
    └── open.log
```

---

# 🛠 使用技術

- Python
- PySide6
- Plugin Architecture
- pathlib
- Python Logging
- Git / GitHub

---

# 💻 動作環境

- Windows
- Python 3.12以上を推奨

---

# 📦 インストール

リポジトリを取得します。

```powershell
git clone https://github.com/sho36sho36/open.git
cd open
```

依存パッケージをインストールします。

```powershell
py -m pip install -r requirements.txt
```

---

# ▶ 起動

```powershell
py main.py
```

---

# 🧪 テスト

```powershell
py -m pytest
```

---

# 📝 ログ

アプリケーションのログは、

```text
logs/open.log
```

に保存されます。

PowerShellから確認する場合:

```powershell
Get-Content .\logs\open.log -Encoding UTF8
```

---

# 📈 Version History

## v3.0.0

### Added

- 📑 Tab functionality
- 🖱 Drag & Drop
- 📁 File Browser
- 🔎 File Search
- 🧾 Error Logging

### Improved

- 複数ファイルを扱いやすいUI
- ファイルを開く操作の改善
- アプリケーションのログ記録
- ファイル探索機能の強化

---

## v2.2.0

- 🎨 Design / Vector Plugin追加
- SVG対応
- EPS対応
- AI対応
- PSD対応
- XCF対応
- KRA対応

## v2.1.0

- 🧊 3D Plugin追加
- OBJ対応
- STL対応
- GLB / GLTF対応
- PLY対応
- 3DS対応
- DAE対応

## v2.0.2

- 🗄 Data Plugin追加
- SQLite対応
- Parquet対応
- JSONL対応

## v2.0.1

- 📦 Archive Plugin拡張
- RAR対応
- CAB対応
- その他アーカイブ形式対応

## v2.0.0

- 📊 Office / OpenDocument Plugin追加

## v1.x

- 基本プラグインシステム
- MIDI
- Audio
- Image
- Video
- Text / Code
- PDF
- Archive
- その他ファイル形式への対応

---

# 🗺 Roadmap

今後の開発候補:

- [ ] 最近開いたファイル
- [ ] お気に入り
- [ ] ファイル情報パネル
- [ ] プレビュー機能の強化
- [ ] プラグイン管理UI
- [ ] 設定画面
- [ ] テーマ機能
- [ ] キーボードショートカット
- [ ] より高度な検索
- [ ] 外部プラグインの配布システム

---

# 🤝 Contributing

IssueやPull Requestによる提案・改善を歓迎します。

新しいファイル形式への対応は、
プラグインとして追加することを推奨しています。

---

# 📄 License

MIT License

Copyright (c) 2026 sho36sho36