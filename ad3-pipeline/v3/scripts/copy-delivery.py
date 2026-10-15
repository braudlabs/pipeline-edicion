from pathlib import Path
import shutil
V=Path(__file__).resolve().parents[1];D=Path((V/'destination.txt').read_text());shutil.copytree(V/'Entrega',D,dirs_exist_ok=True);print(D)
