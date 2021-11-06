from django.shortcuts import render, redirect
from .models import Post, User
from .forms import PostForm, MyUserCreationForm, EditUserform
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q










# Create your views here.


def register_user(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = MyUserCreationForm()
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            messages.error(request, "If you want to update your PFP or Bio, go to your profile settings.")
            return redirect("home")
        else:
            messages.error(request, "Something went wrong.")
    context = {"page": "register", "form": form}
    return render(request, "base/login_register.html", context)

def login_page(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User doesn´t exist.")
            return redirect("login")
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
        else:
            messages.error(request, "Username or Password is incorrect.")
            return redirect("login")
        return redirect("home")
    context = {"page": page}
    return render(request, "base/login_register.html", context)

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("home")
    else:
        return redirect("home")

def follows(follower, followee):
    if follower is followee:
        return False
    try:
        followee.followers.get(id=follower.id)
        return True
    except:
        return False


def profile(request, pk):
    try:
        user = User.objects.get(id=pk)
    except:
        messages.error(request, "User doesn´t exist!")
        return redirect("home")
    users = User.objects.all()
    following = []
    for followee in users:
        if follows(user, followee):
            following.append(followee)
    adj = "UN" if follows(request.user, user) else ""
    context = {"posts": user.post_set.all(), "user": user, "users": users[:5], "following": following, "adj": adj,\
        "side_title": f"Users followed by {user.username}", "usercount": len(users),  "followed_by": user}
    return render(request, "base/profile.html", context)

def home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    posts = []
    for post in Post.objects.all():
        if (follows(request.user, post.owner) or request.user == post.owner) and\
            (q in post.name or q in post.body):
            posts.append(post)
    users = User.objects.all()
    following = []
    for user in users:
        if follows(request.user, user):
            following.append(user)
    side_title = "Users Followed" if request.user.is_authenticated else "REGISTER TO FOLLOW USERS"
    context = {"posts": posts, "users": users[:5], "following": following,\
        "side_title": side_title, "usercount": len(users), "followed_by": request.user}
    return render(request, "base/home.html", context)

@login_required(login_url="/login")
def like_unlike(request, pk):
    try:
        post = Post.objects.get(id=pk)
    except:
        messages.error(request, "Post not found.")
        return redirect("home")
    try:
        user = post.likes.get(id=request.user.id)
        post.likes.remove(user)
    except:
        post.likes.add(request.user)
    return redirect("home")

@login_required(login_url="/login")
def follow_unfollow(request, pk):
    try:
        followee = User.objects.get(id=pk)
    except:
        messages.error(request, "User not found.")
        return redirect("home")
    if follows(request.user, followee):
        followee.followers.remove(request.user)
    else:
        if followee == request.user:
            messages.error(request, "You can´t follow yourself!")
            return redirect("home")
        followee.followers.add(request.user)
    return redirect("home")

@login_required(login_url="/login")
def edit_user(request):
    user = request.user
    form = EditUserform(instance=user)
    context = {"form": form}
    if request.method == "POST":
        form = EditUserform(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile", pk=user.id)
    return render(request, "base/edit_user.html", context)


@login_required(login_url="/login")
def create_post(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            post.save()
            return redirect("home")
    context = {"form": form}
    return render(request, "base/post_form.html", context)


def users(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    users = User.objects.filter(
        Q(username__icontains=q)
    )
    context = {"users": users, "count": users.count()}
    return render(request, "base/users.html", context)


@login_required(login_url="/login")
def followed_users(request, pk):
    try:
        user = User.objects.get(id=pk)
    except:
        messages.error(request, "User doesn´t exist!")
        return redirect("home")
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    users = []
    for second_user in User.objects.all():
        if follows(user, second_user) and q in second_user.username:
            users.append(second_user)
    context = {"users": users, "count": len(users)}
    return render(request, "base/users.html", context)


def following_users(request, pk):
    try:
        user = User.objects.get(id=pk)
    except:
        messages.error(request, "User doesn´t exist!")
        return redirect("home")
    context = {"users": user.followers.all(), "count": user.followers.count()}
    return render(request, "base/users.html", context)