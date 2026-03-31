import argparse
import csv
import gzip
import json
import logging
import re
from datetime import datetime
from typing import Set

from tqdm import tqdm


def saat_sayisini_ayikla(created_at: str) -> str:
    """`created_at` alanından saat (00-23) döndürür."""
    # Varsayılan format: "%Y-%m-%d %H:%M:%S"
    try:
        dt = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
        return f"{dt.hour:02d}"
    except (ValueError, TypeError):
        # Eski/garip formatlar için kaba fallback
        if isinstance(created_at, str) and len(created_at) >= 13:
            return created_at[11:13]
        return "00"


def metin_i_brak_mi(
    text: str,
    on_elemeden_gec: bool,
    on_elemede_kullanilan_karakterler: Set[str],
) -> bool:
    """
    Regex'i hızlandırmak için ön-eleme uygular.
    - on-eleme kapalıysa direkt True.
    - on-eleme açıksa, regex'in aradığı ana harf kümesinden en az biri geçmeli.
    """
    if not on_elemeden_gec:
        return True
    return any(karakter in text for karakter in on_elemede_kullanilan_karakterler)


def main() -> None:
    parser = argparse.ArgumentParser(description="Türkçe tweetlerde yo/yor sayımı yapar.")
    parser.add_argument("--dosya", default="fake_simple.json.gz", help="GZip JSONL tweet dosyası")
    parser.add_argument("--cikti-csv", default="saat_sayim.csv", help="Saat bazlı sayım CSV çıktısı")
    parser.add_argument(
        "--on-eleme-kapali",
        action="store_true",
        default=False,
        help="Regex aday ön-elemesini kapat (varsayılan: açık).",
    )
    parser.add_argument(
        "--on-eleme-karakterleri",
        default="ıiuü",
        help="Ön-eleme için aranan karakter kümesi (varsayılan: ıiuü)",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    # Token-level yaklaşıma yakın sayım için:
    # - RE_YOR: "....(ı/i/u/ü)yor" ile biten kelimeler
    # - RE_YO : "....(ı/i/u/ü)yo" ve opsiyonel "yo'" ile biten kelimeler
    #
    # Not: Sona yakın `\b` kullanımı "yo'" gibi durumlarda kaçabilir; bu yüzden lookahead ile (W veya $) kontrol ediliyor.
    DESENE_YOR = re.compile(r"\b\w*[ıiuü]yor(?=\W|$)", re.I | re.UNICODE)
    DESENE_YO = re.compile(r"\b\w*[ıiuü]yo'?(?=\W|$)", re.I | re.UNICODE)

    on_elemede_kullanilan_karakterler = set(args.on_eleme_karakterleri)
    on_elemeden_gec = not args.on_eleme_kapali

    # tweet-level ve token-level sayımlar ayrı tutulur.
    yo_tweet_sayisi = [0] * 24
    yor_tweet_sayisi = [0] * 24
    yo_token_sayisi = [0] * 24
    yor_token_sayisi = [0] * 24

    open_func = gzip.open if args.dosya.endswith(".gz") else open
    with open_func(args.dosya, "rt", encoding="utf8") as fp:
        for satir in tqdm(fp, desc="Tweet taranıyor"):
            tweet = json.loads(satir)
            metin = str(tweet["text"]).lower()
            if not metin_i_brak_mi(metin, on_elemeden_gec, on_elemede_kullanilan_karakterler):
                continue

            saat_str = saat_sayisini_ayikla(tweet.get("created_at"))
            saat_int = int(saat_str)

            # Token-level sayım: finditer -> eşleşme sayısı (bir tweet içinde birden fazla olabilir).
            eslesme_yor = list(DESENE_YOR.finditer(metin))
            eslesme_yo = list(DESENE_YO.finditer(metin))

            if eslesme_yor:
                yor_tweet_sayisi[saat_int] += 1
                yor_token_sayisi[saat_int] += len(eslesme_yor)
            if eslesme_yo:
                yo_tweet_sayisi[saat_int] += 1
                yo_token_sayisi[saat_int] += len(eslesme_yo)

    with open(args.cikti_csv, "w", newline="", encoding="utf8") as cikti_fh:
        yazar = csv.writer(cikti_fh)
        yazar.writerow(["saat", "yo", "yor", "yo_token", "yor_token", "yo_tweet", "yor_tweet"])
        for saat in range(24):
            # Geriye uyumluluk: eski `yo/yor` sütunları tweet düzeyi sayım olarak tutuluyor.
            yazar.writerow(
                [
                    saat,
                    yo_tweet_sayisi[saat],
                    yor_tweet_sayisi[saat],
                    yo_token_sayisi[saat],
                    yor_token_sayisi[saat],
                    yo_tweet_sayisi[saat],
                    yor_tweet_sayisi[saat],
                ]
            )

    print(f"OK: {args.cikti_csv} oluşturuldu")


if __name__ == "__main__":
    main()
