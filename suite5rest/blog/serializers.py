from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework import serializers
from .models import Writer, Article, Blog


class WriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Writer
        fields = ('id', 'name', 'age', 'email', 'address')


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'excerpt', 'text', 'writer', 'image')


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ('id', 'title', 'articles')
