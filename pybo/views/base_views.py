from django.shortcuts import render,get_object_or_404,redirect
from ..models import Question
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
import logging
logger = logging.getLogger('pybo')

def index(request):
    logger.info("INFO 레벨로 출력")
    page = request.GET.get('page','1') # 페이지
    kw = request.GET.get('kw', '')  #검색어
    question_list = Question.objects.order_by('-create_date')
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  #제목검색
            Q(content__icontains=kw) |  #내용검색
            Q(answer__content__icontains=kw) | #답변내용 검색
            Q(author__username__icontains=kw) | #질문 글쓴이 검색
            Q(answer__author__username__icontains=kw) #답변 글쓴이 검색
        ).distinct()
    paginator = Paginator(question_list, 10 ) # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = { 'question_list': page_obj, 'page':page, 'kw':kw } # question_list는 페이징 객체(page_obj)
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)