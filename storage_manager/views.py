from django.shortcuts import render


# Create your views here.
def stm_index(request):

    return render(request, 'storage_manager/stm_index.html')
