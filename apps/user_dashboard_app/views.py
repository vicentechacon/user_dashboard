from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.core.exceptions import PermissionDenied

# --------------------------------> LOGIN VIEWS <--------------------------------
def index(request):
    return render(request,'register.html')


def register(request):
    if request.method =='GET':
        return render(request,'register.html')
    elif request.method =='POST':
        errors = User.objects.basic_validations(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/register')
        else:
            hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            user=User.objects.first()
            newuser = User(
                first_name=request.POST['first_name'],
                last_name= request.POST['last_name'],
                email= request.POST['email'],
                password= hash1)
            if not user:
                newuser.admin=True
            newuser.save()
            request.session['id'] = newuser.id
        return redirect(f'users/{newuser.id}')


def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    if request.method =='POST':
        login_validator = User.objects.login_validations(request.POST)
        if len(login_validator)>0:
            for key, value in login_validator.items():
                messages.error(request, value)
            return redirect('/login')
        user = User.objects.filter(email=request.POST['email'])[0]
        request.session['id'] = user.id
        return redirect(f'/users/{user.id}')
    return redirect('/login')



def logout(request):
    request.session.clear()
    return redirect('/login')


# --------------------------------> USERS VIEWS <--------------------------------


def show_user(request, user_id):
    if 'id' not in request.session:
        return redirect('/login')
    user = User.objects.get(id=user_id)
    user_online=User.objects.get(id=request.session['id'])
    messages=Message.objects.filter(sended_to_id=user_id)
    comments=Message.objects.all()
    context = {
        'user_online':user_online,
        'user':user,
        'messages':messages,
        'comments':comments
    }
    return render(request, 'users.html', context)


def post_message(request, user_id):
    if request.method == 'POST':
        user_posting = User.objects.get(id=request.session['id'])
        user_receiving = User.objects.get(id=user_id)
        new_message = Message.objects.create(
            message=request.POST['message'],
            sended_to=user_receiving,
            created_by=user_posting,
        )
        print(new_message)
        new_message.save()
    return redirect(f'/users/{user_id}')


def post_comment(request, message_id):
    message = Message.objects.get(id=message_id)
    user_online=User.objects.get(id=request.session['id'])
    if 'id' not in request.session:
        return redirect('/login')
    elif request.method == 'POST':
        comment=request.POST['comment']
        user=message.sended_to
        newcomment=Comment.objects.create(comment=comment, message=message, created_by=user_online)
        newcomment.save()
        return redirect(f'/users/{user.id}')


def delete_message(request, message_id):
    message = Message.objects.get(id=message_id)
    user= message.sended_to
    if message.created_by.id != request.session['id']:
        raise PermissionDenied()
    message.delete()
    return redirect(f'/users/{user.id}')


def delete_comment(request, comment_id):
    comment=Comment.objects.get(id=comment_id)
    message=comment.message
    user = message.sended_to
    if comment.created_by.id != request.session['id']:
        raise PermissionDenied()
    comment.delete()
    return redirect(f'/users/{user.id}')


def dashboard(request):
    if 'id' not in request.session:
        return redirect('/login')
    users=User.objects.all().order_by('id')
    user_online = User.objects.get(id=request.session['id'])
    context = {
        'users':users,
        'user_online':user_online
    }
    return render(request,'dashboard.html', context)


def user_edit(request, user_id):
    user_to_edit = User.objects.get(id=request.session['id'])
    user_to_edit.id=user_id
    if user_to_edit:
        if request.method =='GET':
            context ={
                'user':user_to_edit,
            }
            return render(request, 'edit_profile.html', context)

        elif request.method == 'POST':
            user_to_edit.email = request.POST['email']
            user_to_edit.first_name = request.POST['first_name']
            user_to_edit.last_name = request.POST['last_name']
            user_to_edit.save()
    return redirect(f'/users/{user_id}')


def user_edit_description(request, user_id):
    user_to_edit = User.objects.get(id=request.session['id'])
    if user_to_edit:
        if request.method =='GET':
            context ={
                'user':user_to_edit,
            }
            return render(request, 'edit_profile.html', context)

        elif request.method == 'POST':
            user_to_edit.description = request.POST['description']
            user_to_edit.save()
    return redirect(f'/users/{user_id}')


def change_password(request, user_id):
    if 'id' not in request.session:
        return redirect('/')

    user_to_edit = User.objects.get(id=request.session['id'])
    if user_to_edit:
        if request.method =='GET':
            context = {
                'user':user_to_edit
            }
            return render(request, 'edit_profile.html')
        elif request.method == 'POST':
            password = request.POST['password']
            print('changing password.......')
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user_to_edit.password=pw_hash
            user_to_edit.save()
            message = 'New password is saved successfully, try to login!'
            messages.success(request, message)
            return redirect('/login')





# --------------------------------> ADMIN VIEWS <--------------------------------


def admin_dashboard(request):
    users = User.objects.all().order_by('id')
    user=User.objects.get(id=request.session['id'])
    if user.admin != True:
        raise PermissionDenied
    context ={
        'users':users,
        'user_online':user
    }
    return render(request, 'admin_dashboard.html', context)


def admin_add_new(request):
    if 'id' not in request.session:
        return redirect('/login')
    if request.method == 'GET':
        context = {
            'user_online':User.objects.get(id=request.session['id'])
        }
        return render(request, 'admin_add_user.html', context)
    elif request.method == 'POST':
        errors = User.objects.basic_validations(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/users/new')
        newuser = User.objects.create(
            email=request.POST['email'],
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            password=request.POST['password'],
        )
        newuser.save()
    return redirect('/dashboard/admin')


def admin_delete(request, user_id):
    user=User.objects.get(id=request.session['id'])
    if user.admin != True:
        raise PermissionDenied
    user_to_delete=User.objects.get(id=user_id)
    user_to_delete.delete()
    return redirect('/dashboard/admin')


def admin_edit(request, user_id):
    user_to_edit = User.objects.get(id=user_id)
    user = User.objects.get(id=request.session['id'])
    if user_to_edit:
        if request.method == 'GET':
            context ={
                'user':user_to_edit,
                'user_online':user
            }
            return render (request, 'admin_edit_user.html', context)
        elif request.method=='POST':
            user_to_edit.email = request.POST['email']
            user_to_edit.first_name = request.POST['first_name']
            user_to_edit.last_name = request.POST['last_name']
            user_to_edit.admin = request.POST['admin']
            user_to_edit.save()
    return redirect('/dashboard/admin')

def admin_edit_password(request, user_id):
    user_to_edit = User.objects.get(id=user_id)
    user = User.objects.get(id=request.session['id'])
    if user_to_edit:
        if request.method=='GET':
            context ={
                'user':user_to_edit,
                'user_online':user
            }
            return render(request, 'admin_edit_user.html', context)
        elif request.method == 'POST':
            password = request.POST['password']
            print('changing password.......')
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user_to_edit.password = pw_hash
            user_to_edit.save()
            message = 'New password is saved successfully, try to login!'
            messages.success(request, message)
            return redirect ('/dashboard/admin')

