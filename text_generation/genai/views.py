from django.shortcuts import render, redirect
from django.http import JsonResponse 
from groq import Groq
from django.contrib import auth
from django.contrib.auth.models import User 
from . models import Chat
from django.utils import timezone 


#Authentification
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user) # for loging directly
                return redirect('chatbot')
            except:
                error_message = 'Error creating account'
                return render(request, "chatbot/register.html", {"error_message": error_message})
        else:
            error_message = "Password don't match"
            return render(request, "chatbot/register.html", {"error_message": error_message})
    return render(request, "chatbot/register.html")


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Check if the user laready registered 
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error_message = "Invalid username or password!"
            return render(request, "chatbot/login.html", {"error_message": error_message})
    else:    
        return render(request, "chatbot/login.html")


def logout(request):
    auth.logout(request)
    return redirect('login') # after logout redirect user to login

GROQ_API_KEY = "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"

def ask_llama(message): 
    client = Groq(api_key=GROQ_API_KEY)

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "AI Chatbot"},
            {"role": "user", "content": "Conversation"},
            {"role": "assistant", "content": "I'm happy to chat with you. How's your day going so far?\n\n(Type a response, ask a question, or share a topic you'd like to discuss. I'm all ears... or rather, all text!)"},
            {"role": "user", "content": message}
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None
    )

    # Collect and join streamed chunks
    chunks = []
    for chunk in completion:
        content = chunk.choices[0].delta.content
        if content:
            chunks.append(content)

    # Combine chunks into a single string
    full_response = ''.join(chunks).strip()

    # Optional: normalize paragraph formatting (2 line breaks between paragraphs)
    formatted_text = '\n\n'.join(p.strip() for p in full_response.split('\n\n') if p.strip())

    return formatted_text

"""
def chatbot(request):
    # Get all the chat from the currently login user
    chats = Chat.objects.filter(user=request.user)
    chats = Chat.objects.filter(user=request.user)
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_llama(message) # ask_deepseek(message) #"Hi this is my response"

        # save user messages
        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
       
        return JsonResponse({'message': message, 'response': response})
    
    return render(request, "chatbot/chatbot.html", {"chats":chats})

 """

def chatbot(request):
    if not request.user.is_authenticated:
        return redirect('login')  # or show an error page

    chats = Chat.objects.filter(user=request.user)

    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_llama(message)

        chat = Chat(
            user=request.user,
            message=message,
            response=response,
            created_at=timezone.now()
        )
        chat.save()

        return JsonResponse({'message': message, 'response': response})
    
    return render(request, "chatbot/chatbot.html", {"chats": chats})
