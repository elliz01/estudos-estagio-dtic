from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question


# VIEW: lista das perguntas (usando class-based view)
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        # Retorna as 5 perguntas mais recentes
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
        :5
    ]


# VIEW: detalhe da pergunta
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


# VIEW: resultados da pergunta
class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


# VIEW: processa o voto (continua como função)
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        # pega a escolha enviada pelo formulário
        selected_choice = question.choice_set.get(pk=request.POST["choice"])

    except (KeyError, Choice.DoesNotExist):
        # erro: usuário não escolheu nada
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "You didn't select a choice.",
        })

    else:
        # incrementa o voto (forma segura)
        selected_choice.votes = F("votes") + 1
        selected_choice.save()

        # redireciona para resultados
        return HttpResponseRedirect(
            reverse("polls:results", args=(question.id,))
        )