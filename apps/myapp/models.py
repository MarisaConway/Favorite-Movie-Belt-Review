from django.db import models
import re
import datetime
import bcrypt

class UserManager(models.Manager):
    def reg_validator(self, form):

        errors = {}
        EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]+$")

        fname = form['fname']
        lname = form['lname']
        email = form['email']
        birthday = form['birthday']
        password = form['password']
        confirm_pw = form['confirm_password']
        print(birthday)
        if len(fname) < 2:
            errors['fname'] = "First name cannot be blank"
        elif not fname.isalpha():
            errors['fname'] = "First name cannot contain number or special characters!"
        if len(lname) < 2:
            errors['lname'] = "Last name cannot be blank"
        elif not lname.isalpha():
            errors['lname'] = "Last name cannot contain number or special characters!"
        if len(email) < 1:
            errors['email'] = "Email cannot be blank"
        elif not EMAIL_REGEX.match(email):
            errors["email"]="Invalid email format"
        else:
            users = User.objects.filter(email=email)
            if len(users) > 0:
                errors['email'] = "Email already exists. Please login."
        if not birthday:
            errors['birthday'] = "Please enter a birth date"
        elif birthday > str(datetime.datetime.now()):
            errors['birthday'] = "Sorry you don't exist"
        elif datetime.datetime.now()-datetime.datetime.strptime(birthday, "%Y-%m-%d")<=datetime.timedelta(days=4745):
            errors['birthday'] = "You are too young for this site get a credit card"
        if len(password) < 8:
            errors['password'] = "Password must be at least 8 characters"
        elif password != confirm_pw:
            errors['confirm_pw'] = "Passwords do not match"
        

        return errors
            
    
    def loginvalidator(self, form):
        errors = {}
        email = form['email']
        password = form['password']
        if len(email) < 0:
            errors["email"] = "Please enter emails"
        elif len(User.objects.filter(email = email)) < 1:
            errors['email'] = "Email not in database please register!"
        else:
            if not bcrypt.checkpw(password.encode(), User.objects.get(email = email).password.encode()):
                errors['email'] = "No No Nooo!"
                
        return errors

class MovieManager(models.Manager):
    def movie_validator(self, form):

        errors = {} 
        title = form['title']
        year = form['year']
        # print(form)  print form to terminal for debugging
        if len(title) < 2:
            errors["title"] = "Title is too short"
        if len(year) < 1:
            errors["year"] = "Year cannot be blank"
        elif int(year) < 1888:
            errors["year"] = "There were no movies then"
        elif int(year) > 2019:
            errors["year"] = "This isnt Back to the Future"
            # fix later
        return errors       

class User(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    birthday = models.DateField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    """uploaded_movies get list of uploaded movies for user"""
    """favorites get list of favorited movies for user"""

    
    objects = UserManager()
class Movie(models.Model):
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    addedby = models.ForeignKey(User, related_name="uploaded_movies", on_delete=models.CASCADE)
    favorites=models.ManyToManyField(User,related_name="favorites")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)

    objects = MovieManager()