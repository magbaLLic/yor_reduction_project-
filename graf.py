import argparse

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def main() -> None:
    parser = argparse.ArgumentParser(description="Saat bazlı yo/yor oran grafiği çizer.")
    parser.add_argument("--girdi-csv", default="saat_sayim.csv", help="Saat sayım CSV dosyası")
    parser.add_argument("--cikti-grafik", default="ratio_plot.png", help="PNG çıktı dosyası")
    parser.add_argument(
        "--oran-tipi",
        default="token",
        choices=["token", "tweet"],
        help="oran hesabı için sütun seçimi (token varsayılan)",
    )
    parser.add_argument(
        "--goster",
        action="store_true",
        default=False,
        help="Grafiği ekranda göster (varsayılan: gösterme, sadece dosyaya yaz)",
    )
    args = parser.parse_args()

    df = pd.read_csv(args.girdi_csv, dtype={"saat": int})

    if args.oran_tipi == "token":
        yo_kolonu = "yo_token" if "yo_token" in df.columns else "yo"
        yor_kolonu = "yor_token" if "yor_token" in df.columns else "yor"
        etiket = "token"
    else:
        yo_kolonu = "yo"
        yor_kolonu = "yor"
        etiket = "tweet"

    payda = (df[yo_kolonu] + df[yor_kolonu]).replace({0: None})
    df["oran"] = df[yo_kolonu] / payda

    sns.set_theme()
    sns.lineplot(data=df, x="saat", y="oran", marker="o")
    plt.title(f'"yo/yor" Orani (Saat Bazli, {etiket})')
    plt.xlabel("Saat")
    plt.ylabel('"yo" orani')
    plt.xticks(range(0, 24))
    plt.tight_layout()
    plt.savefig(args.cikti_grafik, dpi=200)
    if args.goster:
        plt.show()


if __name__ == "__main__":
    main()
