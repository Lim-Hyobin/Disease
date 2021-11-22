from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import auth
from .models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, "index.html")

def test(request):
    return render(request, 'test.html')


#회원가입
def signup_view(request):
    res_data = {}
    if request.method=='GET':
        return render(request,'signup.html')
    elif request.method =='POST':
        username=request.POST['username']
        password=request.POST['password1']
        re_password=request.POST['password2']
        nickname=request.POST['nickname']
        name=request.POST['name']
        email=request.POST['email']
        disease=request.POST['disease']

        res_data={}
        #unique값인 username과 nickname 예외처리를 위한
        all=User.objects.all()
        username_lst=[x.username for x in all]
        nick_lst=[x.nickname for x in all]
        if not (username and password and nickname and name and email and disease):
            res_data['error']= "모든 값을 입력해야합니다."
        elif password != re_password:
            res_data['error']= "비밀번호가 다릅니다."
        elif username in username_lst:
            res_data['error']="이미 있는 아이디입니다."
        elif nickname in nick_lst:
            res_data['error']="이미 있는 닉네임입니다."
        else:
            user=User.objects.create_user(
                username=username,
                password=password,
                nickname=nickname,
                name=name,
                email=email,
                disease=disease,)
            user.save()
            auth.login(request,user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('index')
        return render(request, 'signup.html',res_data)
        

#로그인
def login_view(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        User = auth.authenticate(username = username, password = password)
        
        if User is not None:
            auth.login(request, User)
            return redirect('index')
            
            #여기 main.html 연결시켜줘야함.

    return render(request, 'login.html')

#로그아웃
@login_required
def logout_view(request):
    auth.logout(request)
    return redirect('/')

def main(request):
    return render(request, "main.html")


#내 정보 보기
def profile(request,user_id):
    profile=User.objects.get(id=user_id)
    return render(request, 'profile.html',{'profile':profile})

def edit(request,user_id):
    profile=User.objects.get(id=user_id)
    return render(request,'edit.html',{'profile':profile})

def update_profile(request,user_id):
    profile=User.objects.get(id=user_id)
    
    if request.method =='POST':
        # print(request.FILES.get('photo'))
        # if request.FILES.get('photo'):
        #     profile.image=request.FILES['photo']
        profile.username=request.POST['username']
        profile.password1=request.POST['password1']
        profile.password2=request.POST['password2']
        profile.nickname=request.POST['nickname']
        profile.name=request.POST['name']
        profile.disease=request.POST['disease']
        profile.save()
    return redirect('user:profile',profile.id)
