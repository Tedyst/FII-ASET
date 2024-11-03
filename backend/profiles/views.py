from django.shortcuts import render


# Create your views here.
def test(request):
    # return base.html template
    return render(request, "base.html")
