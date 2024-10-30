from django.http import Http404
from django.shortcuts import render
from .models import Question
from .forms import QuestionForm
from django.templatetags.static import static
from django.core.files.storage import FileSystemStorage
import traceback

from .pdfReader import ask_question, load_document

# Create your views here.
def index(request):

    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                saved_form = form.save()
                questions = Question.objects.all
                if request.FILES:
                    print(request.scheme)
                    load_document(request.scheme+"://"+request.get_host()+saved_form.file.url)
                results = ask_question(form.cleaned_data['question'])
                answer = results["answer"]
                return render(request, "index.html", {"questions": questions, "answer": answer, 'form':form, 'saved_form':saved_form})
            except:
                print(traceback.format_exc())
                return render(request, "index.html", {})
        else:
            print("Form is not valid.",form.errors)
    else:
        form = QuestionForm()
    return render(request, "index.html", {'form':form})