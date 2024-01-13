# myapp/urls.py
from rest_framework import routers
from .views import InvoiceViewSet, InvoiceDetailViewSet

router = routers.DefaultRouter()
router.register(r'invoices', InvoiceViewSet)
router.register(r'invoice-details', InvoiceDetailViewSet)

urlpatterns = router.urls
