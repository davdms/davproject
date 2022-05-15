from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import QuoteListView, QuoteDetailView, AuthorsListView, QuoteUpdateView, MyQuotesListView, QuoteDeleteView, \
    QuoteHistoryListView
from . import views

app_name = 'quotes'

urlpatterns = [
    path('quotes/', login_required(QuoteListView.as_view()), name='quotes_list'),
    path('<int:pk>/detail/', login_required(QuoteDetailView.as_view()), name='quote_detail'),
    path('tag/<str:tagname>/', login_required(views.TagListView), name='tag_quotes_list'),
    path('quotes/create/', login_required(views.quotecreate), name='quote_create'),
    path('authors/', login_required(AuthorsListView.as_view()), name='authors_list'),
    path('profile/myquotes/', login_required(MyQuotesListView.as_view()), name='myquotes_list'),
    path('quotes/<int:pk>/update/', login_required(QuoteUpdateView.as_view()), name='quote_update'),
    path('quotes/<int:pk>/delete/', login_required(QuoteDeleteView.as_view()), name='quote_delete'),
    path('quotes/<int:quoteid>/history/', login_required(QuoteHistoryListView.as_view()), name='quote_history'),
    #ete chenq ogtagorcum django rest framework@
    # path('quotes_list_api', ApiQuotesListView.as_view(), name='quotes_list_api'),
]