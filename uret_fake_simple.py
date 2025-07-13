import random, gzip, json, datetime, tqdm, faker
fake = faker.Faker('tr_TR')

verbs      = ["bak", "gel", "git", "yaz", "oku", "seç", "koş", "dön", "kaç"]
vowels     = ["ı", "i", "u", "ü"]
yo_forms   = ["yor", "yo", "yo'"]    
N = 100_000

with gzip.open("fake_faker.json.gz", "wt", encoding="utf8") as fh:
    for _ in tqdm.tqdm(range(N)):
        yo_forms = ['yor', 'yo', "yo'"]                      
        core = f"{random.choice(verbs)}{random.choice(vowels)}{random.choice(yo_forms)}"   
        sentence = fake.sentence(nb_words=4)
        txt = f"{sentence} {core}"

        ts = datetime.datetime(
                2020, 2, 3,
                random.randint(0, 23),
                random.randint(0, 59),
                random.randint(0, 59)
             ).strftime("%Y-%m-%d %H:%M:%S")

        fh.write(json.dumps({"created_at": ts,
                             "text": txt,
                             "source": "FAKE"}) + "\n")

print("fake_faker.json.gz hazır")
