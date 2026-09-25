# FileFusion Plugin Development

FileFusionはプラグイン方式でファイル形式に対応します。

---

## 🔌 基本構造

プラグインは `FilePlugin` を継承します。

```python
from core.plugin import FilePlugin


class MyPlugin(FilePlugin):
    name = "My Plugin"
    version = "1.0.0"

    extensions = [
        ".abc"
    ]

    def create_viewer(self, file_info, parent=None):
        ...
```

---

## 🖥 Viewer

ViewerはPySide6の`QWidget`を使用できます。

```python
from PySide6.QtWidgets import QLabel


def create_viewer(self, file_info, parent=None):
    return QLabel(
        f"Opened: {file_info.name}",
        parent
    )
```

---

## 📁 複数の拡張子

1つのプラグインで複数の拡張子に対応できます。

```python
extensions = [
    ".mid",
    ".midi",
]
```

---

## 🎵 MIDI Pluginの例

将来的なMIDIプラグインでは、

- 🎹 ピアノ鍵盤
- 🎼 落下ノーツ
- ▶ 再生
- ⏸ 一時停止
- ⏹ 停止
- ⏩ シーク
- 🔊 音量
- 🎚 トラック選択

などの専用GUIを実装できます。

イメージ：

```text
┌─────────────────────────────────────────┐
│ MIDI Player                             │
├─────────────────────────────────────────┤
│        █       █                        │
│        █       █       █                │
│    █   █       █       █                │
│    █   █   █   █       █                │
│    █   █   █   █   █   █                │
│    █   █   █   █   █   █                │
│────█───█───█───█───█───█────────────────│
│ ▓▓  ▓▓  ▓▓  ▓▓  ▓▓  ▓▓  ▓▓              │
│  ▓ ▓ ▓ ▓ ▓ ▓ ▓ ▓ ▓ ▓ ▓ ▓                │
├─────────────────────────────────────────┤
│ ▶  ⏸  ⏹       00:12 / 03:45            │
└─────────────────────────────────────────┘
```

---

## 🖼 画像Pluginの例

画像プラグインでは、

- ズーム
- 回転
- スクロール
- フィット表示
- 拡大・縮小

などを実装できます。

---

## 🎬 動画Pluginの例

動画プラグインでは、

- 再生
- 一時停止
- 停止
- シークバー
- 音量
- フルスクリーン

などを実装できます。

---

## 🏗 設計方針

FileFusion本体は、各ファイル形式の処理を直接実装しません。

```text
FileFusion Core
       │
       ▼
Plugin Manager
       │
       ├── Text Plugin
       ├── Image Plugin
       ├── MIDI Plugin
       ├── Audio Plugin
       ├── Video Plugin
       ├── PDF Plugin
       └── ...
```

各形式の処理とGUIは、それぞれのプラグインに分離します。

これにより、本体を軽量に保ちながら対応形式を増やせます。

---

## 📦 プラグインの基本テンプレート

```python
from PySide6.QtWidgets import QLabel

from core.plugin import FilePlugin


class MyPlugin(FilePlugin):

    name = "My Plugin"
    version = "1.0.0"
    description = "My FileFusion Plugin"

    extensions = [
        ".abc"
    ]

    def create_viewer(self, file_info, parent=None):

        viewer = QLabel(
            f"ファイル: {file_info.name}",
            parent
        )

        return viewer
```

---

## ⚠️ 注意

FileFusionのプラグインはPythonコードとして実行されます。

そのため、信頼できないプラグインをインストールしないでください。

---

## 🚀 今後

FileFusionでは今後、

```text
v1.0.0
  ↓
プラグイン基盤
  ↓
v1.1.0
  ↓
テキスト・画像
  ↓
v1.2.0
  ↓
音声
  ↓
v1.3.0
  ↓
MIDI
  ↓
v1.4.0
  ↓
動画
  ↓
v1.5.0
  ↓
PDF・Office
  ↓
...
```

のように対応形式を拡張していくことを想定しています。