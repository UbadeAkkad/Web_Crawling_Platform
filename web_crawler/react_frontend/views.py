from django.shortcuts import render

def Reactindex(request, path=''):
    return render(request,'build/index.html', context={'context_variable': 'value'})