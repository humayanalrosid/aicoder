from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, LoginForm
from .models import Code

import openai

# API KEY : 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

def home(request):
    if not request.user.is_authenticated:
        return render(request, 'app/home.html', {'nbar':'home'})
    else:
        return redirect('fix')

def fix(request):
    if request.user.is_authenticated:
        lang_list = ["html", "markup", "css", "clike", "javascript", "c", "csharp", "cpp", "dart", "django", "go", "java", "markup-templating", "matlab", "mongodb", "objectivec", "perl", "php", "powershell", "python", "r", "regex", "ruby", "rust", "sass", "scala", "sql", "swift", "typescript", "yaml" ]
        
        if request.method == "POST":
            code = request.POST['code']
            lang = request.POST['lang']

            if lang == "Select programming language":
                messages.warning(request, "You forget to pick a programming language.")
                return render(request, 'app/fix.html', {'lang_list':lang_list, 'code':code, 'lang': lang})
            
            else:
                # OpenAI Key
                openai.api_key = "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"
                # Create Instance
                openai.Model.list()
                
                # Make request
                try:
                    api_response = openai.Completion.create(
                        engine = 'text-davinci-003',
                        prompt = f'Respond only with code. Fix this {lang} code: {code}',
                        temperature = 0,
                        max_tokens = 1000,
                        top_p = 1.0,
                        frequency_penalty = 0.0,
                        presence_penalty = 0.0,
                    )

                    # Parse the response
                    response = (api_response["choices"][0]["text"]).strip()

                    # save to db
                    record = Code(prompt = code, response=response, lang=lang, user=request.user)
                    record.save()  

                    return render(request, 'app/fix.html', {'lang_list':lang_list, 'response':response, 'lang': lang})

                except Exception as e:
                    return render(request, 'app/fix.html', {'lang_list':lang_list, 'response':e, 'lang': lang})

        return render(request, 'app/fix.html', {'lang_list':lang_list,'nbar':'fix'}) 
    
    else:
        messages.warning(request, "Please log in to use AI Coder.")
        return redirect('login')

def suggest(request):
    if request.user.is_authenticated:
        lang_list = ["html", "markup", "css", "clike", "javascript", "c", "csharp", "cpp", "dart", "django", "go", "java", "markup-templating", "matlab", "mongodb", "objectivec", "perl", "php", "powershell", "python", "r", "regex", "ruby", "rust", "sass", "scala", "sql", "swift", "typescript", "yaml" ]
        
        if request.method == "POST":
            code = request.POST['code']
            lang = request.POST['lang']

            if lang == "Select programming language":
                messages.warning(request, "You forget to pick a programming language.")
                return render(request, 'app/suggest.html', {'lang_list':lang_list, 'code':code, 'lang': lang})
            
            else:
                # OpenAI Key
                openai.api_key = "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"
                # Create Instance
                openai.Model.list()
                
                # Make request
                try:
                    api_response = openai.Completion.create(
                        engine = 'text-davinci-003',
                        prompt = f'Respond only with code. {code}',
                        temperature = 0,
                        max_tokens = 1000,
                        top_p = 1.0,
                        frequency_penalty = 0.0,
                        presence_penalty = 0.0,
                    )

                    # Parse the response
                    response = (api_response["choices"][0]["text"]).strip()

                    # save to db
                    record = Code(prompt = code, response=response, lang=lang, user=request.user)
                    record.save()  

                    return render(request, 'app/suggest.html', {'lang_list':lang_list, 'response':response, 'lang': lang})

                except Exception as e:
                    return render(request, 'app/suggest.html', {'lang_list':lang_list, 'response':e, 'lang': lang})

        return render(request, 'app/suggest.html', {'lang_list':lang_list, 'nbar':'suggest'})

    else:
        messages.warning(request, "Please log in to use AI Coder.")
        return redirect('login')     


def past_code(request):
    if request.user.is_authenticated:
        code = Code.objects.filter(user=request.user)
        return render(request, 'app/past.html', {'code':code, 'nbar':'past'})
    else:
        messages.warning(request, 'Please log in to use AI Coder.')
        return redirect('login')

def delete_past_code(request, id):
    if request.user.is_authenticated:
        past = Code.objects.get(id=id)
        past.delete()
        messages.success(request, 'Deleted successfully.')
        return redirect('past')
    else:
        messages.warning(request, 'Please log in to use AI Coder.')
        return redirect('login')

def signup(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = SignUpForm(request.POST)

            if form.is_valid():
                form.save()
                messages.success(request, 'Account created successfully.')
                return redirect('login')
        else:
            form = SignUpForm()
        return render(request, 'app/signup.html', {'form':form, 'nbar':'signup'})
    
    else:
        messages.warning(request, "You are already logged in.")
        return redirect('fix')

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request=request, data=request.POST)

            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']

                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Your account has been logged in.')
                    return redirect('fix')
                else:
                    messages.warning(request, 'Login error! Please try again.')
                    return redirect('login')
        else:
            form = LoginForm()
        return render(request, 'app/login.html', {'form':form, 'nbar':'login'})
    
    else:
        messages.warning(request, "You are already logged in.")
        return redirect('fix')    

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.warning(request, 'You have successfully logged out.')
        return redirect('home')
    else:
        messages.warning(request, 'Please log in.')
        return redirect('login')

