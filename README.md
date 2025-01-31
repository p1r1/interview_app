# Logistics API v2

## Amaç
Bu proje, lojistik verilerini analiz etmek, yönetmek ve operasyonel verimliliğini artırmak için veri analizi yapan bir RESTful API sağlar. Django ve Django REST Framework kullanılarak geliştirilmiştir.

## Nasıl Kurulur
Örnek bir ".env" dosyası ".env_example" olarak oluşturulmuştur.

### 1. Sanal Ortam Oluşturma
- Ana dizine bir sanal ortam (.venv) oluşturun.
```bash
python -m venv .venv
```
- Sonra gerekli kütüphaneleri yükleyin.
```bash
pip install -r requirements.txt
```

### 2. Veritabanı Oluşturma
Veritabanını ister kendiniz isterseniz yedekleme yöntemi ile oluşturabilirsiniz.
#### **i. Migration İle**
- Postgre ile bir veritabanı oluşturun ve veritabanı bağlantısını (connection string) ".env" dosyanıza yazın. Ardından migration yapın. Böylece gerekli tablolar oluşmuş olacaktır. 
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```
- Daha Sonra tabloları örnek csv dosyaları ile doldurmak için ".csv" uzantılı dosyalarınızı "csv" klasörüne koyun. Böylece ".csv" dosyaları veritabanına işlenmiş olacak.
```bash
python manage.py load_data
```

#### **ii. Veritabanı Yedeğine Geri Dönerek**
- Yada postgre veritabanında "interview_app" adında yeni bir veritabanı oluşturun. (Encoding = WIN1252) Sonra "./docs/other_files/interview_app.dump" dosyasına geri dönün.
```bash
pg_restore -U postgre -d interview_app -v interview_app.dump
```
"postgre" kullanıcı adı.

### 3. Redis
Windows işletim sisteminde resmi olarak bir redis dağıtımı olmadığı için docker kullanacağız. Docker yükleyin ve aşağıdaki komutu çalıştırın.
``` bash
docker run --name django-redis -d -p 6379:6379 --rm redis
```
Burada iç port ve dış port numarası önemli (6379:6379). Yine redis bağlantısını (uri) ".env" dosyanıza eklemeyi unutmayın.

```bash
docker exec -it b5d214f1c.. redis-cli
```
b5d214f1c.. (redis container id)
Bu komut ile redis-cli arayüzüne ulaşabilirsiniz.

### 4. Swagger UI Schema
Halihazırda bir schema.yml dosyası mevcut ama güncellemek için Swagger UI schema.yaml oluşturma:
```bash
python manage.py spectacular --color --file schema.yml
```
### 5. SuperUser (Admin) Oluşturma
```bash
python manage.py createsuperuser
```

## Nasıl Çalıştırılır

```bash
python manage.py runserver
```
## Nasıl Kullanılır

### 1. API Uygulaması Oluşturma
http://127.0.0.1:8000/admin/ (http://127.0.0.1:8000/ -> base url) adesine gidin ve superuser ile giriş yapın. Daha sonra "Django OAuth Toolkit" altında "Applications" > Add Applications kısmına tıklayın.
İlgili kısımları doldurun. Authorization grant type bölümünü test için "Resource owner password-based" olarak seçmeniz tavsiye ederim. Çünkü bütün http dosyaların buna göre hazırlandı. Test olmayan kullanımlarda diğer erişim tiplerinden uygun olanını seçebilirsiniz.

Örnek olarak oluşturulan API application:
- Verilen Client id ".vscode/settings.json" içinde saklayın.
- User kısmından şifresini bildiğiniz bir kullanıcı seçin. Ben superuser'ı seçtim. Yine ".vscode/settings.json" user name ve password bölümünü ilgili kullanıcıya göre kayıt edin.
- Client type -> Public
- Authorization grant type -> Resource owner password-based.
- Verilen Client secret ".vscode/settings.json" içinde saklayın.
- Hash client secret seçilebilir.

".vscode/settings.json" dosyanızı kontrol edin ve "Add Applications" sayfasını save tuşuna basarak kaydedin. API kullanmaya hazır ve ".http" dosyalarını deneyebilirsiniz. 

### 2. HTTP Dosya Kullanımı
Vscode rest client eklentisi ile geliştireln bu dosyalar api için örnekler teşkil etmekte. Dosyadaki değişkenler ".vscode/settings.json" dosyasından gelmekte olup örnek bir dosya "".vscode/settings.json" adı altında bulunmaktadır. Bu dosyalrı kullanırken:
- Öncelikle "POST {{BASE_URL}}/o/token/" "Send Request" linkine tıklayarak token alınız.
- Daha sonra diğer "Send Request" link yada linklerine tıklayarak api örnek kullanımı görebilirsiniz.

### 3. Testler
- #### Unit, API testleri 
```bash
python manage.py test
```
- #### Performans (Load) Testi
```bash
locust -f locust.py --host=http://127.0.0.1:8000
```
- http://127.0.0.1:8000 -> API base url
- http://localhost:8089 -> Locust performans testini bu urlden yapabilirsiniz. 
## Kaynaklar
https://www.kaggle.com/datasets/aashokaacharya/logistics-company-dataset-for-sql