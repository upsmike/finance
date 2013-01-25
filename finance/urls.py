from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from contas.views import registrar
import contas.views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', include('contas.urls')),
    # url(r'^finance/', include('finance.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^entrar/$', 'django.contrib.auth.views.login', {'template_name': 'entrar.html'}, 'entrar'),
    (r'^sair/$', 'django.contrib.auth.views.logout', {'template_name': 'sair.html'}, 'sair'),
    (r'^registrar/$', 'contas.views.registrar', {}, 'registrar'),
    (r'^todos_os_usuarios/$', 'contas.views.todos_os_usuarios', {}, 'todos_os_usuarios'),
    (r'^mudar_senha/$', 'django.contrib.auth.views.password_change',
     {'template_name': 'mudar_senha.html'}, 'mudar_senha'),
    (r'^mudar_senha/concluido/$', 'django.contrib.auth.views.password_change_done',
     {'template_name': 'mudar_senha_concluido.html'}, 'mudar_senha_concluido'),
    url(r'^contas/', include('contas.urls')),
    url(r'^admin/', include(admin.site.urls)),
)