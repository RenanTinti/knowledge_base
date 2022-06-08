from django.conf import settings
from django.shortcuts import render, redirect, reverse
from .forms import SuggestionForm
from datetime import date, timedelta

from pathlib import Path


# Biblioteca para bloquear as páginas que apenas usuários logados poderão acessar. Na verdade, o bloqueio é feito nas views, que consequentemente bloqueia as páginas. O primeiro parâmetro das views deverá ser essa biblioteca, e o segundo parâmetro deverá ser a classe pai padrão do Django (como as ListViews, TemplateViews, etc). É necessário, no arquivo settings, definir qual a url da página de login e qual url o usuário será redirecionado depois de fazer o login.
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Comunicado, Ferramenta, Procedimento, Link, Suggestion, Documento, User

# Bibliotecas para manipular o acesso as páginas dos documentos que fazem download de arquivos (view ListaFerramentas)
from django.http import Http404, HttpResponse

# Biblioteca para realizar queries avançadas. No nosso caso, realizamos uma query filtrando informações de duas colunas diferentes da model Procedimentos (titulo e descricao)
from django.db.models import Q

# Biblioteca para manipular os diretórios
import os

# Bibliotecas necessárias para criação de views através de classes. O TemplateView é utilizado para páginas que não possuem context, como a loginpage.html. Já a ListView é utilizada para páginas que possuem context, principalmente se essa página possuir uma lista (no caso, existe a lista de comunicados). A DetailView é um tipo de view ideal para que sejam apresentadas todas as informações de um item de um model, ou seja, utilizaremos a DetailView para mostrar tudo o que estiver dentro de um único procedimento, em páginas diferenciadas pelo seu id.
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, CreateView

# Create your views here.

# Para criação de views para projetos simples, recomenda-se utilizar o Function based Views, exemplificado abaixo. Porém, para sites maiores, usamos o Class Based Views, que possui uma estrutura mais robusta e completa ao longo prazo.


# Class based views

class Loginpage(TemplateView):
    template_name = 'loginpage.html'

    def get(self, request, *args, **kwargs):

        # Se o usuário estiver logado, redireciona para a view Homepage. Não podemos apenas direcionar o usuário para um outro template, devemos direcioná-lo para uma outra view, pois a view Loginpage é uma TemplateView e a Homepage é uma ListView, e caso fosse feito o direcionado ao template (html), haveria perda de informações e a página não funcionaria. Além disso, a view Homepage ainda faz a verificação se o usuário está logado, através da LoginRequiredMixin. Também é necessário importar o redirect, ao lado do render
        if request.user.is_authenticated:
            return redirect('procedimento:home')
        # Caso contrário, direciona para a url padrão dessa view, que é a página de login
        else:
            return super().get(request, *args, **kwargs)


class Homepage(LoginRequiredMixin, CreateView):

    # Ao utilizar uma class based view, a lista (model) que antes era o context agora passa a se chamar object_list, sendo necessária realizar essa alteração no template da página. O que define o que é cada model é a classe passada a ele. Nesse caso, o model é a classe Comunicado.
    template_name = 'homepage.html'
    model = Suggestion
    form_class = SuggestionForm
    #fields = ('sugestao',)

    def get_context_data(self, *args, **kwargs):

        # super: significa que está pegando parametros da superclasse (a classe que está acima da ListView)
        context = super(Homepage, self).get_context_data(*args, **kwargs)

        # As variáveis devem ser inseridas entre a declaração do context e o retorno do context.

        comunicados = Comunicado.objects.order_by('-data_criacao')
        context['comunicados'] = comunicados

        curr_date = date.today()
        hoje = curr_date.strftime('%d/%m')
        hoje = str(hoje)
        context['hoje'] = hoje

        return context

    # Função para destacar na página administrativa qual usuário criou a sugestão
    def form_valid(self, form):
        form.instance.solicitante = self.request.user
        return super(Homepage, self).form_valid(form)

    '''def criar_sugestao(request, self, form):
        form = SuggestionForm(request.POST or None)

        if form.is_valid():
            object.solicitante = request.user
            self.object = form.save(commit=False)
                    
            return redirect('home')

        return render(request, 'home', {'form': form})'''

    def get_success_url(self):
        return reverse('procedimento:home')


class ListaProcedimentos(LoginRequiredMixin, ListView):
    template_name = 'procedimentos.html'
    model = Procedimento
    # object_list

    def get_context_data(self, **kwargs):

        # super: significa que está pegando parametros da superclasse (a classe que está acima da DetailView)
        context = super(ListaProcedimentos, self).get_context_data(**kwargs)

        # As variáveis devem ser inseridas entre a declaração do context e o retorno do context.
        # Filtrar a tabela de procedimentos e ordenar todos os procedimentos pelo grupo.

        procedimentos = self.model.objects.order_by('grupo')
        context['procedimentos'] = procedimentos

        mais_vistos = self.model.objects.order_by('-visualizacoes')[0:10]
        context['mais_vistos'] = mais_vistos

        return context


class PaginaProcedimento(LoginRequiredMixin, DetailView):
    template_name = 'pag_proc.html'
    model = Procedimento
    # object

    # IMPORTANTE: para passar outras variáveis da view para o template, é necessário utilizar o método get_context_data conforme abaixo.
    def get_context_data(self, **kwargs):

        # super: significa que está pegando parametros da superclasse (a classe que está acima da DetailView)
        context = super(PaginaProcedimento, self).get_context_data(**kwargs)

        # As variáveis devem ser inseridas entre a declaração do context e o retorno do context.
        # Filtrar a tabela de procedimentos e filtrar todos os procedimentos relacionados pelo grupo. A função get_object referencia o object atual do template, ou seja, o procedimento que está ativo (sendo exibido no site).
        relacionados = self.model.objects.filter(grupo=self.get_object().grupo)
        context['relacionados'] = relacionados

        return context

    # Método para contabilizar visualizações de um procedimento. O acesso a uma página é uma função get, que já está inserida dentro da super classe. Diante disso, vamos declarar esss método e editá-lo.
    def get(self, request, *args, **kwargs):
        # A função get_object identifica qual procedimento está sendo acessado
        procedimento = self.get_object()

        # Incrementa 1 ao número de visualizações
        procedimento.visualizacoes += 1

        # Salva a informação no banco de dados
        procedimento.save()

        # Redireciona o usuário para a url final
        return super().get(request, *args, **kwargs)


class ListaFerramentas(LoginRequiredMixin, ListView):
    template_name = 'ferramentas.html'
    model = Ferramenta

    # Deixando o nome dos objetos no template mais amigável. Ao invés de utilizar o object_list, podemos utilizar o nome definido abaixo
    context_object_name = 'ferramentas'

    # Método alternativo de ordenaçâo, sem precisar do get_context_data
    ordering = ['nome']

    # object_list

    def download(request, path):
        file_path = os.path.join(settings.MEDIA_ROOT, path)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(
                    fh.read(), content_type='application/arquivo')
                response['Content-Disposition'] = 'inline;filename=' + \
                    os.path.basename(file_path)
                return response

        raise Http404

    def get_context_data(self, **kwargs):
        context = super(ListaFerramentas, self).get_context_data(**kwargs)

        # As variáveis devem ser inseridas entre a declaração do context e o retorno do context.
        links = Link.objects.order_by('nome')
        context['links'] = links

        return context


class ListaDocumentos(LoginRequiredMixin, ListView):
    template_name = 'documentos.html'
    model = Documento

    def download(request, path):
        file_path = os.path.join(settings.MEDIA_ROOT, path)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(
                    fh.read(), content_type='application/arquivo')
                response['Content-Disposition'] = 'inline;filename=' + \
                    os.path.basename(file_path)
                return response

        raise Http404


class ListaComunicados(LoginRequiredMixin, ListView):
    template_name = 'comunicados.html'
    model = Comunicado
    context_object_name = 'comunicados'
    ordering = ['-data_criacao']
    paginate_by = 10


class Pesquisa(LoginRequiredMixin, ListView):
    template_name = 'pesquisa.html'
    model = Procedimento

    # Método da ListView que permite que seja feito o get da query (pesquisa)
    def get_queryset(self):

        # Pega o valor da query e insere dentro da variável "termo", passada através do método GET. O GET representa o método, já o get() é um método que permite pegarmos alguma informação, por isso que se repetem
        termo = self.request.GET.get('query')

        # Verifica se existe alguma informação no campo de pesquisa e faz o filtro dos procedimentos através dele. Caso não exista, não retorna nada ao usuário
        if termo:
            object_list = self.model.objects.filter(
                Q(titulo__icontains=termo) | Q(descricao__icontains=termo))
            return object_list.order_by('-visualizacoes')
        else:
            return None


class EditarPerfil(LoginRequiredMixin, UpdateView):
    template_name = 'perfil.html'
    model = User

    def get_success_url(self):
        return reverse('procedimento:perfil')
