from rest_framework.routers import DefaultRouter

from core.views import ImageViewSet

app_name = "core"

router = DefaultRouter()
router.register("images", ImageViewSet, "images")
router.register("images", ImageViewSet, "images")
router.register("images", ImageViewSet, "images")
router.register("images", ImageViewSet, "images")
router.register("images", ImageViewSet, "images")
router.register("images", ImageViewSet, "images")
router.register("images", ImageViewSet, "images")
router.register("images", ImageViewSet, "images")


urlpatterns = router.urls
