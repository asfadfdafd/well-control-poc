# scripts/generate_dataset.py
import pandas as pd
import numpy as np

def inject_anomalies(df, n_anoms=10, factor=3.0, random_state=42):
    rng = np.random.RandomState(random_state)
    df = df.copy()
    # Случайно выберем индексы и для них увеличим все численные признаки в n раз
    idx = rng.choice(df.index, size=n_anoms, replace=False)
    for i in idx:
        # умножаем значения признаков на большой коэффициент
        df.loc[i, df.columns != 'timestamp'] *= factor
        df.loc[i, 'label'] = 1
    # у всех остальных метка 0
    df['label'] = df['label'].fillna(0).astype(int)
    return df

def main():
    # Берём исходный CSV с обычными данными
    df = pd.read_csv('data/raw/train.csv')
    # Приведём метки в df
    df['label'] = 0
    # Добавим аномалии
    df_anom = inject_anomalies(df, n_anoms=15, factor=5.0)
    # Сохраним для тренировки + теста
    df_anom.to_csv('data/raw/train_with_anoms.csv', index=False)
    print("Создан файл data/raw/train_with_anoms.csv с явными аномалиями.")

if __name__ == "__main__":
    main()
