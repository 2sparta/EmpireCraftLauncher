from pathlib import Path
import subprocess
import pytest
from tools.channel import build

@pytest.mark.parametrize("conflict", [False, True])
def test_native_artifact_in_source_and_installed_mod_folder(tmp_path, conflict):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    name = "empirecraft-launcher-client-test.jar"
    installed = tmp_path/"mods"/name
    source = tmp_path/"launcher/native/dist"/name
    installed.parent.mkdir(parents=True)
    source.parent.mkdir(parents=True)
    installed.write_bytes(b"release artifact")
    source.write_bytes(b"different artifact" if conflict else b"release artifact")
    subprocess.run(["git", "-C", str(tmp_path), "add", "."], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "fixture"], check=True)
    if conflict:
        with pytest.raises(ValueError, match="Conflicting pack inputs"):
            build("HEAD", tmp_path, "2sparta/EmpireCraftLauncher")
    else:
        manifest = build("HEAD", tmp_path, "2sparta/EmpireCraftLauncher")
        for profile in manifest["profiles"].values():
            assert sum(f["path"] == "mods/"+name for f in profile["files"]) == 1
