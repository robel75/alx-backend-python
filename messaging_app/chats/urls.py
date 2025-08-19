from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet

router = routers.DefaultRouter()
router.register('conversations', ConversationViewSet, basename='conversation')
nested_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
nested_router.register('messages', MessageViewSet, basename='conversation-message')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(nested_router.urls))
]
