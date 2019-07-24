import requests, json, sys, os
from datetime import datetime, timedelta
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "baby2body.settings")

django.setup()
from retroville.users.models import User
from retroville.stories.models import Story
from retroville.stories.models import UserReadStory

def main():


    for i in range(10):
        user = User.objects.create_user(email=f'vaughndevilliers+{i}@baby2body.com',
                                        username=f'vaughn{i}',
                                        password='password123')




if __name__ == '__main__':
    main()