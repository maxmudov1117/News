from django.contrib import admin
from .models import *
from django.contrib.auth.models import User, Group
from django.utils.html import format_html


admin.site.unregister([User,Group])
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name',)
    list_editable = ("name",)
    search_fields = ('name',)



@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class InlineContext(admin.StackedInline):
    model = Context
    extra = 1

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'cover_image', 'published', 'views', 'read_time', 'author', 'important',)
    list_display_links = ('id',)
    list_editable = ('title', 'published', 'read_time', 'author',)
    ordering = ('views','read_time')
    list_filter = ('category', 'published')
    search_fields = ('category', 'author')

    inlines = [InlineContext,]

    def cover_image(self, obj):
        if obj.cover:
            return format_html(
                '<img src="{}" width="70" height="50" style="object-fit:cover; border-radius: 6px;" />',
                obj.cover.url
            )
        return "-"
    cover_image.short_description = "Cover"  # Admin paneldagi ustun nomi

@admin.register(Context)
class ContextAdmin(admin.ModelAdmin):
    list_display = ('id','text', 'image', 'article', 'created_at', )
    list_editable = ('text',)
    list_display_links = ('id',)
    search_fields = ('text',)
    list_filter = ('article',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','text', 'author', 'email', 'published', 'created_at', )
    search_fields = ('text', 'email','author')
    list_editable = ('published',)
    list_filter = ('author', 'email',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'message', 'created_at', 'seen',)
    list_per_page = 10
    list_editable = ('seen',)
    search_fields = ('name', 'email', 'subject',)
    list_filter = ('subject', 'name', 'seen',)


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email',)
    search_fields = ('email',)