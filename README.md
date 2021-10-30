# Face Recognition Service

This is a simple service containing an API used to do facial recognition.

I built it thinking as an authentication service that can receive as query parameters:
- A return url
- A JWT token containing information about the user you want to authenticate

You can use JWT.io to generate a token.  Use the static secret in `authentication_flow.py` as the secret.
The JWT must contain at least an user id, like this:

`
{
    user_id: 3
}
`

# Development

You must have MongoDB installed locally and running, either normally or via Docker.

Before running, create a local environment to keep things tidy, such as

```python3 -m venv facerecognition```

and activate it by doing

``` source facerecognition/bin/activate```

Then install the dependencies by running:

```pip install -r requirements.txt```

To test the full authentication flow, do the following:

1 - Use postman or another tool of your preference to make a POST
    to localhost:8000/user/<any_user_id_you_want>/seeds

    The body is a Form Data, with the only field being "image", and must be a jpg or png file,
    which should be a picture of the person you want this user to be.

    You do not need to create any_user_id_you_want, as the endpoint will create if it doesn't exist.
    You can upload as many pictures as you want per user, but be sure that they are from the same
    person, otherwise it might mess the comparison. The system will compare against all pictures, and 
    return the average.

2 - Go to JWT.io, generate a jwt token containing a payload such as:
    ```{ user_id: <the user id you want to compare> }```
    The secret must be the same present in authentication_flow.py

3 - Go to localhost:8000/authentication-check?returnUrl=<the_return_url_you_want>&token=<the_jwt_you_generated>
    Follow the instructions.


# Notes

I am aware that this project is far from ideal in terms of code quality, but it was made 
as a test to an idea that I had, and honestly, I find it pretty cool. There are no tests, but
I have some plans to add some.

# Contributing

Pull requests are welcome.