"""
Basit sentetik Türkçe tweet üretimi.


"""

import argparse
import gzip
import json
import logging
import random
import datetime

from tqdm import tqdm


def main() -> None:
    parser = argparse.ArgumentParser(
        description="100k sentetik Türkçe tweet üret (fake_simple.json.gz)."
    )
    parser.add_argument("--cikti-dosya", default="fake_simple.json.gz", help="GZip JSONL çıktı dosyası")
    parser.add_argument("--N", type=int, default=100_000, help="Üretilecek tweet sayısı")
    parser.add_argument("--seed", type=int, default=None, help="Rastgele tohum (reprodüksiyon için)")
    parser.add_argument("--tarih", default="2020-02-03", help="created_at tarihi (YYYY-MM-DD)")
    parser.add_argument("--kelime-sayisi", type=int, default=4, help="Sentetik cümle için kelime sayısı")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    if args.seed is not None:
        random.seed(args.seed)

    tarihi = datetime.datetime.strptime(args.tarih, "%Y-%m-%d").date()

    fiil_kokleri = ["bak", "gel", "git", "yaz", "oku", "seç", "koş", "dön", "kaç"]
    unlu_harfler = ["ı", "i", "u", "ü"]
    azaltma_bicimleri = ["yor", "yo", "yo'"]
    kelime_havuzu = [
        "ben",
        "sen",
        "biz",
        "siz",
        "onlar",
        "bugün",
        "şimdi",
        "yolda",
        "bir",
        "iki",
        "güzel",
        "hızlı",
        "yazıyorum",
        "okuyorum",
        "konuşalım",
        "sonra",
        "önce",
        "ama",
        "çünkü",
        "lütfen",
        "evet",
        "hayır",
    ]

    logging.info("Tweet üretiliyor: N=%s, cikti=%s", args.N, args.cikti_dosya)
    with gzip.open(args.cikti_dosya, "wt", encoding="utf8") as cikti_fh:
        for _ in tqdm(range(args.N), desc="Tweet üretiliyor"):
            azaltma_bicimi = random.choice(azaltma_bicimleri)
            unlu = random.choice(unlu_harfler)
            fiil = random.choice(fiil_kokleri)
            govde = f"{fiil}{unlu}{azaltma_bicimi}"

            tumce = " ".join(random.choice(kelime_havuzu) for _ in range(args.kelime_sayisi))
            metin = f"{tumce} {govde}"

            saat = random.randint(0, 23)
            dakika = random.randint(0, 59)
            saniye = random.randint(0, 59)
            created_at = datetime.datetime(
                tarihi.year, tarihi.month, tarihi.day, saat, dakika, saniye
            ).strftime("%Y-%m-%d %H:%M:%S")

            satir = {
                "created_at": created_at,
                "text": metin,
                "source": "FAKE_SIMPLE",
            }
            cikti_fh.write(json.dumps(satir) + "\n")

    print(f"OK: {args.cikti_dosya} hazir")


if __name__ == "__main__":
    main()
