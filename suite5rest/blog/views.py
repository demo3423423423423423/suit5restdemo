from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Writer, Article, Blog
from .serializers import WriterSerializer, ArticleSerializer, BlogSerializer

'''
    Articles, Writers, Blogs ---- POST Request and GET Request
'''
@csrf_exempt
def writer_list(request):
    if request.method == 'GET':
        writers = Writer.objects.all()
        serializer = WriterSerializer(writers, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = WriterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ArticleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def blog_list(request):
    if request.method == 'GET':
        articles = Blog.objects.all()
        serializer = BlogSerializer(articles, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = BlogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


'''
    Single Article, Single Writer, Single Blog ---- GET,POST,PUT,DELETE
'''


@csrf_exempt
def writer_detail(request, pk):
    """
    Retrieve, update or delete a writer.
    """
    try:
        writer = Writer.objects.get(pk=pk)
    except Writer.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = WriterSerializer(writer)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = WriterSerializer(writer, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        writer.delete()
        return HttpResponse(status=204)


def article_action_per_method(request, article):

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ArticleSerializer(article, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        article.delete()
        return HttpResponse(status=204)

    return HttpResponse(status=404)


@csrf_exempt
def article_detail(request, pk):
    """
    Retrieve, update or delete an article.
    """
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return HttpResponse(status=404)

    return article_action_per_method(request, article)


@csrf_exempt
def blog_detail(request, pk):
    """
    Retrieve, update or delete a blog.
    """
    try:
        blog = Blog.objects.get(pk=pk)
    except Blog.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = BlogSerializer(blog)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = BlogSerializer(blog, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        blog.delete()
        return HttpResponse(status=204)


@csrf_exempt
def writer_article_action(request, writer_pk, article_pk=None):
    """
    Retrieve, update or delete an article.
    """
    try:
        writer = Writer.objects.get(pk=writer_pk)
    except Writer.DoesNotExist:
        return HttpResponse(status=404)

    if not article_pk:
        if request.method == 'GET':
            articles = Article.objects.filter(writer=writer_pk)
            serializer = ArticleSerializer(articles, many=True)
            return JsonResponse(serializer.data, safe=False)
        elif request.method == 'POST':
            data = JSONParser().parse(request)
            data.update({'writer': writer_pk})
            serializer = ArticleSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)

        return HttpResponse(status=404)

    try:
        article = Article.objects.get(pk=article_pk, writer=writer_pk)
    except Article.DoesNotExist:
        return HttpResponse(status=404)

    return article_action_per_method(request, article)


@csrf_exempt
def writer_blog_action(request, writer_pk, article_pk, blog_pk):
    """
    Retrieve, update or delete an article.
    """
    try:
        writer = Writer.objects.get(pk=writer_pk)
    except Writer.DoesNotExist:
        return HttpResponse(status=404)

    try:
        article = Article.objects.get(pk=article_pk, writer=writer_pk)
    except Article.DoesNotExist:
        return HttpResponse(status=404)

    try:
        blog = Blog.objects.get(pk=blog_pk)
    except Blog.DoesNotExist:
        return HttpResponse(status=404)

    serializer = BlogSerializer(blog)
    if request.method == 'PUT':
        serializer = BlogSerializer(blog)
        serializer.data['articles'].append(article_pk)

    elif request.method == 'DELETE':
        serializer = BlogSerializer(blog)
        try:
            serializer.data['articles'].remove(article_pk)
        except:
            pass
    if request.method in  ('DELETE', 'PUT'):
        serializer = BlogSerializer(blog, data=serializer.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)

    return HttpResponse(status=404)



@csrf_exempt
def blog_article_action(request, blog_pk):
    """
    Retrieve, update or delete an article.
    """
    try:
        blog = Blog.objects.get(pk=blog_pk)
    except Blog.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = BlogSerializer(blog)
        articles = []
        for article_pk in serializer.data['articles']:
            articles.append(Article.objects.get(id=article_pk))
        serializer = ArticleSerializer(articles, many=True)
        return JsonResponse(serializer.data, safe=False)