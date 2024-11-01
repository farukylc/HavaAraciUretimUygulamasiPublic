import requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator

def home_view(request):
    # JWT token ve kullanıcı bilgilerini kontrol ediyoruz
    jwt_token = request.session.get('jwt_token')
    username = request.session.get('username')
    department = request.session.get('department')  # Departmanı session’da kaydetmiş olun

    if not jwt_token:
        messages.warning(request, 'Bu sayfayı görüntülemek için giriş yapmalısınız.')
        return redirect('login')

    return render(request, 'home.html', {'username': username, 'department': department})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            # API'ye istek atarak JWT token alıyoruz
            response = requests.post(
                f"{settings.API_BASE_URL}/api/token/",
                json={'username': username, 'password': password},
                timeout=5
            )

            if response.status_code == 200:
                data = response.json()
                token = data.get('access')
                
                if token:
                    request.session['jwt_token'] = token
                    request.session['username'] = username

                    # Departman listesini almak için istek yapıyoruz
                    department_response = requests.get(
                        f"{settings.API_BASE_URL}/api/department/department-list",
                        headers={'Authorization': f'Bearer {token}'},
                        timeout=5
                    )

                    if department_response.status_code == 200:
                        departments = department_response.json()
                        # Departmanları ID ile eşlenmiş bir sözlük olarak saklıyoruz
                        department_dict = {dep['id']: dep['name'] for dep in departments}

                        # Kullanıcı listesini almak için istek yapıyoruz
                        user_list_response = requests.get(
                            f"{settings.API_BASE_URL}/api/person/person-list",
                            headers={'Authorization': f'Bearer {token}'},
                            timeout=5
                        )

                        if user_list_response.status_code == 200:
                            user_list = user_list_response.json()
                            
                            # Giriş yapan kullanıcıyı listede bulup departman adını session'a kaydediyoruz
                            for user in user_list:
                                if user['username'] == username:
                                    department_id = user.get('department')
                                    department_name = department_dict.get(department_id, 'Bilinmiyor')
                                    request.session['department'] = department_name
                                    break
                            else:
                                messages.warning(request, 'Departman bilgisi alınamadı.')
                        else:
                            messages.warning(request, 'Kullanıcı bilgileri alınamadı.')
                    else:
                        messages.warning(request, 'Departman listesi alınamadı.')

                    # Başarılı giriş sonrası ana sayfaya yönlendirme
                    return redirect('home')
                else:
                    messages.error(request, 'Giriş işlemi sırasında bir hata oluştu.')
            elif response.status_code == 401:
                messages.error(request, 'Kullanıcı adı veya şifre hatalı.')
            else:
                messages.error(request, 'Bir hata oluştu, lütfen tekrar deneyin.')
        except requests.exceptions.RequestException as e:
            messages.error(request, 'Sunucuya ulaşılamadı, lütfen daha sonra tekrar deneyin.')
            print(f"API isteğinde hata oluştu: {e}")
        
    return render(request, 'login.html')

 
def register_view(request):
    # Departman listesini çekmek için API isteği yapıyoruz
    try:
        department_response = requests.get(f"{settings.API_BASE_URL}/api/department/department-list")
        departments = department_response.json() if department_response.status_code == 200 else []
    except requests.exceptions.RequestException:
        departments = []
        messages.error(request, 'Departman listesi yüklenemedi.')

    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        department = request.POST.get('department')

        # Kullanıcıyı kaydetmek için API isteği
        try:
            response = requests.post(
                f"{settings.API_BASE_URL}/api/person/register/",
                json={
                    'name': name,
                    'username': username,
                    'password': password,
                    'department': department
                }
            )

            if response.status_code == 201:
                messages.success(request, 'Kayıt başarılı, giriş yapabilirsiniz.')
                return redirect('login')
            elif response.status_code == 400:
                messages.error(request, "Bu kullanıcı adı alınmıs")
                return redirect('register')
            else:
                messages.error(request, 'Kayıt başarısız oldu, lütfen bilgilerinizi kontrol edin.')
        except requests.exceptions.RequestException:
            messages.error(request, 'Sunucuya ulaşılamadı, lütfen daha sonra tekrar deneyin.')

    return render(request, 'register.html', {'departments': departments})


def logout_view(request):
    # JWT token varsa API'ye token iptali isteği gönder
    jwt_token = request.session.get('jwt_token')
    if jwt_token:
        try:
            # JWT iptal endpointine istekte bulun (örneğin /api/token/logout/)
            requests.post(
                f"{settings.API_BASE_URL}/logout/",
                headers={'Authorization': f'Bearer {jwt_token}'}
            )
        except requests.exceptions.RequestException:
            messages.error(request, 'Çıkış yaparken bir hata oluştu.')

    # Session'u temizle
    request.session.flush()
    messages.success(request, 'Başarıyla çıkış yaptınız.')

    # Kullanıcıyı login sayfasına yönlendir
    return redirect('login')


PART_TYPE_CHOICES = [
    ('Kanat', 'Kanat'), 
    ('Gövde', 'Gövde'), 
    ('Kuyruk', 'Kuyruk'), 
    ('Aviyonik', 'Aviyonik'), 
]

MODEL_TYPE_CHOICES = [
    ('TB2', 'TB2'),
    ('TB3', 'TB3'),
    ('AKINCI', 'AKINCI'),
    ('KIZILELMA', 'KIZILELMA'),
]

def create_piece_view(request):
    # JWT token ve kullanıcı departmanı kontrolü
    jwt_token = request.session.get('jwt_token')
    user_department = request.session.get('department')  # Kullanıcının departmanı

    if not jwt_token:
        messages.warning(request, 'Bu sayfayı görüntülemek için giriş yapmalısınız.')
        return redirect('login')
    if not user_department:
        messages.error(request, 'Departman bilgisi bulunamadı. Lütfen tekrar giriş yapın.')
        return redirect('login')

    if request.method == 'POST':
        piece_type = request.POST.get('piece_type')
        model_type = request.POST.get('model_type')
        print(user_department)
        print(piece_type)
        # Kullanıcı departmanı ile seçilen parça türünü karşılaştır
        if piece_type != user_department:
            messages.error(request, 'Parça türü departmanınızla eşleşmiyor. Lütfen departmanınıza uygun bir parça türü seçin.')
            return render(request, 'create_piece.html', {
                'part_type_choices': PART_TYPE_CHOICES,
                'model_type_choices': MODEL_TYPE_CHOICES,
                'username': request.session.get('username'),
                'department': user_department,
            })
        
        
        # piece_type_turkish = next((label for value, label in PART_TYPE_CHOICES if value == piece_type), None)
        
        try:
            response = requests.post(
                f"{settings.API_BASE_URL}/api/ihapiece/create/",
                json={
                    'piece_type': piece_type,
                    'model_type': model_type,
                    'is_used': False
                },
                headers={'Authorization': f'Bearer {jwt_token}'}
            )

            if response.status_code == 201:
                data = response.json()
                piece_id = data.get('id')
                
                messages.success(request, f"{piece_type} parçası {model_type} modeli için başarıyla oluşturuldu. Parça ID: {piece_id}")
                return redirect('create_piece')
            else:
                messages.error(request, 'Parça oluşturulamadı. Lütfen bilgilerinizi kontrol edin.')
        except requests.exceptions.RequestException:
            messages.error(request, 'Sunucuya ulaşılamadı, lütfen daha sonra tekrar deneyin.')

    return render(request, 'create_piece.html', {
        'part_type_choices': PART_TYPE_CHOICES,
        'model_type_choices': MODEL_TYPE_CHOICES,
        'username': request.session.get('username'),
        'department': user_department,
    })

def list_pieces_view(request):
    jwt_token = request.session.get('jwt_token')
    user_department_en = request.session.get('department')

    if not jwt_token:
        messages.warning(request, 'Bu sayfayı görüntülemek için giriş yapmalısınız.')
        return redirect('login')

    user_department = dict(PART_TYPE_CHOICES).get(user_department_en, user_department_en)

    try:
        # Parçaları genel API isteğiyle alıyoruz
        response = requests.get(
            f"{settings.API_BASE_URL}/api/ihapiece/piece-list/",
            headers={'Authorization': f'Bearer {jwt_token}'}
        )
        
        if response.status_code == 200:
            pieces = response.json()
            # Parça türlerini Türkçeye çevirme
            for piece in pieces:
                piece['piece_type'] = dict(PART_TYPE_CHOICES).get(piece.get('piece_type'), piece.get('piece_type'))

            # Kullanıcının departmanı ile eşleşen parçaları üstte listelemek için ayırma
            user_team_pieces = [piece for piece in pieces if piece['piece_type'] == user_department]
            other_team_pieces = [piece for piece in pieces if piece['piece_type'] != user_department]

            # Diğer parçalar için sayfalandırma
            paginator = Paginator(other_team_pieces, 5)
            page_number = request.GET.get('page')
            other_team_pieces_page = paginator.get_page(page_number)
        else:
            messages.error(request, 'Parçalar alınamadı.')
            user_team_pieces = []
            other_team_pieces_page = []
    except requests.exceptions.RequestException:
        messages.error(request, 'Sunucuya ulaşılamadı.')
        user_team_pieces = []
        other_team_pieces_page = []

    return render(request, 'list_pieces.html', {
        'user_team_pieces': user_team_pieces,
        'other_team_pieces_page': other_team_pieces_page,
        'username': request.session.get('username'),
        'department': user_department,
    })

# Uçak üretme view
def create_airplane_view(request):
    if request.method == 'POST':
        model_type = request.POST.get('model_type')
        jwt_token = request.session.get('jwt_token')

        response = requests.post(
            f"{settings.API_BASE_URL}/api/airplane/create/",
            json={'model_type': model_type},
            headers={'Authorization': f'Bearer {jwt_token}'}
        )

        if response.status_code == 201:
            messages.success(request, 'Uçak başarıyla üretildi.')
        else:
            messages.error(request, 'Uçak üretme işlemi başarısız oldu.')
        return redirect('airplane_plan')  # URL adı güncellendi
    
    return redirect('airplane_plan')  # GET isteğinde de yönlendirme

# Parça takma view
def attach_piece_view(request):
    if request.method == 'POST':
        airplane_id = request.POST.get('airplane_id')
        piece_id = request.POST.get('piece_id')
        jwt_token = request.session.get('jwt_token')

        response = requests.post(
            f"{settings.API_BASE_URL}/api/airplane-piece/create/",
            json={'airplane': airplane_id, 'piece': piece_id},
            headers={'Authorization': f'Bearer {jwt_token}'}
        )

        if response.status_code == 201:
            messages.success(request, 'Parça başarıyla takıldı.')
        else:
            messages.error(request, 'Parça takma işlemi başarısız oldu.')
        return redirect('airplane_operations')

def list_airplanes_view(request):
    jwt_token = request.session.get('jwt_token')
    username = request.session.get('username')
    department = request.session.get('department')

    # Eğer kullanıcı oturum açmadıysa giriş sayfasına yönlendirme yap
    if not jwt_token:
        messages.warning(request, 'Bu sayfayı görüntülemek için giriş yapmalısınız.')
        return redirect('login')

    # Uçak listesini endpointten al
    airplane_response = requests.get(
        f"{settings.API_BASE_URL}/api/airplane/airplane-list",
        headers={'Authorization': f'Bearer {jwt_token}'}
    )
    print(airplane_response)
    if airplane_response.status_code == 200:
        airplanes = airplane_response.json()
    else:
        airplanes = []
        messages.error(request, 'Uçak listesi alınamadı.')

    return render(request, 'airplane_plan.html', {
        'airplanes': airplanes,
        'username': username,      # Kullanıcı adı şablona iletilir
        'department': department,  # Departman bilgisi şablona iletilir
    })

def manage_airplanes_view(request):
    jwt_token = request.session.get('jwt_token')
    username = request.session.get('username')
    department = request.session.get('department')

    # Eğer kullanıcı Montaj ekibinde değilse uyarı sayfasına yönlendir
    if department != "Montaj":
        return render(request, 'access_denied.html')  # Uyarı sayfasını göster

    # Eğer kullanıcı oturum açmadıysa giriş sayfasına yönlendirme yap
    if not jwt_token:
        messages.warning(request, 'Bu sayfayı görüntülemek için giriş yapmalısınız.')
        return redirect('login')

    # Uçak listesini endpointten al
    airplane_response = requests.get(
        f"{settings.API_BASE_URL}/api/airplane/airplane-list",
        headers={'Authorization': f'Bearer {jwt_token}'}
    )

    # Parçaları endpointten al ve sadece kullanılmayanları filtrele
    piece_response = requests.get(
        f"{settings.API_BASE_URL}/api/ihapiece/piece-list/",
        headers={'Authorization': f'Bearer {jwt_token}'}
    )

    # Uçak ve parça verilerini kontrol et
    if airplane_response.status_code == 200:
        airplanes = airplane_response.json()
    else:
        airplanes = []
        messages.error(request, 'Uçak listesi alınamadı.')

    if piece_response.status_code == 200:
        pieces = [piece for piece in piece_response.json() if not piece['is_used']]
    else:
        pieces = []
        messages.error(request, 'Parça listesi alınamadı.')

    # Parça Takma İşlemi (POST isteği ile gelen veri)
    if request.method == 'POST' and 'airplane_id' in request.POST and 'piece_id' in request.POST:
        airplane_id = request.POST.get('airplane_id')
        piece_id = request.POST.get('piece_id')
        response = requests.post(
            f"{settings.API_BASE_URL}/api/airplane-piece/create/",
            json={'airplane': airplane_id, 'piece_id': piece_id},
            headers={'Authorization': f'Bearer {jwt_token}'}
        )

        if response.status_code == 201:
            messages.success(request, f"Parça ID: {piece_id}, Uçak ID: {airplane_id} ile başarıyla birleştirildi.")
        else:
            print("Hata Detayları:", response.status_code, response.text)
            messages.error(request, 'Parça ekleme işlemi başarısız oldu. Lütfen tekrar deneyin.')
        return redirect('manage_airplanes')

    return render(request, 'manage_airplanes.html', {
        'airplanes': airplanes,
        'pieces': pieces,
        'username': username,
        'department': department,
    })