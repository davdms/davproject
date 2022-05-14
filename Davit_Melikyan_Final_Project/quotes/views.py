from django.core.paginator import Paginator
from django.db import connections
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView, DeleteView
from .models import Quotes, Authors, QuotesToTags, Tags, QuotesHistory
from .forms import QuoteSearchForm, AuthorSearchForm, MyPageQuoteSearchForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


class QuoteDetailView(DetailView):
    model = Quotes


def showinfo(author='', quote=''):
    cursor = connections["default"].cursor()
    cursor.execute(f"""SELECT quotes.id, quotes.quote, quotes.created_at, authors.name
                    from quotes
                    left join authors on quotes.author_id = authors.id
                    where upper(authors.name) like upper('%{author}%')
                    and upper(quotes.quote) LIKE upper('%{quote}%')
                    order by quotes.created_at desc
                    """)
    answer = cursor.fetchall()
    return answer


def showquotesbytag(tagname):
    cursor = connections["default"].cursor()
    cursor.execute(f"""SELECT quotes.id, quotes.quote, quotes.created_at, 
                    authors.name, tags.id
                    from quotes
                    left join authors on quotes.author_id = authors.id
                    left join quotes_to_tags on quotes.id = quotes_to_tags.quote_id
                    inner join tags on quotes_to_tags.tag_id = tags.id
                    where tags.name='{tagname}'
                    order by quotes.created_at desc
                    """)
    answer = cursor.fetchall()
    return answer


def showuserquotes(userid, quote):
    cursor = connections["default"].cursor()
    cursor.execute(f"""SELECT quotes.id, quotes.quote, quotes.created_at, 
                    authors.name, tags.id
                    from quotes
                    left join authors on quotes.author_id = authors.id
                    left join quotes_to_tags on quotes.id = quotes_to_tags.quote_id
                    left join tags on quotes_to_tags.tag_id = tags.id
                    where authors.user_id={userid}
                    and upper(quotes.quote) LIKE upper('%{quote}%')
                    order by quotes.created_at desc
                    """)
    answer = cursor.fetchall()
    return answer


def authorsinfo(author=''):
    cursor = connections["default"].cursor()
    cursor.execute(f"""select authors.id, authors.name, authors.image, authors.user_id, count(quotes.id) 
                from authors
                left join quotes on quotes.author_id = authors.id
                where upper(authors.name) like upper('%{author}%')
                group by authors.id, authors.name, authors.image, authors.user_id
                order by count(quotes.id) desc
    """)
    answer = cursor.fetchall()
    return answer


def gettags(quotelist):
    cursor = connections["default"].cursor()
    alltags = []
    for q in quotelist:
        tags = {}
        tags['quoteid'] = q[0]
        cursor.execute(f"""SELECT tags.id, tags.name
        from quotes
        left join quotes_to_tags on quotes.id = quotes_to_tags.quote_id
        left join tags on quotes_to_tags.tag_id = tags.id
        where quotes.id = {q[0]}""")
        answer = cursor.fetchall()
        tagslist = []
        if len(answer) != 0:
            for q in answer:
                tagslist.append(q[1])
        tags['tags'] = tagslist
        alltags.append(tags)

    return alltags


class QuoteListView(ListView):
    model = Quotes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = QuoteSearchForm(self.request.GET)
        quotename = ''
        authorname = ''
        if form.is_valid():
            quote = form.cleaned_data['quote']
            author = form.cleaned_data['author']

            if quote:
                quotename = quote

            if author:
                authorname = author

        info = showinfo(authorname, quotename)
        # tag = QuotesToTags.objects.filter(quote_id=501)


        paginator = Paginator(info, 10)  # Show 10 contacts per page.

        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        tags = gettags(info)

        context = {
            'search_form': QuoteSearchForm(self.request.GET),
            'page_obj': page_obj,
            'tags': tags
        }
        return context


def TagListView(request, tagname):
    info = showquotesbytag(tagname)

    paginator = Paginator(info, 10)  # Show 10 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    tags = gettags(info)

    context = {
        'tagname': tagname,
        'page_obj': page_obj,
        'tags': tags
    }
    return render(request, "quotes/tag_quotes_list.html", context)


class QuoteMixin:
    model = Quotes
    fields = '__all__'
    success_url = reverse_lazy('quotes:quotes_list')


@login_required
def quotecreate(request):
    alltags = Tags.objects.order_by('name').values('pk', 'name')
    if request.method == 'POST':
        myform = request.POST
        quote = request.POST.get('quote')
        tags = request.POST.get('tags')

        context = {'form': myform, 'tags': alltags}

        if not quote or not tags:
            messages.error(request, "All fields are required.")
            return render(request, "quotes/quote_create.html", context=context)

        account = request.user
        userfullname = f'{account.first_name} {account.last_name}'
        quoteauthor = Authors.objects.filter(user_id=account.id).values('pk')

        if not quoteauthor:
            newauthor = Authors.objects.create(user_id=account.id, name=userfullname)
            newauthor.save()

        quoteauthor = Authors.objects.filter(user_id=account.id).values('pk')
        quoteauthorid = quoteauthor[0]['pk']

        newquote = Quotes.objects.create(quote=quote, author_id=quoteauthorid)
        newquote.save()

        newtag = QuotesToTags.objects.create(quote_id=newquote.id, tag_id=tags)
        newtag.save()

        messages.info(request, f"Your quote is added.")
        return redirect("quotes:myquotes_list")

    context = {'tags': alltags}
    return render(request, "quotes/quote_create.html", context=context)


class AuthorsListView(ListView):
    model = Authors

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = AuthorSearchForm(self.request.GET)
        authorname = ''
        if form.is_valid():
            author = form.cleaned_data['author']

            if author:
                authorname = author

        info = authorsinfo(authorname)

        paginator = Paginator(info, 10)  # Show 10 contacts per page.

        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'search_form': AuthorSearchForm(self.request.GET),
            'page_obj': page_obj,
        }
        return context


class MyQuotesListView(ListView):
    model = Quotes
    template_name = "quotes/myquotes_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = MyPageQuoteSearchForm(self.request.GET)
        quotename = ''
        if form.is_valid():
            quote = form.cleaned_data['quote']

            if quote:
                quotename = quote

        account = self.request.user
        info = showuserquotes(account.id, quotename)

        quoteshistory = QuotesHistory.objects.filter(quote=info[0][0]).values('quote', 'quote_text', 'change_date')

        paginator = Paginator(info, 10)  # Show 10 contacts per page.

        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        tags = gettags(info)

        context = {
            'search_form': MyPageQuoteSearchForm(self.request.GET),
            'page_obj': page_obj,
            'quoteshistory': quoteshistory,
            'tags': tags
        }
        return context


# def quote_history_list(request, quoteid):
#     model = QuotesHistory
#
#     quotehistory = QuotesHistory.objects.filter(quote=quoteid, user_id=request.user.pk).order_by("change_date")
#
#     print('info-', quotehistory)
#     paginator = Paginator(quotehistory, 10)  # Show 10 contacts per page.
#
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#
#     context = {
#         'page_obj': page_obj,
#         'quotehistory': quotehistory
#     }
#     return render(request, "quotes/quote_history.html", context)


class QuoteHistoryListView(ListView):
    model = QuotesHistory
    paginate_by = 10
    template_name = "quotes/quote_history.html"

    def get_context_data(self, **kwargs):
            context = super(QuoteHistoryListView, self).get_context_data(**kwargs)
            quoteid = self.kwargs.get('quoteid')
            account = self.request.user
            #ebr dnum enq <-> darnum e asc
            quoteshistory = QuotesHistory.objects.filter(quote=quoteid, user_id=account.id).order_by('-change_date')

            paginator = Paginator(quoteshistory, 10)  # Show 10 contacts per page.

            page_number = self.request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {
                'page_obj': page_obj,
                'quoteshistory': quoteshistory,
            }
            return context


class QuoteUpdateView(UpdateView):
    model = Quotes
    fields = ('quote', )
    template_name = "quotes/quote_update.html"
    success_url = reverse_lazy('quotes:myquotes_list')

    def form_valid(self, form):
        formquote = form.cleaned_data['quote']
        if not formquote:
            messages.error(self.request, "Quote is required.")
            context = {'form': form}
            return render(self.request, "quotes/quote_update.html", context=context)

        quote = self.get_object()
        if quote.quote == formquote:
            messages.error(self.request, "Sorry, but this is the same quote !!!")
            context = {'form': form}
            return render(self.request, "quotes/quote_update.html", context=context)

        messages.success(self.request, f"Your info was successfully updated !!!")
        context = {'form': form}
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        quote = super(QuoteUpdateView, self).get_object()
        account = self.request.user
        quotehistory = QuotesHistory.objects.create(quote=quote.id,
                                                    user_id=account.id,
                                                    quote_text=quote.quote)
        quotehistory.save()
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        account = self.request.user
        # quoteauthor = Authors.objects.filter(user_id=account.id).values('pk')
        # quoteauthorid = quoteauthor[0]['pk']
        # return Quotes.objects.filter(author_id=quoteauthorid)
        return Quotes.objects.filter(author__user__id=account.id)


class QuoteDeleteView(DeleteView):
    model = Quotes
    fields = '__all__'
    template_name = "quotes/quote_confirm_delete.html"
    success_url = reverse_lazy('quotes:myquotes_list')

    def form_valid(self, form):
        self.object.is_deleted = True
        self.object.save()

    def post(self, request, *args, **kwargs):
        quote = super(QuoteDeleteView, self).get_object()
        account = self.request.user
        quotehistory = QuotesHistory.objects.create(quote=quote.id,
                                                    user_id=account.id,
                                                    quote_text=quote.quote)
        quotehistory.save()
        return self.delete(request, *args, **kwargs)

    def get_queryset(self):
        account = self.request.user
        quoteauthor = Authors.objects.filter(user_id=account.id).values('pk')
        quoteauthorid = quoteauthor[0]['pk']
        return Quotes.objects.filter(author_id=quoteauthorid)

#Kam petqa ogtagorcenq django rest framework@
# @method_decorator(csrf_exempt, name='dispatch')
# class ApiQuotesListView(View):
#     def get(self, request):
#         # Version 1
#         quotes = Quotes.objects.values('id', 'quote', 'created_at')
#
#         # Version 2
#         # quotes = []
#         # for quote in Quotes.objects.all():
#         #     quotes.append({
#         #         'id': quote.id,
#         #         'quote_text': quote.quote,
#         #         'created_at': quote.created_at
#         #     })
#
#         # Return
#         data = {
#             'quotes': list(quotes)
#         }
#         return JsonResponse(data)
#
#     # IF need post request
#     # def post(self, request):
#     #     post_data = request.body.decode('utf-8')
#     #     post_data = json.load(post_data)
#     #     ...
