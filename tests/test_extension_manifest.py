import json
from pathlib import Path


EXTENSION_DIR = Path(__file__).parent.parent / "extension"


def test_extension_manifest_references_existing_files() -> None:
    manifest = json.loads((EXTENSION_DIR / "manifest.json").read_text())

    background_path = EXTENSION_DIR / manifest["background"]["service_worker"]
    side_panel_path = EXTENSION_DIR / manifest["side_panel"]["default_path"]
    assert manifest["manifest_version"] == 3
    assert background_path.exists()
    assert side_panel_path.exists()
    assert (EXTENSION_DIR / "popup.html").exists()
    assert (EXTENSION_DIR / "popup.js").exists()
    assert (EXTENSION_DIR / "popup.css").exists()


def test_extension_manifest_can_call_local_api() -> None:
    manifest = json.loads((EXTENSION_DIR / "manifest.json").read_text())

    assert "http://127.0.0.1:8000/*" in manifest["host_permissions"]
    assert "scripting" in manifest["permissions"]
    assert "activeTab" in manifest["permissions"]
    assert "sidePanel" in manifest["permissions"]
