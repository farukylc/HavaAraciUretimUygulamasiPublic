# İHA Üretim ve Montaj Yönetim Sistemi
Bu proje, İHA parçalarının yönetimi ve montajı için geliştirilen bir uygulamadır. Proje, her bir parçanın üretimi, ekiplere göre atanması, envanter yönetimi ve İHA montajı gibi özellikleri içerir. Montaj işlemleri sadece Montaj Ekibi tarafından gerçekleştirilirken, her bir İHA modeli için belirli parça kuralları tanımlanmıştır. Proje, uçak üretimi ve parçaların tek seferlik kullanımını sağlamak üzere tasarlanmıştır.

# Projenin Deploy edilmesi
Bu proje Railway kullanılarak deploy edilmiştir. Aşağıdaki linken uygulamaya erişip kendiniz için kullanıcılar oluşturup test edebilirsiniz.

https://havaaraciuretimuygulamasi-production.up.railway.app/login/

# Özellikler

**Kullanıcı Yönetimi**: Kullanıcılar, farklı departmanlara göre yönetilir ve her kullanıcının kendi ekibi için parça üretimi yapmasına izin verilir.

**JWT Token ve Yetkilendirme**
Bu proje, güvenli kullanıcı erişimi sağlamak için JWT (JSON Web Token) tabanlı kimlik doğrulama sistemi kullanır. Her kullanıcının kimlik doğrulaması sonrasında bir JWT token oluşturulur ve bu token ile belirli kaynaklara erişim sağlanır. JWT token, kullanıcının oturum açmasıyla oluşturulur ve her yetkilendirilmiş API isteğinde kullanıcının yetkisini doğrulamak için gereklidir.

**Parça Yönetimi**: Parçalar her departmana göre atanır ve üretim sürecinde kullanılır.

**İHA Montajı**: İHA montajı yalnızca Montaj Ekibi tarafından yapılabilir ve her İHA modeli için belirli parçalar gereklidir.

**Envanter Kontrolü**: Parçalar yalnızca bir kez kullanılabilir ve her bir İHA'ya özel atanır.

**Doğrulama ve Uyarı Mesajları**: Uygun departmana göre parça atanmazsa uyarı mesajları gösterilir.

**Oturum Yönetimi**: Kullanıcı oturum açma, oturum kapatma ve yetki doğrulaması yapılır.


# Kullanılan Teknolojiler

**Python**: Proje geliştirme dili olarak kullanıldı.

**Docker**: Proje docker ile kolayca ayağa kaldırılabilir.

**Django:** Projenin backend altyapısı için tercih edildi. Django, yüksek performanslı bir MVC yapısı sunar.

**Django Rest Framework**: API oluşturma sürecinde kullanıldı.

**Bootstrap**: Ön yüz geliştirme için kullanılan CSS çerçevesi.



# Projeyi klonlayın
```bash
git clone https://github.com/farukylc/HavaAraciUretimUygulamasi.git
```


# Gerekli bağımlılıkları yükleyin
```bash
pip install -r requirements.txt
```

# Veritabanını oluşturun
```bash
python manage.py migrate
python manage.py makemigrations
```

# Projeyi Ayağa Kaldırın

Projeyi docker ile ayağa kaldırmak için
```bash
docker-compose up --build
```
komutunu kullanabilirsiniz

Projeyi docker kullanmadan ayağa kaldırmak isterseniz API_BASE_URL="http://127.0.0.1:8000/" şeklinde olmalıdır.

```bash
cd backend
python manage.py runserver

cd frontend
python manage.py runserver 8001
```


## Proje içi Görseller

<div align="center">
    <p style="color:blue; font-weight:bold; font-size: 18px;">Giriş Ekranı</p>
    <img src="https://github.com/user-attachments/assets/2c9b9a48-5f6c-41b0-bbd4-1496b6e7310f" alt="Ekran Resmi 2024-11-01 10 27 05" width="600">
    <p>Kullanıcıların sisteme giriş yapabildiği ekrandır. Bu ekranda kullanıcı adı ve şifre bilgileri girilerek doğrulama yapılır ve başarılı bir giriş sonrasında ana ekrana yönlendirilir.</p>
</div>

<div align="center">
    <p style="color:blue; font-weight:bold; font-size: 18px;">Kayıt Ekranı</p>
    <img src="https://github.com/user-attachments/assets/a1968364-b937-4b2a-90f9-38d5be3e4334" alt="image" width="600">
    <p>Yeni kullanıcıların sisteme kaydolabileceği ekrandır. Kayıt sırasında kullanıcının departman ve diğer kimlik bilgileri istenir. Departmanlar dropdown menüden seçilerek ekibe özel atama yapılır.</p>
</div>

<div align="center">
    <p style="color:blue; font-weight:bold; font-size: 18px;">Ana Ekran</p>
    <img src="https://github.com/user-attachments/assets/887ced99-0740-4753-a7e6-009033aeb888" alt="image" width="600">
    <p>Sisteme giriş yaptıktan sonra kullanıcıları karşılayan ana ekrandır. Kullanıcının yetkisine ve departmanına göre menü ve işlem seçenekleri burada görüntülenir. Montajcı kullanıcılar için özel işlemler bulunmaktadır.</p>
</div>

<div align="center">
    <p style="color:blue; font-weight:bold; font-size: 18px;">Parça Üretim Ekranı</p>
    <img src="https://github.com/user-attachments/assets/137ac322-6f74-445e-9028-3e19b6459ca1" alt="image" width="600">
    <p>Parça üretim işlemlerinin gerçekleştirildiği ekrandır. Kullanıcıların bağlı oldukları departmana göre parça üretebilmelerine izin verilir. Ayrıca parça tipi ve detayları burada seçilir.</p>
</div>

<div align="center">
    <p style="color:blue; font-weight:bold; font-size: 18px;">Uçak Planı Üretim Ekranı</p>
    <img src="https://github.com/user-attachments/assets/f578e149-1168-4ce9-b0c7-09ff8ea38879" alt="image" width="600">
    <p>Yalnızca Montaj Ekibi'nin erişebildiği uçak planı oluşturma ekranıdır. Yeni bir İHA modeli oluşturulurken gereksinim duyulan parçaların planı burada yapılır.</p>
</div>

<div align="center">
    <p style="color:blue; font-weight:bold; font-size: 18px;">Uçaklara Parça Takma Ekranı</p>
    <img src="https://github.com/user-attachments/assets/e33857c4-5b07-4544-9c8a-30052e435690" alt="image" width="600">
    <p>Üretilmiş parçaların İHA'ya takılabildiği ekrandır. Parçalar, model ve uçak planına uygun bir şekilde tek seferlik kullanılarak atanır. Her bir uçak için farklı parçaların takılması sağlanır.</p>
</div>





