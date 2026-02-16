from django.shortcuts import render, redirect, get_object_or_404
from .models import Snippet
from .forms import SnippetForm, RejestracjaForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


@login_required
def snippet_list(request):
    if request.user.is_teacher or request.user.is_superuser:
        snippets = Snippet.objects.all().order_by('-created_at')
    else:
        snippets = Snippet.objects.filter(author=request.user).order_by('-created_at')
    
    context = {
        'lista_snippetow': snippets
    }
    
    return render(request, 'snippets/snippet_list.html', context)

@login_required
def snippet_new(request):
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            # Zatrzymujemy automatyczny zapis formularza
            snippet = form.save(commit=False)
            
            # przypisanie autora
            snippet.author = request.user
            snippet.save()

            return redirect('lista_kodow')
    else:
        form = SnippetForm()
    
    return render(request, 'snippets/snippet_edit.html', {'form': form})

def snippet_detail(request, pk):
    snippet = get_object_or_404(Snippet, pk=pk)

    if snippet.author != request.user and not request.user.is_teacher and not request.user.is_superuser:
        raise PermissionDenied("Brak dostępu do kodu innego użytkownika")

    return render(request, 'snippets/snippet_detail.html', {'snippet': snippet})

def rejestracja(request):
    if request.method == 'POST':
        form = RejestracjaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RejestracjaForm()

    return render(request, 'registration/rejestracja.html', {'form': form})