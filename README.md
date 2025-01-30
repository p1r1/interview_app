# Logistics API v2

## Amaç
Bu proje, lojistik verilerini analiz etmek, yönetmek ve operasyonel verimliliğini artırmak için veri analizi yapan bir RESTful API sağlar. Django ve Django REST Framework kullanılarak geliştirilmiştir.

## Nasıl Kurulur
Örnek bir ".env" dosyası ".env_example" olarak oluşturulmuştur.
1. **Sanal Ortam Oluşturma:**
Ana dizine bir sanal ortam (.venv) oluşturun:
```bash
python -m venv /path/to/new/virtual/environment
```
2. **Veritabanı Oluşturma**
Postgre ile bir veritabanı oluşturun ve veritabanı bağlantısını (connection string) ".env" dosyanıza yazın. Ardından migration yapın:
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
3. **Redis**
Windows işletim sisteminde docker içinde redis kullanmak için docker yükleyin ve aşağıdaki komutu çalıştırın.
``` bash
docker run --name django-redis -d -p 6379:6379 --rm redis
```
Burada iç port ve dış port numarası önemli (6379:6379). Yine redis bağlantısını ".env" dosyanıza eklemeyi unutmayın.
4. **Swagger UI Schema**
Swagger UI schema.yaml oluşturmak için :
```bash
python ./manage.py spectacular --color --file schema.yml
```

## Nasıl Çalıştırılır

```bash
python manage.py runserver
```
## Nasıl Kullanılır

## Kaynaklar
https://www.kaggle.com/datasets/aashokaacharya/logistics-company-dataset-for-sql