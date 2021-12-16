from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.files.uploadedfile import InMemoryUploadedFile

from ads.models import Ad, Comment, Fav
from ads.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from ads.forms import CreateForm, CommentForm
from ads.utils import dump_queries

from django.db.models import Q
from django.contrib.humanize.templatetags.humanize import naturaltime



class solo(LoginRequiredMixin, View):
    template_name = 'solo/solo.html'
    success_url = reverse_lazy('solo:all')

    def get(self, request):

        res = request.session.get('solo_d',False)
        if( res) : del(request.session['solo_d'])
        ctx = {'solo_d': res}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):

        msg1 = request.POST.get('field1')
        msg2 = request.POST.get('field2')

        result = str(msg1) + ' ' + str(msg2)
        result = result.strip()
        result = result[::-1]
        result = result.casefold()

        request.session['solo_d'] = result
        #ctx = {'solo_d': result}
        #return render(request, self.template_name, ctx)
        return redirect(request.path)
        #return redirect(self.success_url)
