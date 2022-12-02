from django.shortcuts import render
from textblob import TextBlob
from bs4 import BeautifulSoup

# Create your views here.
def base(request):
    return render(request,'input.html')

def mispell(request):
    word=request.POST['word']
    text=BeautifulSoup(word, features='html.parser').text

    print(text)
    convert_word=TextBlob(text)
    corrected_word=convert_word.correct()
    return render(request,'result.html',{'result':corrected_word})

from django.http import HttpResponse
from django.shortcuts import render
# import torch
# from gramformer import Gramformer
def result(request):    
    gf_inference = torch.load(r'/content/sample_data/gf.pth')
    aa=str(request.GET['pclass'])
    influent_sentences = []
    op=[]
    op1=[]
    context={}
    influent_sentences.append(aa)  
    for influent_sentence in influent_sentences:
        corrected_sentence = gf_inference.correct(influent_sentence)
        print("[Input] ", influent_sentence)
        op.append(corrected_sentence[0])
        op1.append(influent_sentence)
        
        
        context['h']=influent_sentence
        context['o']=corrected_sentence[0]

        # {'a1':op},{'a2':aa}
    return render(request, 'result.html',context)

def documetation(request):
    return render(request,'documetation.html')


