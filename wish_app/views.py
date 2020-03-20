from django.shortcuts import render, redirect
from .models import Wish, User
from django.contrib import messages
from datetime import date

# Create your views here.

def view(request):
    print("In view method")
    if not verify_logged_in(request):
        return redirect('/')

    context = {
        "user": User.objects.get(id=request.session['id']),
        # "user_wishes": User.objects.get(id=1).wishes.filter(is_granted=False),
        "user_wishes": Wish.objects.filter(user_id=request.session['id'], is_granted=False),
        "granted_wishes": Wish.objects.filter(is_granted=True),
    }
    return render(request, "wishes.html", context)

def new(request):
    print("In new method")
    if not verify_logged_in(request):
        return redirect('/')

    context = {
        "user": User.objects.get(id=request.session['id']),
    }
    return render(request, 'new_wish.html', context)

def edit(request, wish_id):
    print("In edit method")
    if not verify_logged_in(request):
        return redirect('/')

    context = {
        "user": User.objects.get(id=request.session['id']),
        "wish": Wish.objects.get(id=wish_id),
    }
    return render(request, 'edit_wish.html', context)

def remove(request, wish_id):
    print("In remove method")
    if not verify_logged_in(request):
        return redirect('/')

    wish = Wish.objects.get(id=wish_id)
    wish.delete()

    return redirect('/wishes/')

def grant(request, wish_id):
    print("In grant method")
    if not verify_logged_in(request):
        return redirect('/')

    wish = Wish.objects.get(id=wish_id)
    wish.is_granted = True
    wish.granted_date = date.today()
    wish.save()

    return redirect('/wishes/')

def create(request):
    print("In create method")
    if not valid_post_request(request):
        return redirect("/wishes/")
    
    errors = Wish.objects.validate(request.POST)
    if errors:         # if we have any errors returned in the errors object, display them
        for key, err in errors.items():
            messages.error(request, err)
        return redirect("/wishes/new")

    this_user = User.objects.get(id=request.session['id'])

    wish = Wish.objects.create(
        item = request.POST['item_name'],
        desc = request.POST['item_description'],
        user = this_user,
        is_granted = False,
    )

    wish.likes.add(this_user)

    print("Wish created successfully - item:", wish.item)
    # return to the list of wishes if we are successful
    return redirect('/wishes/')

def update(request, wish_id):
    print("In update method")
    if not valid_post_request(request):
        return redirect("/wishes/")

    errors = Wish.objects.validate(request.POST)
    if errors:         # if we have any errors returned in the errors object, display them
        for key, err in errors.items():
            messages.error(request, err)
        return redirect(f"/wishes/edit/{wish_id}")
    
    update_wish = Wish.objects.get(id=wish_id)
    update_wish.item = request.POST['item_name']
    update_wish.desc = request.POST['item_description']
    update_wish.save()

    # return to the list of wishes if we are successful
    return redirect('/wishes/')


def verify_logged_in(request):
    if not 'id' in request.session:
        print("Value missing from session in VLI")
        return False
    return True
    
    # return the user object to save code in all the functions above
    # return User.objects.get(id=request.session['id'])

def valid_post_request(request):
    if request.method != "POST":
        print("Non-POST request attempted")
        return False
    if not 'id' in request.session:
        print("Not logged in, sending back to login page:", request.get_full_path)
        return False
    # they appear to be authenticated and they are suppossed to be here (post request)
    return True

#######################################################################################
#  Black Belt options

# pull user id from session to get stats
def stats(request):
    print("In stats method - black belt option")
    if not verify_logged_in(request):
        return redirect('/')

    total_granted_wishes = Wish.objects.filter(is_granted=True)
    user_granted_wishes = Wish.objects.filter(is_granted=True, user_id=request.session['id'])
    user_wishes = Wish.objects.filter(is_granted=False, user_id=request.session['id'])

    context = {
        "user": User.objects.get(id=request.session['id']),
        "total_granted_wishes": len(total_granted_wishes),
        "your_granted_wishes": len(user_granted_wishes),
        "your_pending_wishes": len(user_wishes),
    }
    return render(request, 'stats.html', context)

def like(request, wish_id):
    print("In stats method - black belt option")
    if not verify_logged_in(request):
        return redirect('/')

    # using a many to many linking table we can create a relationship
    #   between likes and users to prevent liking too many things
    this_user = User.objects.get(id=request.session['id'])
    this_wish = Wish.objects.get(id=wish_id)
    this_wish.likes.add(this_user)

    # the reason this can work is because you can only add the relationship
    #    ONE time...any additional attempts will just skip adding it to the table
    # Once you have liked something, you can't get added again!!
    return redirect('/wishes/')
