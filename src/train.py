from xgboost import XGBRegressor
from src.data import load_cmapss, UTILES

RUL_TOPE = 125


def main():
    df = load_cmapss("data/train_FD001.txt")
    rul = df.groupby("unit")["cycle"].transform("max") - df["cycle"]
    y = rul.clip(upper=RUL_TOPE)

    modelo = XGBRegressor(n_estimators=300, learning_rate=0.05,
                          max_depth=4, random_state=42)
    modelo.fit(df[UTILES], y)
    modelo.save_model("models/xgb_rul.json")
    print("Modelo guardado en models/xgb_rul.json")


if __name__ == "__main__":
    main()