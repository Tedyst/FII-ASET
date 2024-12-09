from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import DocumentUploadForm


def index(request):
    return render(request, "index.html")


@login_required
def upload_documents(request):
    if request.method == "POST":
        form = DocumentUploadForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = DocumentUploadForm(instance=request.user)
    return render(request, "upload_documents.html", {"form": form})
