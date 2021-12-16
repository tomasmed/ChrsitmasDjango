from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.uploadedfile import InMemoryUploadedFile

from gifts.models import Gift, Member
from ads.models import Comment, Fav
from gifts.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from gifts.forms import CreateForm, CommentForm, SignUpForm
from gifts.utils import dump_queries, get_link_info
from bs4 import BeautifulSoup
import requests
import base64


from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from django.db.models import Q
from django.contrib.humanize.templatetags.humanize import naturaltime

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.member.birth_date = form.cleaned_data.get('birth_date')
            user.member.name = form.cleaned_data.get('name')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'gifts/signup.html', {'form': form})



class MemberListView(View):
    def get(self, request):
        ml = Member.objects.all()
        ctx = {'member_list': ml}
        return render(request, 'gifts/member_list.html', ctx)


class MemberCreate(OwnerCreateView):
    model = Member
    fields = '__all__'
    success_url = reverse_lazy('gifts:all')

class MemberUpdate(OwnerUpdateView):
    model = Member
    fields = '__all__'
    success_url = reverse_lazy('gifts:all')


class MemberDelete(OwnerDeleteView):
    model = Member
    fields = '__all__'
    success_url = reverse_lazy('gifts:all')


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        f = get_object_or_404(Gift, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, gift=f)
        comment.save()
        return redirect(reverse('gifts:gift_detail', args=[pk]))

class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "gifts/gift_comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        gift = self.object.gift
        return reverse('gifts:gift_detail', args=[gift.id])

class GiftListView(OwnerListView):
    model = Gift
    # By convention:
    template_name = "gifts/gift_list.html"

    def get(self, request) :
        strval = request.GET.get("search", False)
        if strval:
            query = Q(title__icontains=strval)
            query.add(Q(text__icontains=strval), Q.OR)
            gift_list = Gift.objects.filter(query).select_related().order_by('-updated_at')[:10]
        else:
            gift_list = Gift.objects.all()

        favorites = list()
        if request.user.is_authenticated:
            # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
            rows = request.user.favorite_gifts.values('id')
            # favorites = [2, 4, ...] using list comprehension
            favorites = [ row['id'] for row in rows ]

        # Augment the post_list
        for obj in gift_list:
            obj.natural_updated = naturaltime(obj.updated_at)


        ctx = {'gift_list' : gift_list, 'favorites': favorites, 'search': strval}
        return render(request, self.template_name, ctx)


class MemberGiftListView(OwnerListView):
    model = Member
    # By convention:
    template_name = "gifts/member_gift_list.html"

    def get(self, request,pk) :
        m = Member.objects.get(id=pk)
        strval = request.GET.get("search", False)
        if strval:
            query = Q(title__icontains=strval)
            query.add(Q(text__icontains=strval), Q.OR)
            gift_list = Gift.objects.filter(owner_id= pk).filter(query).select_related().order_by('-updated_at')[:10]
        else:
            gift_list = Gift.objects.filter(owner_id = pk)


        # Augment the post_list
        for obj in gift_list:
            obj.natural_updated = naturaltime(obj.updated_at)


        ctx = {'gift_list' : gift_list, 'search': strval, 'member':m}
        return render(request, self.template_name, ctx)




class GiftDetailView(OwnerDetailView):
    model = Gift
    template_name = "gifts/gift_detail.html"

    def get(self, request, pk) :
        x = Gift.objects.get(id=pk)
        comments = Comment.objects.filter(gift=x).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'gift' : x, 'comments': comments, 'comment_form': comment_form}
        return render(request, self.template_name, context)


class GiftCreateView(OwnerCreateView):
#    model = Gift
#    fields = ['title', 'price','text']
    template_name = 'gifts/gift_form.html'
    success_url = reverse_lazy('gifts:all')

    def get(self, request, pk=None):
        form = CreateForm()

        # https://django-taggit.readthedocs.io/en/latest/forms.html#commit-false
        #form.save_m2m()    # Giftd this
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)

        # https://django-taggit.readthedocs.io/en/latest/forms.html#commit-false
        #form.save_m2m()    # Giftd this
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        # Giftd owner to the model before saving

        gift = form.save(commit=False)
        gift.owner = Member.objects.get(user = self.request.user)
        gift.save()
        form.save_m2m()
        return redirect(self.success_url)

class GiftCreateFromLinkView(OwnerCreateView):
    template_name = 'gifts/gift_form_link.html'
    success_url = reverse_lazy('gifts:all')

    def get(self, request):

        res = request.session.get('linkgen','')
        res_title = request.session.get('bs_title', 'Enter a Title')
        res_text = request.session.get('bs_text', 'Enter a Description')
        res_price = request.session.get('bs_price',0)
        res_img = request.session.get('picture', None)

        data_dict = {'title': res_title, 'text': res_text, 'link': res, 'price':res_price, 'picture':res_img}
        form = CreateForm(initial= data_dict)
        ctx = {'form': form , 'linkgen': res}

        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        if 'linksubmit' in request.POST:

            link_add = request.POST.get('linkgen')

            req = requests.get(link_add)
            bs = BeautifulSoup(req.text, 'html.parser')

            bs_html_title = bs.find(id="vi-lkhdr-itmTitl")
            bs_title = bs_html_title.text

            bs_html_desc = bs.find(class_="topItmCndDscMsg")
            if bs_html_desc == None :
                bs_desc = bs_title
            else:
                bs_desc = bs_html_desc.text

            bs_html_price = bs.find(id="prcIsum")
            bs_price = bs_html_price.text[4:]

            bs_img = bs.find(id="icImg")
            bs_img_dat = base64.b64encode(requests.get(bs_img['src']).content)

            data_dict = {'title': bs_title, 'text': bs_desc, 'link': link_add, 'price':bs_price, 'picture':bs_img_dat}
            form = CreateForm(initial= data_dict)

            ctx ={'bs_title' : bs_title, 'bs_text' : bs_desc, 'bs_price' : bs_price, 'linkgen':link_add, 'form':form, 'picture':bs_img_dat }
            return render(request, self.template_name, ctx)

        elif 'savesubmit' in request.POST:
            form = CreateForm(request.POST, request.FILES or None)
            # https://django-taggit.readthedocs.io/en/latest/forms.html#commit-false
            #form.save_m2m()    # Giftd this
            if not form.is_valid():
                ctx = {'form': form}
                return render(request, self.template_name, ctx)
            # Add owner to the model before saving
            gift = form.save(commit=False)
            gift.owner = Member.objects.get(user = self.request.user)
            gift.save()
            form.save_m2m()
            return redirect(self.success_url)





class GiftUpdateView(OwnerUpdateView):
#    model = Gift
#    fields = ['title', 'price','text']
    template_name = 'gifts/gift_form.html'
    success_url = reverse_lazy('gifts:all')

    def get(self, request, pk):
        gift = get_object_or_404(Gift, id=pk, owner= Member.objects.get(user = self.request.user))
        form = CreateForm(instance=gift)

        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        gift = get_object_or_404(Gift, id=pk, owner=Member.objects.get(user = self.request.user))
        form = CreateForm(request.POST, request.FILES or None, instance=gift)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        gift = form.save(commit=False)
        gift.save()
        form.save_m2m()

        return redirect(self.success_url)

class GiftDeleteView(OwnerDeleteView):
    model = Gift



def stream_file(request, pk):
    gift = get_object_or_404(Gift, id=pk)
    response = HttpResponse()
    response['Content-Type'] = gift.content_type
    response['Content-Length'] = len(gift.picture)
    response.write(gift.picture)
    return response


# csrf exemption in class based views
# https://stackoverflow.com/questions/16458166/how-to-disable-djangos-csrf-validation
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Giftd PK",pk)
        t = get_object_or_404(Gift, id=pk)
        fav = Fav(user=Member.objects.get(user = Member.objects.get(user = self.request.user)), gift=t)
        try:
            fav.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Delete PK",pk)
        t = get_object_or_404(Gift, id=pk)
        try:
            fav = Fav.objects.get(user=Member.objects.get(user = Member.objects.get(user = self.request.user)), gift=t).delete()
        except Fav.DoesNotExist as e:
            pass

        return HttpResponse()


def ReportJsonData(request):
    data = list(Gift.objects.values())
    return JsonResponse(data,safe = False)