from django.db import models
from django.contrib.auth import get_user_model

# Biblioteca para criar campos de texto editáveis. 
from ckeditor_uploader.fields import RichTextUploadingField

# Biblioteca necessária para que seja possível verificar quem criou um novo item. AbstractUser serve para criar os novos campos de um usuário, os que não são padrão do Django
from django.contrib.auth.models import User

# Biblioteca utilizada para definir data e horário de criação de dados na tabela (timezone.now)
from django.utils import timezone

# Create your models here.
# Criação dos procedimentos

# Lista de grupos de procedimentos. Os grupos precisam ser criados para existir uma relação entre as páginas. Cada grupo conterá uma determinada quantidade de páginas, entre explicações teóricas, procedimentos, utilização de ferramentas, etc. A primeira coluna corresponde à forma como as informações serão apresentadas ao bano de dados, já a segunda coluna representa a forma como as informações serão mostradas ao usuário (com nomes mais "friendly").
LISTA_GRUPOS = (
    ('Product01', 'Product01'),
    ('Product02', 'Product02'),
    ('Product03', 'Product03'),
    ('Other', 'Other'),
)

# Criação da classe dos procedimentos. O parâmetro models.Model é necessário, visto que a classe Procedimento é uma subclasse de models. Sempre que for criada uma nova tabela no banco de dados, é preciso fazer a migração utilizando os comandos "python manage.py makemigrations" e "python manage.py migrate". Vale lembrar que apenas é criada uma nova tabela no banco de dados, mas ainda não é possível visualizá-la na página de admin. Para visuzalizar as novas tabelas, deve-se importar o model dentro do arquivo admin.py.
class Procedimento(models.Model):
    titulo = models.CharField(max_length=100, default='')
    subtitulo = models.TextField(max_length=1000, default='')
    descricao = RichTextUploadingField(default='')
    grupo = models.CharField(max_length=50, choices=LISTA_GRUPOS)
    ativo = models.BooleanField(default=True)
    author = models.ForeignKey(User, default=get_user_model(), on_delete=models.PROTECT, related_name='author')
    visualizacoes = models.IntegerField(default=0)
    data_criacao = models.DateTimeField(default=timezone.now)
    data_atualizacao = models.DateTimeField(auto_now=True)

    # Comando para que o título do procedimento seja descrito a lista do banco de dados. Caso esse comando não seja feito, o procedimento aparecerá como "Procedimento (1)".
    def __str__(self):
        return self.titulo

class Comunicado(models.Model):
    titulo = models.CharField(max_length=100, default='')
    descricao = RichTextUploadingField(default='')
    grupo = models.CharField(max_length=50, choices=LISTA_GRUPOS)
    author = models.ForeignKey(User, default=get_user_model(), on_delete=models.PROTECT)
    data_criacao = models.DateTimeField(default=timezone.now)

    def date(self):
        return self.data_criacao.strftime('%d/%m')

    def __str__(self):
        return self.titulo

class Ferramenta(models.Model):
    nome = models.CharField(max_length=100, default='')
    descricao = RichTextUploadingField(default='')
    versao = models.CharField(max_length=20, default='')
    arquivo = models.FileField(upload_to='media/')
    ativo = models.BooleanField(default=True)
    author = models.ForeignKey(User, default=get_user_model(), on_delete=models.PROTECT)
    data_criacao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nome
    
class Link(models.Model):
    nome = models.CharField(max_length=100, default='')
    endereco = models.CharField(max_length=200, default='')
    author = models.ForeignKey(User, default=get_user_model(), on_delete=models.PROTECT)
    data_criacao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nome

class Suggestion(models.Model):
    sugestao = models.TextField(max_length=2000, default='')
    atendido = models.BooleanField(default=False)
    solicitante = models.ForeignKey(User, on_delete=models.PROTECT, blank=True)
    data_criacao = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'sugestões'

    def __str__(self):
        if self.atendido == True:
            self.atendido = 'Answered suggestion'
        else:
            self.atendido = 'Unanswered suggestion'
        return str(self.atendido)

DOCS_GRUPOS = (
    ('General Docs', 'General Docs'),
    ('Training', 'Training'),
    ('Manuals', 'Manuals'),
)
    
class Documento(models.Model):
    nome = models.CharField(max_length=100, default='')
    descricao = RichTextUploadingField(default='')
    arquivo = models.FileField(upload_to='media/')
    grupo = models.CharField(max_length=50, choices=DOCS_GRUPOS)
    author = models.ForeignKey(User, default=get_user_model(), on_delete=models.PROTECT)
    data_criacao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nome