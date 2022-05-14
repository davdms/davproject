from django.urls import path, include
from rest_framework import routers
from .views import QuotesListViewset

router = routers.DefaultRouter()
router.register('quotes', QuotesListViewset)
#ete unenq mi qani view
# router.register('quotes-2', QuotesListViewset)
# router.register('quotes-3', QuotesListViewset)

app_name = 'quotes_api'
urlpatterns = [
    path('', include(router.urls))
]
