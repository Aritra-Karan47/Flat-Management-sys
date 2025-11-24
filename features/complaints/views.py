from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from django.db.models import Q
from .models import Complaint, Comment, Category
import requests 

@login_required
def complaint_list(request):
    society = request.user.society
    if not society:
        return redirect('home')
    complaints = Complaint.objects.filter(society=society).select_related('created_by')
    return render(request, 'complaints/list.html', {'complaints': complaints})

class CreateComplaintView(View):
    @method_decorator(login_required)
    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'complaints/create.html', {'categories': categories})

    @method_decorator(login_required)
    def post(self, request):
        society = request.user.society
        if not society:
            return redirect('home')
        complaint = Complaint.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            category_id=request.POST['category'],
            society=society,
            created_by=request.user,
            photo=request.FILES.get('photo')
        )
        return redirect('complaint_list')

@login_required
@require_http_methods(["POST"])
def upvote_complaint(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk, society=request.user.society)
    user = request.user
    if user not in complaint.upvotes.all():
        complaint.upvotes.add(user)
    count = complaint.upvotes.count()
    return JsonResponse({'count': count, 'upvoted': True})

@login_required
@require_http_methods(["POST"])
def add_comment(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk, society=request.user.society)
    text = request.POST.get('text')
    parent_id = request.POST.get('parent_id')
    parent = Comment.objects.get(id=parent_id) if parent_id else None
    Comment.objects.create(
        complaint=complaint,
        text=text,
        created_by=request.user,
        parent=parent
    )
    comments = complaint.comments.all()
    return JsonResponse({'status': 'added', 'comments_count': comments.count()})

@login_required
def complaint_detail(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk, society=request.user.society)
    comments = complaint.comments.all()
    return render(request, 'complaints/detail.html', {'complaint': complaint, 'comments': comments})