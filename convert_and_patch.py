"""Convert horse_human_model.h5 -> tfjs et corrige model.json (Keras 3 -> tfjs).

Usage (depuis la racine du projet, venv actif) :
    python convert_and_patch.py
"""
import json, shutil, subprocess, sys
from pathlib import Path

H5 = Path("horse_human_model.h5")
#OUT = Path("docs/tfjs_model")
OUT = Path("tfjs_model")


def fix(o):
    if isinstance(o, dict):
        if "batch_shape" in o:
            o["batch_input_shape"] = o.pop("batch_shape")
        d = o.get("dtype")
        if isinstance(d, dict) and d.get("class_name") == "DTypePolicy":
            o["dtype"] = d["config"]["name"]
        for v in o.values():
            fix(v)
    elif isinstance(o, list):
        for v in o:
            fix(v)


def patch(path: Path):
    m = json.loads(path.read_text())
    fix(m["modelTopology"])
    for g in m["weightsManifest"]:
        for w in g["weights"]:
            w["name"] = w["name"].replace("sequential/", "", 1)
    path.write_text(json.dumps(m))
    layers = m["modelTopology"]["model_config"]["config"]["layers"]
    shape = layers[0]["config"]["batch_input_shape"]
    print(f"OK - input {shape}, {sum(l['class_name']=='Conv2D' for l in layers)} blocs Conv2D")
    print(f"=> dans le HTML : .resizeBilinear([{shape[1]}, {shape[2]}])")


if __name__ == "__main__":
    if not H5.exists():
        sys.exit(f"Introuvable : {H5} (rendez d'abord Part3.qmd)")
    if OUT.exists():
        shutil.rmtree(OUT)
    subprocess.run(
        ["tensorflowjs_converter", "--input_format=keras", str(H5), str(OUT)],
        check=True,
    )
    patch(OUT / "model.json")
