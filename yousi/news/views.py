from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DeleteView
from yousi.helpers import ajax_required, AuthorRequiredMixin

from yousi.news.models import News


# class NewsListView(LoginRequiredMixin, ListView):
#     """首页动态"""
#     # model = News
#     # paginate_by = 10
#     # context_object_name = None
#     # template_name = 'news/news_list.html'
#     template_name = 'index.html'
#     def get_queryset(self, **kwargs):
#         return News.objects.filter(reply=False)


class NewsListView(LoginRequiredMixin, ListView):
    """首页动态"""
    model = News
    paginate_by = 10
    context_object_name = None
    template_name = 'news/news_list.html'

    def get_queryset(self, **kwargs):
        return News.objects.filter(reply=False)

class NewsDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    """继承DeleteView重写delete方法，使用AJAX响应请求"""
    model = News
    template_name = 'news/news_confirm_delete.html'
    slug_url_kwarg = 'slug' #通过URL传入要删除的对象主键id,默认slug
    pk_url_kwarg = 'pk' #通过url传入要删除的对象主键id,默认值是pk

    success_url = reverse_lazy("news:list")  # 在项目的URLConf未加载前使用



@login_required
@ajax_required
@require_http_methods(["POST"])
def post_news(request):
    """发送动态，AJAX POST请求"""
    post = request.POST['post'].strip()
    if post:
        posted = News.objects.create(user=request.user, content=post)
        html = render_to_string('news/news_single.html', {'news': posted, 'request': request})
        return HttpResponse(html)
    else:
        return HttpResponseBadRequest("内容不能为空！")


@login_required
@ajax_required
@require_http_methods(["POST"])
def like(request):
    """点赞，AJAX POST请求"""
    news_id = request.POST['news']
    news = News.objects.get(pk=news_id)
    # 取消或者添加赞
    news.switch_like(request.user)
    # 返回赞的数量
    return JsonResponse({"likes": news.count_likers()})


@login_required
@ajax_required
@require_http_methods(["GET"])
def get_thread(request):
    """返回动态的评论，AJAX GET请求"""
    news_id = request.GET['news']
    news = News.objects.get(pk=news_id)
    # render_to_string()表示加载模板，填充数据，返回字符串
    news_html = render_to_string("news/news_single.html", {"news": news})  # 没有评论的时候
    thread_html = render_to_string("news/news_thread.html", {"thread": news.get_thread()})  # 有评论的时候
    return JsonResponse({
        "uuid": news_id,
        "news": news_html,
        "thread": thread_html,
    })

@login_required
@ajax_required
@require_http_methods(["POST"])
def post_comment(request):
    """评论，AJAX POST请求"""
    post = request.POST['reply']
    parent_id = request.POST['parent']
    parent = News.objects.get(pk=parent_id)
    post = post.strip()
    if post:
        parent.reply_this(request.user, post)
        return JsonResponse({'comments': parent.comment_count()})
    else:  # 评论为空返回400.html
        return HttpResponseBadRequest("内容不能为空！")


@login_required
@ajax_required
@require_http_methods(["POST"])
def update_interactions(request):
    """更新互动信息"""
    data_point = request.POST['id_value']
    news = News.objects.get(pk=data_point)
    data = {'likes': news.count_likers(), 'comments': news.comment_count()}
    return JsonResponse(data)
