# Para cada página criada, precisam ser criadas uma URL, uma view e um template. Nas URLs, caso o primeiro parâmetro do path seja vazio nos dois arquivos url.py (tanto o do projeto como o do procedimento), o segundo parâmetro será a homepage

from django.urls import path, reverse_lazy

# Importação da biblioteca que cria uma view padrão de login e logout. Recebe o apelido de auth_view, pois o nome views já é do arquivo views.py
from django.contrib.auth import views as auth_view

# Importação das classes/funções que estão dentro do arquivo views.py
from .views import ListaComunicados, ListaProcedimentos, Loginpage, Homepage, PaginaProcedimento, ListaFerramentas, ListaDocumentos, Pesquisa, EditarPerfil

from . import views

# Variável com o nome do aplicativo. É preciso passar essa variável como namespace no arquivo de urls do projeto para que o Django saiba a quais urls a função está se referindo. 
app_name = 'procedimento'

urlpatterns = [
    # homepage é uma função que foi definida dentro do arquivo views.py, caso seja uma function based view.
    # Homepage é a classe que foi definida dentro do arquivo views.py caso seja uma class based view. Caso seja, é preciso alterar o nome da função importada para o nome da classe e definir, no path, a classe como view, com a função as_view
    # O parâmetro "name" é responsável por referenciar qual página o link está se referindo quando trabalhamos com listas de links. É recomendado que se utilize o mesmo nome da página. Deve existir um app_name neste arquivo, que deve ser passado como parâmetro na função path desse app, presente no arquivo urls do projeto. 

    # A página de login recebe a classe padrão de login do Django
    path('', auth_view.LoginView.as_view(template_name='loginpage.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='logoutpage.html'), name='logout'),
    path('home/', Homepage.as_view(), name='home'),
    path('procedimentos/', ListaProcedimentos.as_view(), name='procedimentos'),
    path('ferramentas/', ListaFerramentas.as_view(), name='ferramentas'),
    path('documentos/', ListaDocumentos.as_view(), name='documentos'),
    path('comunicados/', ListaComunicados.as_view(), name='comunicados'),
    path('pesquisa/', Pesquisa.as_view(), name='pesquisa'),

    # Página para editar os dados do usuário. É passado o ID do usuário como parâmetro para que ele edite o próprio perfil.
    path('perfil/<int:pk>', auth_view.PasswordChangeView.as_view(template_name='perfil.html', success_url=reverse_lazy('procedimento:home')), name='perfil'),
    
    # A view DetailView espera que em sua url seja fornecido um parâmetro. Nesse caso, estamos passando um parâmetro do tipo inteiro chamado pk (primary key). A primary key é o id de um item do banco de dados (model)
    path('procedimentos/<int:pk>', PaginaProcedimento.as_view(), name='pag_proc'),
]