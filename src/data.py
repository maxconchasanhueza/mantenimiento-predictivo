import pandas as pd

COLUMNS = (
    ["unit", "cycle"]
    + [f"setting_{i}" for i in range(1, 4)]
    + [f"s{i}" for i in range(1, 22)]
)
CONSTANTES = ["setting_3", "s1", "s5", "s10", "s16", "s18", "s19"]
UTILES = [c for c in COLUMNS[2:] if c not in CONSTANTES]

def load_cmapss(path):
    """Carga un archivo train/test de C-MAPSS con nombres de columna."""
    return pd.read_csv(path, sep=r"\s+", header=None, names=COLUMNS)