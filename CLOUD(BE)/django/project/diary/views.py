from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import diary
from .forms import DiaryForm
from django.core.paginator import Paginator

def index(request):
    page = request.GET.get('page', '1')
    diary_list = diary.objects.order_by('-date')
    paginator = Paginator(diary_list,10)
    page_obj = paginator.get_page(page)
    context = {'diary_list':page_obj}
    return render(request, 'diary/diary_list.html', context)

def detail(request, diary_id): 
    Diary = get_object_or_404(diary,pk=diary_id)
    context = {'diary' : Diary}
    return render(request, 'diary/diary_detail.html', context)
# 일기는 원래 자기가 작성한 일기만 볼 수 있어야 하는데, 현재 그 기능이 없어 모든 일기를 열어볼 수 있습니다.
# 혹시 다른 사람의 일기를 열어보는 일을 방지하기 위해, 위의 함수에 로그인된 ID랑 diary object의 USER_ID가 같은지 확인하는 과정이 필요합니다.

def diary_write(request):
    if request.method == 'POST':
        form = DiaryForm(request.POST)
        if form.is_valid():
            Diary = form.save(commit=False)
            Diary.date = timezone.now()
            Diary.save()
            return redirect('diary:index')
    else:
        form = DiaryForm()
    context = {'form': form}
    return render(request, 'diary/diary_form.html', context)