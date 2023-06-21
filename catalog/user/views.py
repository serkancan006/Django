from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth,messages

# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username = username, password = password)
        if user is not None:
            auth.login(request, user)
            #print('login basarılı')
            messages.add_message(request, messages.SUCCESS,'Oturum acildi')
            return redirect('index')
        else:
            #print('Kullanıcı adı veya parola yanlış')
            messages.add_message(request, messages.ERROR,'Hatali Kullanici adi yada parola')
            return redirect('login')
    else:
        return render(request, 'user/login.html')

def register(request):
    if request.method == 'POST':
        
        #get form values
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repassword = request.POST['repassword']
        
        if password == repassword:
            #Username
            if User.objects.filter(username = username).exists():
                #print('bu kullanıcı adı daha önce alınmış')
                messages.add_message(request, messages.WARNING,'Bu kullanici adi daha önce alinmis')
                return redirect('register')
            else:
                if User.objects.filter(email = email).exists():
                    #print('bu email adı daha önce alınmış')
                    messages.add_message(request, messages.WARNING,'bu email adi daha önce alinmis')
                    return redirect('register')
                else:
                    #herşey güzel
                    user = User.objects.create_user(username=username,password=password,email=email)
                    user.save()
                    #print('kullanıcı oluşturuldu')
                    messages.add_message(request,messages.SUCCESS,'Hesabiniz olusturuldu')
                    return redirect('login')
        else:
            print('parololar eşleşmiyor')
            return render(request, 'user/register.html')
        
      
    else:
        return render(request, 'user/register.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.add_message(request, messages.SUCCESS,'oturumunuz kapatildi')
        return redirect('index')
