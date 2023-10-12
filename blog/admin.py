from django.contrib import admin
# Tâm An
from .models import Post, Comment, User, Like,Categori
# from blog.models import UserProfileInfo

# Tâm An


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'password', 'fullname','avatar','Interaction_score','role' )
    search_fields = ['Fullname', 'Create_at', 'Updated_at','Role']
admin.site.register(User, UserAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ['title','Author','Category','status', 'views', 'likes', 'comments']
    search_fields = ['title', 'content','status']
    def Author(self, obj):
        return obj.author.fullname
    def Category(self, obj):
        return obj.categori.name   
admin.site.register(Post,PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['Title', "User", 'content', "created_at"]
    search_fields = ["Title", "User", "content"]
    def Title(self, obj):
        return obj.post.title
    def User(self, obj):
        return obj.user.fullname
admin.site.register(Comment,CommentAdmin)

class LikeAdmin(admin.ModelAdmin):
    list_display = ['Title', "User", 'like_status', "created_at"]
    search_fields = ['Title', 'User', 'like_status']
    def Title(self, obj):
        return obj.post.title
    def User(self, obj):
        return obj.user.fullname
    # Chỉ lấy những thằng đã like, unlike cút
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.filter(like_status='0')
        return queryset   
admin.site.register(Like,LikeAdmin)

class CateAdmin(admin.ModelAdmin):
    list_display = ['name', "Category_Parent"]
    search_fields = ['name','Category_Parent']
    def Category_Parent(self, obj):
        if obj.parent:
            return obj.parent.name
        else:
            return "Root"
admin.site.register(Categori, CateAdmin)


