import matplotlib.pyplot as plt
import re
import pandas as pd
from pathlib import Path

# veriyi yükle
data_path = Path(__file__).with_name("fake_faker.json.gz")
df = pd.read_json(data_path, compression="gzip", lines=True)

# regex patternleri
pattern_yo = r"\b\w+[ıiuü]yo\b"
pattern_yor = r"\b\w+[ıiuü]yor\b"

# saat çıkar
df["created_at"] = pd.to_datetime(df["created_at"])
df["hour"] = df["created_at"].dt.hour

# sayım
df["yo_count"] = df["text"].str.count(pattern_yo)
df["yor_count"] = df["text"].str.count(pattern_yor)

# saatlik grupla
grouped = df.groupby("hour")[["yo_count", "yor_count"]].sum()

# oran hesapla
grouped["ratio"] = grouped["yo_count"] / (grouped["yo_count"] + grouped["yor_count"])

# grafik
plt.figure()
grouped["ratio"].plot(kind="bar")

plt.xlabel("Saat")
plt.ylabel("yo / (yo + yor)")
plt.title("-yo Varyasyonu (Saatlik Dağılım)")

plt.show()

total_yo = df["yo_count"].sum()
total_yor = df["yor_count"].sum()

plt.figure()
plt.bar(["yo", "yor"], [total_yo, total_yor])

plt.title("Toplam Frekans Karşılaştırması")
plt.ylabel("Frekans")

plt.show()
