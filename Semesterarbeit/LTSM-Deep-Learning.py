import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import matplotlib.pyplot as plt

# CSV-Datei laden
df = pd.read_csv("KTZH_00001362_00006004.csv")

# Nur "Nitrat"-Analysen auswählen
nitrat_df = df[df["analyt"] == "Nitrat"].copy()
nitrat_df["datum"] = pd.to_datetime(nitrat_df["datum"])
nitrat_df = nitrat_df[["jahr", "kategorie"]]

# Gruppieren nach Jahr und Kategorie
category_per_year = nitrat_df.groupby(["jahr", "kategorie"]).size().unstack(fill_value=0)

# Prognose für jede Kategorie erstellen
predictions = {}
sequence_length = 3
future_years = 3

for category in category_per_year.columns:
    data = category_per_year[category].values.reshape(-1, 1)
    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(data)

    def create_sequences(data, seq_length):
        X, y = [], []
        for i in range(len(data) - seq_length):
            X.append(data[i:i + seq_length])
            y.append(data[i + seq_length])
        return np.array(X), np.array(y)

    X, y = create_sequences(data_scaled, sequence_length)

    if len(X) == 0:
        continue

    model = Sequential([
        LSTM(50, activation='relu', input_shape=(sequence_length, 1)),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs=200, verbose=0)

    input_seq = data_scaled[-sequence_length:]
    future_preds = []

    for _ in range(future_years):
        pred = model.predict(input_seq.reshape(1, sequence_length, 1), verbose=0)
        future_preds.append(pred[0][0])
        input_seq = np.append(input_seq[1:], pred, axis=0)

    predicted_values = scaler.inverse_transform(np.array(future_preds).reshape(-1, 1)).flatten()
    predictions[category] = predicted_values.astype(int)

# Ergebnisse zusammenfassen
last_year = category_per_year.index[-1]
future_index = [last_year + i + 1 for i in range(future_years)]
pred_df = pd.DataFrame(predictions, index=future_index)

# Prognose anzeigen
print("Prognose der Nitrat-Kategorien für die nächsten Jahre:")
print(pred_df)

# Optional: Plot anzeigen
pred_df.plot(marker='o')
plt.title("Prognose der Nitrat-Kategorien")
plt.xlabel("Jahr")
plt.ylabel("Anzahl Proben")
plt.grid(True)
plt.tight_layout()
plt.show()
