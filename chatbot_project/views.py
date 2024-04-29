from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai
from django.contrib import auth
from django.contrib.auth.models import User
import os

open_ai_key = os.environ.get("API_KEY")
openai.api_key = open_ai_key


def ask_openai(message):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    # print(response)
    answer = response.choices[0].text.strip()
    return answer


# Create your views here.
def chatbot(request):
    if request.method == "POST":
        message = request.POST.get("message")
        print(message)
        response = ask_openai(message)
        print(response)
        return JsonResponse({"message": message, "response": response})
    return render(request, "chatbot.html")


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("chatbot")
        else:
            error = "ERROR"
            return render(request, "register.html", {"error": error})
    else:
        return render(request, "login.html")


def logout(request):
    auth.logout(request)
    return redirect("login")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 == password2:
            try:
                user = User.objects.create_user(user, email, password1)
                user.save()
                auth.login(request, user)
                return redirect("chatbot")
            except:
                error = "ERROR"
                return render(request, "register.html", {"error": error})
        else:
            error = "Incorrect PW"
            return render(request, "register.html", {"error": error})
    return render(request, "register.html")
