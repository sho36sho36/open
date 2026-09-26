from core.plugin import FilePlugin

from .three_d_viewer import ThreeDViewer


class ThreeDPlugin(FilePlugin):
    """3Dモデルを表示するプラグイン。"""

    name = "3D Plugin"
    version = "2.1.0"

    description = (
        "OBJ、STL、GLB、glTF、PLY、3DS、"
        "DAEなどの3Dモデルを表示します。"
    )

    extensions = [
        ".obj",
        ".stl",
        ".glb",
        ".gltf",
        ".ply",
        ".3ds",
        ".dae",
    ]

    def create_viewer(
        self,
        file_info,
        parent=None,
    ):
        return ThreeDViewer(
            file_info,
            parent,
        )