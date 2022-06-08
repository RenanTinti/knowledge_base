"""knowledge_base URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve


# Para que uma página seja acessada primeiro (default), deve-se inserir apenas a barra no path
# Controla as urls do site inteiro
urlpatterns = [
    # Página de admin criada por padrão pelo Django
    path('admin/', admin.site.urls),

    # Inclusão do arquivo urls.py do app procedimento, junto com o namespace que recebe o mesmo nome do app, para que o Django saiba quais links se referenciar, caso existam mais de um app. O namespace não é um link, mas sim um conjunto de links.
    path('', include('procedimento.urls', namespace='procedimento')),

    # Inclusão da URL que gerenciará os Downloads do site
    re_path(r'^download/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),

    # Inclusão das URLs do ckeditor
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
]

# Definição de URL para os arquivos estáticos. Toda a documentação de como configurar essas etapas, bem como a importação de bibliotecas, está presente em https://docs.djangoproject.com/en/4.0/howto/static-files/
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Administration"
admin.site.site_title = "Administration"
admin.site.index_title = "Welcome to the Administrative Portal"