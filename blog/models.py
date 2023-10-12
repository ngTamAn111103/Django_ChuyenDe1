from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Danh mục bài viết
class Categori(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='cate_chill')
    def __str__(self):
        # return f'ID: {self.id}\n' + f'Name: {self.name}\n' + f'Parent: {self.parent}'
        return f'ID: {self.id:<10} | Name: {self.name:<25} | Parent: {self.parent_id:<25} |'
    
        
    
    
# User sử dụng web blog
class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    fullname = models.CharField(max_length=255)
    avatar = models.ImageField(default='/MyBlogProject/media/9-anh-dai-dien-trang-inkythuatso-03-15-27-03.jpg', null=True)
    created_at = models.DateTimeField(auto_now_add=True, null= True)
    updated_at = models.DateTimeField(auto_now_add=True, null = True)
    # Trường role có giá trị 0 hoặc 1
    role = models.IntegerField(choices=[(0, 'Người dùng'), (1, 'Quản trị viên')], default=0)
    # Trường Level  là khóa ngoại với bảng Level
    Interaction_score  = models.IntegerField(default=0)
    def __str__(self):
        return self.fullname
    
    # Tâm An
    def login(username, password):
        users =User.objects.all().filter(username=username, password = password)
        return users
        # for user in users:
        #     if user.username == username and user.password == password: 
        #         return user
        # return None
                
    # def login(self, User):
    #     if self.username == User.username and self.password == User.password:
    #         return User
    #     else:
    #         return "KO có tài khoản"

# Post bài viết trên web blog
class Post(models.Model):
    title =models.CharField(max_length=255)
    content = models.TextField()
    author  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_post')
    categori  = models.ForeignKey(Categori, on_delete=models.CASCADE, related_name='categori_post') 
    thumbnail = models.ImageField(upload_to='Volumes/DATA/Python_Django/MyBlogProjec/static/images/', null=True)
    status = models.IntegerField(choices=[(0, 'Public'), (1, 'Pravited')], default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    def __str__(self):
        return self.title
    def publish(self):
        self.status = 0
        self.save()

    
class Like (models.Model):
    post  = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='like_post')
    user  = models.ForeignKey(User, on_delete=models.CASCADE , related_name='user_like')
    like_status = models.IntegerField(choices=[(0, 'Liked'), (1, 'Unlike')], default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.post.title

class Comment (models.Model):
    # id = models.AutoField(primary_key=True)
    post  = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment_post')
    user  = models.ForeignKey(User, on_delete=models.CASCADE , related_name='user_comment')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.post.title
    
    

# Lâm: Login
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    portfolito_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pic', blank=True)

    def __str__(self):
        return self.user.username