import datetime
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404
from forms import FormPagamento
from django.utils.translation import ugettext as _
from django.core.paginator import Paginator
from django.contrib import messages
from forms import FormRegistro
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required

from models import ContaPagar, ContaReceber, CONTA_STATUS_APAGAR

@login_required
def contas(request):
    contas_a_pagar = ContaPagar.objects.filter(
        status=CONTA_STATUS_APAGAR, usuario=request.user,
    )
    contas_a_receber = ContaReceber.objects.filter(
        status=CONTA_STATUS_APAGAR, usuario=request.user,
    )

    return render_to_response(
        'contas/contas.html',
        locals(),
        context_instance=RequestContext(request),
    )

@login_required
def conta(request, conta_id, classe):
    conta = get_object_or_404(classe, id=conta_id)

    if conta.usuario != request.user:
        raise Http404

    form_pagamento = FormPagamento()
    return render_to_response(
        'contas/conta.html',
        locals(),
        context_instance=RequestContext(request),
    )

@login_required
def conta_pagamento(request, conta_id, classe):
    conta = get_object_or_404(classe, id=conta_id)

    if conta.usuario != request.user:
        raise Http404

    if request.method == 'POST':
        form_pagamento = FormPagamento(request.POST)

        if form_pagamento.is_valid():
            form_pagamento.salvar_pagamento(conta)

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def contas_por_classe(request, classe, titulo):
    contas = classe.objects.filter(usuario=request.user).order_by('status','data_vencimento')

    paginacao = Paginator(contas, 5)
    pagina = paginacao.page(request.GET.get('pagina', 1))

    titulo = _(titulo)

    return render_to_response(
        'contas/contas_por_classe.html',
        locals(),
        context_instance=RequestContext(request),
    )

@login_required
def editar_conta(request, classe_form, titulo, conta_id=None):

    if conta_id:
        conta = get_object_or_404(classe_form._meta.model, id=conta_id)

        if conta.usuario != request.user:
            raise Http404

    else:
        conta = None

    if request.method == 'POST':
        form = classe_form(request.POST, instance=conta)

        if form.is_valid():
            conta = form.save(commit=False)
            conta.usuario = request.user
            conta.save()

            return HttpResponseRedirect(conta.get_absolute_url())
    else:
        form = classe_form(initial={'data_vencimento': datetime.date.today()},
        instance=conta,
        )

    return render_to_response(
        'contas/editar_conta.html',
        locals(),
        context_instance=RequestContext(request)
    )

@login_required
def excluir_conta(request, classe, conta_id, proxima='/contas/'):
    conta = get_object_or_404(classe, id=conta_id)
    if conta.usuario != request.user:
        raise Http404

    conta.delete()

    #request.user.message_set.create(message='Conta excluida com sucesso!')
    messages.add_message(request, messages.INFO, 'Conta excluida com sucesso!')

    return HttpResponseRedirect(proxima)

def registrar(request):
    if request.method == 'POST':
        form = FormRegistro(request.POST)

        if form.is_valid():
            novo_usuario = form.save()
            return HttpResponseRedirect('/')
    else:
        form = FormRegistro()

    return render_to_response(
        'registrar.html',
        locals(),
        context_instance=RequestContext(request),
    )

@permission_required('ver_todos_os_usuarios')
def todos_os_usuarios(request):
    usuarios = User.objects.all()
    render_to_response(
        'todos_os_usuarios.html'
        ,locals()
        ,context_instance=RequestContext(request)
    )