# Simple Twitter Auto Base

Buat environments variabel kemudian isi dengan consumer key, access token, dll. Triger word digunakan untuk mentriger pesan agar dikirim. kemudian sleep time waktu yang dibutuhkan untuk sekali pengecekan. Kalau mau menggunakan docker, build image docker nya. kemudian jalankan containernya

```bash
docker build -t statfess .
docker run -it -d --name statfess \
-e CONSUMER_KEY="CONSUMER_KEY" \
-e CONSUMER_SECRET="CONSUMER_SECRET" \
-e ACCESS_TOKEN="ACCESS_TOKEN" \
-e ACCESS_TOKEN_SECRET="ACCESS_TOKEN_SECRET" \
-e TRIGER_WORD="TRIGER_WORD" \
-e TIME_SLEEP=TIME_SLEEP \
statfess
```

Kalau gak mau jalanin pake docker, bisa install dulu requirements nya. kalo kayak gini enaknya pake virtual environments. `pip install -r requirements.txt` habistu jalankan `python main.py`. tapi jangan lupa buat dulu envrionment variabelnya, pake file `env` ubah jadi `.env` terus isi seuai dengan apa yang ada disitu