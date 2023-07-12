# api/urls.py

from django.urls import path
from api import views
from users import views as user_views
from core import views as core_views
from customers import views as customer_views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = format_suffix_patterns([

    path('', views.api_root),

    # Authentication
    path(
        'login/',
        TokenObtainPairView.as_view(),
        name='token-obtain'),
    path(
        'logout/',
        views.TokenBlacklistView.as_view(),
        name='token-invalidate'),
    path('logout_all/', views.TokenInvalidateAllView.as_view(),
         name='token-invalidate-all'),

    # Customers
    path(
        'customers/',
        customer_views.CustomerList.as_view(),
        name='customer-list'),
    path('customers/<uuid:pk>/',
         customer_views.CustomerDetail.as_view(), name='customer-detail'),
    path('customers/<uuid:pk>/fields',
         customer_views.CustomerFieldList.as_view(), name='customer-fields'),
    path('customers/<uuid:pk>/fields/visibility',
         customer_views.CustomerFieldListVisibilitySetting.as_view(), name='customer-fields-visibility'),

    # Users
    path('users/', user_views.UserList.as_view(), name='user-list'),
    path('users/me', user_views.UserRequestDetails.as_view(),
         name='user-request'),
    path('users/<uuid:pk>/', user_views.UserDetail.as_view(),
         name='user-detail'),
    path('users/<uuid:pk>/changepassword',
         user_views.UserChangePassword.as_view(), name='user-changepassword'),
    path('users/<uuid:pk>/fields',
         user_views.UserFieldList.as_view(), name='user-fields'),
    path('users/<uuid:pk>/fields/<int:fieldpk>',
         user_views.UserFieldDetail.as_view(), name='user-field-detail'),
    path('users/<uuid:pk>/fields/visibility',
         user_views.UserFieldListVisibilitySetting.as_view(), name='user-fields-visibility'),

    # Fields
    path('fields/metadata/',
         core_views.FieldMetadataList.as_view(),
         name='fieldmeta-list'),
    path('fields/metadata/<int:fieldpk>/',
         core_views.FieldMetadataDetail.as_view(),
         name='fieldmeta-detail'),
    path('fields/metadata/reorder/',
         core_views.FieldMetadataReorder.as_view(),
         name='fieldmeta-reorder'),
    path('fields/fieldtypes/', core_views.FieldTypeList.as_view(),
         name='fieldtypes-list'),

    # Company Site
    path('companysites/',
         core_views.CompanySiteList.as_view(),
         name='companysite-list'),
    path('companysites/<int:pk>',
         core_views.CompanySiteDetail.as_view(),
         name='companysite-detail'),
])
