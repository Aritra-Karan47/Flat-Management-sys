from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# removed top-level model import to avoid circular imports

def index(request):
    return home(request)
def home(request):
    from .models import Society  # lazy import to prevent circular import
    if request.user.is_authenticated:
        if not getattr(request.user, 'society', None):
            societies = Society.objects.all()
            if request.method == 'POST':
                society_id = request.POST.get('society')
                request.user.society = Society.objects.get(id=society_id)
                request.user.save()
                return redirect('dashboard')
            return render(request, 'core/home.html', {'societies': societies})
        return redirect('dashboard')
    return redirect('account_login')

@login_required
def dashboard(request):
    # lazy/defensive access if user has no is_admin attr
    is_admin = getattr(request.user, 'is_admin', False)
    context = {'is_admin': is_admin}
    return render(request, 'core/dashboard.html', context)
