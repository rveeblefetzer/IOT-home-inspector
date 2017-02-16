#Internet of Things Home Inspector

**Purpose:** To identify and provide resources for updates to your Internet of Things devices whether you search for them on the site or connect your IoT device directly to our site.

**Authors**

Rick Valenzuela

Regenal Grant

Joseph Derosa

Conor Clary

**Setup Instructions**
```
git clone https://github.com/rveeblefetzer/IOT-home-inspector.git
```

## Two-factor authentication
Any visitor can use the site's basic function of entering a device model and receiving information on the current software and/or firmware versions. Registered users can use the site to maintain a list of their devices. They can also choose to add two-factor authentication (2fa) to their login process, which is implemented through the [django-two-factor-auth library](https://django-two-factor-auth.readthedocs.io/en/stable/). Currently this is implemented through time-based tokens using an app such as [Google Authenticator](https://support.google.com/accounts/answer/1066447) or [Authy](https://www.authy.com), or a from a listed of generated backup tokens. Site admins must use two-factor authentication.

To see how 2fa works for the end user, as well as this implementation in Django, you can try it out in [this example app](https://example-two-factor-auth.herokuapp.com/).
```
