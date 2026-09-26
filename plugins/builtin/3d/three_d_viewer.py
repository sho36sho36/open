import json
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

import pyvista as pv
from pyvistaqt import QtInteractor
import trimesh


class ThreeDViewer(QWidget):
    """3Dモデルを表示するViewer。"""

    SUPPORTED_EXTENSIONS = {
        ".obj",
        ".stl",
        ".glb",
        ".gltf",
        ".ply",
        ".3ds",
        ".dae",
    }

    def __init__(
        self,
        file_info,
        parent=None,
    ):
        super().__init__(parent)

        self.file_info = file_info
        self.path = Path(file_info.path)

        self.plotter = None
        self.meshes = []

        self.info_label = QLabel()

        self._setup_ui()
        self._load_model()

    # ==================================================
    # UI
    # ==================================================

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)

        header_layout = QHBoxLayout()

        title = QLabel(
            f"🧊 3D Viewer - {self.path.name}"
        )

        title.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        header_layout.addWidget(title)
        header_layout.addStretch()

        self.reset_button = QPushButton(
            "表示をリセット"
        )

        self.wireframe_button = QPushButton(
            "ワイヤーフレーム"
        )

        self.points_button = QPushButton(
            "頂点表示"
        )

        self.reload_button = QPushButton(
            "再読み込み"
        )

        header_layout.addWidget(
            self.reset_button
        )

        header_layout.addWidget(
            self.wireframe_button
        )

        header_layout.addWidget(
            self.points_button
        )

        header_layout.addWidget(
            self.reload_button
        )

        main_layout.addLayout(
            header_layout
        )

        self.info_label.setText(
            "読み込み中..."
        )

        main_layout.addWidget(
            self.info_label
        )

        self.plotter = QtInteractor(
            self
        )

        self.plotter.set_background(
            "#202124"
        )

        main_layout.addWidget(
            self.plotter.interactor
        )

        self.reset_button.clicked.connect(
            self._reset_camera
        )

        self.wireframe_button.clicked.connect(
            self._toggle_wireframe
        )

        self.points_button.clicked.connect(
            self._toggle_points
        )

        self.reload_button.clicked.connect(
            self._reload
        )

    # ==================================================
    # Load
    # ==================================================

    def _load_model(self):
        extension = self.path.suffix.lower()

        if extension not in self.SUPPORTED_EXTENSIONS:
            self._show_error(
                "対応していない3D形式です。"
            )
            return

        try:
            scene = trimesh.load(
                self.path,
                force="scene",
                process=False,
            )

            self._display_scene(
                scene
            )

        except Exception as exc:
            self._show_error(
                "3Dモデルを読み込めませんでした。",
                exc,
            )

    # ==================================================
    # Scene
    # ==================================================

    def _display_scene(
        self,
        scene,
    ):
        self._clear_scene()

        geometry = self._extract_geometry(
            scene
        )

        if not geometry:
            self._show_error(
                "3Dモデル内に表示可能な"
                "メッシュがありません。"
            )
            return

        total_vertices = 0
        total_faces = 0

        for index, mesh in enumerate(
            geometry
        ):
            try:
                vertices = mesh.vertices
                faces = mesh.faces

                if (
                    vertices is None
                    or faces is None
                    or len(vertices) == 0
                    or len(faces) == 0
                ):
                    continue

                points = pv.PolyData(
                    vertices
                )

                vtk_faces = []

                for face in faces:
                    if len(face) != 3:
                        continue

                    vtk_faces.extend(
                        [
                            3,
                            int(face[0]),
                            int(face[1]),
                            int(face[2]),
                        ]
                    )

                if not vtk_faces:
                    continue

                points.faces = vtk_faces

                actor = self.plotter.add_mesh(
                    points,
                    name=f"mesh_{index}",
                    show_edges=False,
                    smooth_shading=True,
                )

                self.meshes.append(
                    {
                        "mesh": points,
                        "actor": actor,
                    }
                )

                total_vertices += len(
                    vertices
                )

                total_faces += len(
                    faces
                )

            except Exception:
                continue

        if not self.meshes:
            self._show_error(
                "3Dメッシュを表示できませんでした。"
            )
            return

        self.plotter.reset_camera()

        self.info_label.setText(
            f"ファイル: {self.path.name}    "
            f"メッシュ: {len(self.meshes):,}    "
            f"頂点: {total_vertices:,}    "
            f"面: {total_faces:,}"
        )

        self.plotter.render()

    # ==================================================
    # Geometry
    # ==================================================

    @staticmethod
    def _extract_geometry(scene):
        geometry = []

        if isinstance(
            scene,
            trimesh.Trimesh,
        ):
            geometry.append(scene)

            return geometry

        if isinstance(
            scene,
            trimesh.Scene,
        ):
            for mesh in scene.geometry.values():
                if isinstance(
                    mesh,
                    trimesh.Trimesh,
                ):
                    geometry.append(mesh)

        return geometry

    # ==================================================
    # Controls
    # ==================================================

    def _reset_camera(self):
        if self.plotter is None:
            return

        self.plotter.reset_camera()
        self.plotter.render()

    def _toggle_wireframe(self):
        for item in self.meshes:
            actor = item["actor"]

            try:
                property_object = (
                    actor.GetProperty()
                )

                current_representation = (
                    property_object.GetRepresentation()
                )

                if current_representation == 2:
                    property_object.SetRepresentationToSurface()

                else:
                    property_object.SetRepresentationToWireframe()

            except Exception:
                continue

        self.plotter.render()

    def _toggle_points(self):
        for item in self.meshes:
            actor = item["actor"]

            try:
                property_object = (
                    actor.GetProperty()
                )

                current_visibility = (
                    property_object.GetVertexVisibility()
                )

                if current_visibility:
                    property_object.VertexVisibilityOff()

                else:
                    property_object.VertexVisibilityOn()

                    property_object.SetPointSize(
                        5
                    )

            except Exception:
                continue

        self.plotter.render()

    # ==================================================
    # Reload
    # ==================================================

    def _reload(self):
        self._load_model()

    # ==================================================
    # Cleanup
    # ==================================================

    def _clear_scene(self):
        self.meshes.clear()

        if self.plotter is not None:
            try:
                self.plotter.clear()

            except Exception:
                pass

    def _show_error(
        self,
        message,
        exception=None,
    ):
        if exception is not None:
            message = (
                f"{message}\n\n"
                f"{exception}"
            )

        self.info_label.setText(
            message
        )

        QMessageBox.warning(
            self,
            "3D Plugin",
            message,
        )

    def closeEvent(self, event):
        if self.plotter is not None:
            try:
                self.plotter.close()

            except Exception:
                pass

        super().closeEvent(
            event
        )