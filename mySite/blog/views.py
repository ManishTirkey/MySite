from django.shortcuts import render as ren, redirect
from django.http import HttpResponse as res
from .models import Post, Comments
from django.contrib import messages
from django.contrib.auth.models import User, auth
# from django.contrib.auth import authenticate, lgout, login
from .templatetags import extras

# Create your views here.
def blogHome(request):
    return ren(request, "blog/home.html")


def blogs(request):
    allpost = Post.objects.all()
    return ren(request, "blog/blogs.html", {"posts": allpost})


# def blogsslug(request, slug):
#     post = Post.objects.filter(slug=slug).first()
#     print(slug)
#     print(post)
#     return res (f"hi this is slug : {slug}")


def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    post.views = post.views + 1
    post.save()
    user = request.user
    blogcomment = Comments.objects.filter(post=post, parent=None)
    reply = Comments.objects.filter(post=post).exclude(parent=None)


    repdict = {}
    for repl in reply:
        if repl.parent.sno not in repdict.keys():
            repdict[repl.parent.sno] = [repl]
        else:
            repdict[repl.parent.sno].append(repl)
    # return ren(request, 'blog/blogpost.html', {'post': post, "comments": blogcomment, "user": user, "replies": repdict})
    return ren(request, 'blog/blogpost.html', {'post': post, "comments": blogcomment, "user": user, "replies": reply})


def BlogComments(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        user = request.user

        postid = request.POST.get("postid")
        post = Post.objects.get(sno=postid)

        parentid = request.POST.get("parentid")

        if parentid == "null":
            comment = Comments(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, f"Thank you {user.first_name} for your comments...")
        else:
            parent = Comments.objects.get(sno=parentid)
            comment = Comments(comment=comment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(request, f"Thank you {user.first_name} for your reply...")

    return redirect(f"/blog/blogs/{post.slug}/")

def search(request):
    query = request.GET['query']
    if len(query) > 100:
        allposts = Post.objects.none()
    else:
        allposttitle = Post.objects.filter(title__icontains=query)
        allpostcontent = Post.objects.filter(content__icontains=query)
        allpost = allposttitle.union(allpostcontent)
        # print(allpost)
        allposts = [post for post in allpost]
        # print(allposts)

    if len(allposts) == 0:
    # if allposts.count() == 0:
        # messages.error(request, "No Posts are found")
        messages.warning(request, "No search results found. Please refine Your Query.")

    # return res("this is search")
    return ren(request, "home/search.html", {"posts": allposts, "query": query})



# works with database

def handleSignup(request):
    if request.method == "POST":

        username = request.POST["username-signup"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["signemail"]
        password_1 = request.POST["password-1"]
        password_2 = request.POST["password-2"]

        if len(username) > 10:
            messages.warning(request, "Username must be greater than 10 char!")
            return redirect("/")

        if not username.isalnum():
            messages.warning(request, "Username must contain character and numbers only!")
            return redirect("/")

        if password_1 == password_2:
            user = User.objects.create_user(username=username, email=email, password=password_1)
            user.first_name = fname
            user.last_name = lname
            user.save()
            messages.success(request, f"your account is successfully created thank you {fname} for signup")
            return redirect("/")
        else:
            messages.warning(request, "password do not match !")
            return redirect("/")
    else:
        return res("404, not found!")

def login(request):
    if request.method == "POST":
        username = request.POST["username-signin"]
        password = request.POST["password"]

        print(username)
        print(password)

        # user = authenticate(username=username, password=password)
        user = auth.authenticate(username=username, password=password)
        print(user)
        if user is not None:
            # login(request, user)
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request, "invalid user")
            return redirect("/")
    return res("404, Not Found")

def logout(request):
    auth.logout(request)
    return redirect("/")















































