from api.urls.listsurls import urlpatterns as list_urls
from api.urls.userurls import urlpatterns as user_urls
from api.urls.searchurls import urlpatterns as search_urls

urlpatterns = list_urls
urlpatterns += user_urls
urlpatterns += search_urls


