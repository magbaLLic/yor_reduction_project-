# -yor » -yo Sentetik Veri Denemesi

Bu repo, Türkçe uzantılı `-yor` ekinin sosyal medyada `-yo` kısalmasına dair
basit frekans analizi içerir.

## Dosyalar
| Dosya | Açıklama |
|-------|----------|
| `uret_fake_simple.py` | 100k sentetik tweet üretir (`fake_simple.json.gz`) |
| `uret_fake_faker.py`   | 100k Faker tabanli sentetik tweet üretir (`fake_faker.json.gz`) |
| `say_yo.py`            | Dosyadan yo/yor sayar → `saat_sayim.csv` |
| `graf.py`              | CSV'den grafiği çizer → `ratio_plot.png` |

## Kullanım
```bash
python uret_fake_simple.py
python say_yo.py
python graf.py
```
