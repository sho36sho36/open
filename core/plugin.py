from abc import ABC, abstractmethod


class FilePlugin(ABC):
    """
    FileFusionプラグインの基本クラス。

    各プラグインはこのクラスを継承します。
    """

    name = "Unnamed Plugin"
    version = "1.0.0"
    description = ""
    extensions = []

    def can_open(self, file_info):
        """
        このプラグインがファイルを開けるか判定します。
        """

        extension = file_info.extension.lower()

        return extension in [
            ext.lower()
            for ext in self.extensions
        ]

    @abstractmethod
    def create_viewer(self, file_info, parent=None):
        """
        ファイル表示用のGUIを作成します。

        戻り値:
            QWidget
        """
        raise NotImplementedError

    def initialize(self):
        """プラグイン初期化処理。"""
        pass

    def shutdown(self):
        """プラグイン終了処理。"""
        pass

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} "
            f"name={self.name!r} "
            f"version={self.version!r}>"
        )