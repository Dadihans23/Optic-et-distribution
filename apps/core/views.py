from django.shortcuts import render


def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')
