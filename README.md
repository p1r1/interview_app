# Logistics API v2

## Amaç
Bu proje, lojistik verilerini analiz etmek, yönetmek ve operasyonel verimliliğini artırmak için veri analizi yapan bir RESTful API sağlar. Django ve Django REST Framework kullanılarak geliştirilmiştir.

## Nasıl Kurulur
Örnek bir ".env" dosyası ".env_example" olarak oluşturulmuştur.

**Sanal Ortam Oluşturma:**
Ana dizine bir sanal ortam (.venv) oluşturun.
```bash
python -m venv /path/to/new/virtual/environment
```
Sonra gerekli kütüphaneleri yükleyin.
```bash
pip install -r requirements.txt
```

**Veritabanı Oluşturma:**
Postgre ile bir veritabanı oluşturun ve veritabanı bağlantısını (connection string) ".env" dosyanıza yazın. Ardından migration yapın.
```bash
python manage.py makemigrations
python manage.py migrate
```
Böylece gerekli tablolar oluşmuş olacaktır. 
Daha Sonra tabloları örnek csv dosyaları ile doldurmak için ".csv" uzantılı dosyalarınızı "csv" klasörüne koyun.
```bash
python manage.py load_data
```
Böylece ".csv" dosyaları veritabanına işlenmiş olacak.

(Opsiyonel)
Yada postgre psql ile "interview_app" adında yeni bir veritabanı oluşturun. Encoding = WIN1252
Sonra "docs/other_files/interview_app.dump" dosyasına geri dönün.
```bash
pg_restore -U postgre -d interview_app -v interview_app.dump
```
"postgre" kullanıcı adı.

**Redis:**
Windows işletim sisteminde docker içinde redis kullanmak için docker yükleyin ve aşağıdaki komutu çalıştırın.
``` bash
docker run --name django-redis -d -p 6379:6379 --rm redis
```
Burada iç port ve dış port numarası önemli (6379:6379). Yine redis bağlantısını ".env" dosyanıza eklemeyi unutmayın.

**Swagger UI Schema:**
Swagger UI schema.yaml oluşturmak için :
```bash
python ./manage.py spectacular --color --file schema.yml
```
**SuperUser (Admin) Oluşturma**
```bash
python manage.py createsuperuser
```

## Nasıl Çalıştırılır

```bash
python manage.py runserver
```
## Nasıl Kullanılır

**API Uygulaması Oluşturma**
http://127.0.0.1:8000/admin/ adesine gidin ve superuser ile giriş yapın. Daha sonra "Django OAuth Toolkit" altında "Applications" > Add Applications kısmına tıklayın.
İlgili kısımları doldurun. Authorization grant type bölümünü test için "Resource owner password-based" olarak seçmeniz tavsiye ederim. Çünkü bütün http dosyaların buna göre hazırlandı. Test olmayan kullanımlarda diğer erişim tiplerinden uygun olanını seçebilirsiniz.

Örnek olarak:
-Verilen Client id ".vscode/settings.json" içinde saklayın.
-User kısmından şifresini bildiğiniz bir kullanıcı seçin. Ben superuser'ı seçtim. Yine ".vscode/settings.json" user name ve password bölümünü ilgili kullanıcıya göre kayıt edin.
-Client type -> Public
-Authorization grant type -> Resource owner password-based.
-Verilen Client secret ".vscode/settings.json" içinde saklayın.
-Hash client secret seçilebilir.

".vscode/settings.json" dosyanızı kontrol edin ve "Add Applications" sayfasını save tuluna basarak kaydedin. API kullanmaya hazır ve ".http" dosyalarını deneyebilirsiniz. 

**HTTP Dosya Kullanımı**
Vscode rest client eklentisi ile geliştireln bu dosyalar api için örnekler teşkil etmekte. Dosyadaki değişkenler ".vscode/settings.json" dosyasından gelmekte olup örnek bir dosya "".vscode/settings.json" adı altında bulunmaktadır. Bu dosyalrı kullanırken:
-Öncelikle "POST {{BASE_URL}}/o/token/" "Send Request" linkine tıklayarak token alınız.
-Daha sonra diğer "Send Request" link yada linklerine tıklayarak api örnek kullanımı görebilirsiniz.

## Kaynaklar
https://www.kaggle.com/datasets/aashokaacharya/logistics-company-dataset-for-sql