import os

UPLOAD_FOLDER = './src/uploaded_images'
USERS_PETS_FOLDER = './src/uploaded_images/users_pets'
UPLOAD_FOLDER_VIDEOS = './src/uploaded_videos/'


def get_user_mail(file):
    filename = file.filename
    user_mail_and_timestamp = filename.split('&')
    return user_mail_and_timestamp[0]


def get_latest_file_in_directory(directory_path):
    files = os.listdir(directory_path)
    files.sort(key=lambda x: os.path.getmtime(os.path.join(directory_path, x)))
    return os.path.join(directory_path, files[-1])


def save_file_in_directory(file, directory):
    user_mail = get_user_mail(file)
    new_user_mail_directory = os.path.join(directory, user_mail)
    if not os.path.exists(new_user_mail_directory):
        os.makedirs(new_user_mail_directory)
    file.save(os.path.join(new_user_mail_directory, file.filename))



