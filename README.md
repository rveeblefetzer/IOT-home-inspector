#Internet of Things Home Inspector

**Purpose:** To identify and provide resources for updates to your Internet of Things devices whether you search for them on the site or connect your IoT device directly to our site.

**Authors**

Rick Valenzuela

Regenal Grant

Joseph Derosa

Conor Clary

**Setup Instructions**

Use the git clone command to ```git clone https://github.com/rveeblefetzer/IOT-home-inspector.git``` into your directory of choice.

Install a virtual environment with ```python3 -m venv .``` or ```python3 -m venv /[some_env_directory_name]```

Activate the virtual environment with ```. [path/to/bin/activate]```

Navigate to the IOThomeinspector directory to the same level as requirements.pip

Install the app with ```pip install -r requirements.pip```

At this point please ensure that in your virtual environment activate file you have a DB_USER, DB_PASS, EMAIL_PASS, and EMAIL_ACCT exported. You can also set these up in your settings.py file in IOT-home-inspector/IOThomeinspector/IOThomeinspector/settings.py

At the same level as requirements.pip, use the ```createdb IOT``` command to create the IOT database for users

Use the ```./manage.py makemigrations``` and ```./manage.py migrate``` commands to move your models to the newly created database. 

You can now run ```./manage.py runserver``` to run the site from your command line. By default the site will run on port 8000.

##Routes

```
   admin/
   / #The home page route
   /registration/register #The route for a new user to register
   /login #The login route for users. Users will be prompted to input a verification code from the 2 Factor Authentication
   /logout #Logs out the user
   /profile #A user can view their own profile. No social sharing here.
   user/password/reset/ #Route to reset a password
```

## Two-factor authentication
Any visitor can use the site's basic function of entering a device model and receiving information on the current software and/or firmware versions. Registered users can use the site to maintain a list of their devices. They can also choose to add two-factor authentication (2fa) to their login process, which is implemented through the [django-two-factor-auth library](https://django-two-factor-auth.readthedocs.io/en/stable/). Currently this is implemented through time-based tokens using an app such as [Google Authenticator](https://support.google.com/accounts/answer/1066447) or [Authy](https://www.authy.com), or a from a listed of generated backup tokens. Site admins must use two-factor authentication.

To see how 2fa works for the end user, as well as this implementation in Django, you can try it out in [this example app](https://example-two-factor-auth.herokuapp.com/).
```
