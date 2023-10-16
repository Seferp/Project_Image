# Project_Image

# Requirements:
- it should be possible to easily run the project. docker-compose is a plus
- users should be able to upload images via HTTP request
- users should be able to list their images
- there are three builtin account tiers: Basic, Premium and Enterprise:
- users that have "Basic" plan after uploading an image get: 
    - a link to a thumbnail that's 200px in height
- users that have "Premium" plan get:
    - a link to a thumbnail that's 200px in height
    - a link to a thumbnail that's 400px in height
    - a link to the originally uploaded image
- users that have "Enterprise" plan get
    - a link to a thumbnail that's 200px in height
    - a link to a thumbnail that's 400px in height
    - a link to the originally uploaded image
    - ability to fetch an expiring link to the image (the link expires after a given number of seconds (the user can specify any number between 300 and 30000))
- apart from the builtin tiers, admins should be able to create arbitrary tiers with the following things configurable:
    - arbitrary thumbnail sizes
    - presence of the link to the originally uploaded file
    - ability to generate expiring links
- admin UI should be done via django-admin
- there should be no custom user UI (just browsable API from Django Rest Framework)
- remember about:
    - tests
    - validation
    - performance considerations (assume there can be a lot of images and the API is frequently accessed)


As instructed, I created the necessary user accounts in the admin panel.

# Basic user
Basic user can add image by POST method. 
![image](https://github.com/Seferp/Project_Image/assets/111074557/3d434b69-3b73-44eb-adda-8e31b3d28356)

After that received link URL to miniature of original image in 200px in height.
![image](https://github.com/Seferp/Project_Image/assets/111074557/197ff2f1-e3fd-43ee-9d52-43bc4f8ae112)

# Premium user
Similar to basic user, premium user can add image but received also link URL to image in 400px in height and to original image.
![image](https://github.com/Seferp/Project_Image/assets/111074557/353068af-adee-417b-b11b-6a2af74a9976)
![image](https://github.com/Seferp/Project_Image/assets/111074557/883b2e0e-4fa1-4c07-b369-4341fbc24207)

# Enterprise user
The last account tier after upload image as premium user received links URL to image in size 200px and 400px in height and to original image.
Except that, enterprise user also received expired link URL to download original image.
The time after which the link expires is given by enterprise user when sending the image in field "Expired time" and it should be less than 300 seconds and greater than 30000 seconds.
![image](https://github.com/Seferp/Project_Image/assets/111074557/686549b9-2b68-45a3-8717-b0e2d8623a21)
![image](https://github.com/Seferp/Project_Image/assets/111074557/1d00ea73-7f33-4617-8caf-a443eab906b5)

## How To Set Up Locally
- clone the repo
- create super user account in terminal
- visit http://127.0.0.1:8000/admin/ and login with you username and password
- create account tier which you need
- visit http://127.0.0.1:8000/login/ and login with username and password for your new acount
- now you can uploud image
If you need switch between two or more accounts, you can use logout URL: http://127.0.0.1:8000/logout/ - automatically logout from current account

