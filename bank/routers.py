from bank.views import BankViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'bank', BankViewSet, basename='bank')
urlpatterns = router.urls
