from django.http import HttpResponse

def some_view(request):
    return HttpResponse("Hello, this is the auction app!")
