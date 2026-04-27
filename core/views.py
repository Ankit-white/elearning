from django.shortcuts import render
from .models import File
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
import os


@login_required
def home(request):
    files = File.objects.all()
    is_admin = request.user.is_superuser
    return render(request, 'core/home.html', {
        'files': files,
        'is_admin': is_admin
    })


# check admin
def is_admin_check(user):
    return user.is_superuser


@user_passes_test(is_admin_check)
def upload_file(request):
    if request.method == "POST":
        title = request.POST.get('title')
        file = request.FILES.get('file')

        if not title or not file:
            return render(request, 'core/upload.html', {'error': 'Title and file are required.'})

        # Validate file size (50MB limit)
        max_size = 50 * 1024 * 1024  # 50 MB
        if file.size > max_size:
            return render(request, 'core/upload.html', {'error': 'File too large. Maximum size is 50MB.'})

        # Allowed extensions (including PDF)
        ALLOWED_EXTENSIONS = [
            '.pdf', '.mp4', '.mp3',
            '.doc', '.docx', '.ppt', '.pptx',
            '.png', '.jpg', '.jpeg', '.gif',
            '.zip', '.txt'
        ]

        ext = os.path.splitext(file.name)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            return render(request, 'core/upload.html', {
                'error': f'File type "{ext}" is not allowed.'
            })

        File.objects.create(title=title, file=file)
        return redirect('/')

    return render(request, 'core/upload.html')


def ai_help(request):
    try:
        from .models import File
        count = File.objects.count()

        if count == 0:
            return JsonResponse({"answer": "No files uploaded by admin."})
        return JsonResponse({"answer": f"System working fine. {count} file(s) available."})

    except Exception as e:
        return JsonResponse({"answer": f"Error: {str(e)}"})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'core/login.html', {'error': 'Invalid username or password.'})

    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    return redirect('/login/')


from django.contrib.auth.models import User


def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'core/register.html', {'error': 'Username already exists.'})

        user = User.objects.create_user(username=username, password=password)
        user.save()

        return redirect('/login/')

    return render(request, 'core/register.html')