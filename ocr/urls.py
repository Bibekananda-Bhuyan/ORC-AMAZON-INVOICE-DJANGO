from django.urls import path,include
from . import views
urlpatterns = \
    [

    path('upload-invoice',views.index,name="Index Page"),
    path('track-invoice',views.trackinvoice,name="Track Invoice"),
    path('update-invoice/<int:id>',views.updateinvoice,name="Update Invoice"),
    path('delete-invoice/<int:id>',views.deleteinvoice,name="Update Invoice"),

    ]