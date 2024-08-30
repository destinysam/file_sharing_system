# File Sharing Management System


## Project Setup

1. Clone the repository using
```
git clone https://github.com/destinysam/file_sharing_system.git
```
2. Setup the enviornment using
```
python3 -m venv env
```
4. Activate the environment (Linux only)
```
source env/bin/activate
```
4. install the dependency into it
```
pip install -r requirements.txt
```
5. Make migrations
```
python3 manage.py makemigrations
```
6. Migrate migrations
```
python3 manage.py migrate
```
7. To run server
```
python3 manage.py runserver
```

## Project Architect

### This project consists of 3 apps:

1. **users** -> Used to manage the user related stuff like api's, models.
   
2. **file_management** -> Used to manage user file uploads and recieved files.
  
3. **chat** -> Used to manage chat/messaging on file uploads and shared files.



## DataBase Schema

1. **User(Django)** -> Used to manage user details.

2. **File** -> Used to manage file uploads.

3. **Message** -> Used to manage messages/chat on spacific files.


## API's

### users app

1. **SignUpAPI** -> Used to register users.

2. **SigninAPI** -> Used to Signin users and get access token,refresh token.

3. **RefreshAccessTokenAPI** -> Used to get access token using refresh token.


### file_management app

1. **FileUploadAPI** -> Used to upload files.

2. **ListFileUploadAPI** -> Used to list uploaded files of current user.

3. **ListRecievedFileAPI** -> Used to list recieved files of current user.


### chat app

1. **SendMessageAPI** -> Used to send message on spacific file.

2. **LongPoolingFileMessageAPI** -> List messages on spacific file using long pooling.
   




