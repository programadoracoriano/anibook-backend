from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views
from api.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/user/', SignupAPI, name="signup"),
    path('login/user/', LoginAPI, name="signin"),
    path('login/guard/', LoginGuardAPI, name="loginguard"),
    path('get/default/avatar/', DefaulAvatarAPI, name="defaultavatar"),
    path('logout/', LogoutAPI, name="logout"),

    #profile urls
    path('get/user/profile/', UserDetailsAPI, name="userdetails"),
    path('get/user/profile/extra/', UserExtraDetailsAPI, name="userextradetails"),
    path('get/profile/', ProfileAPI, name="getprofile"),
    path('get/user/data/', UserDataAPI, name="getuserdata"),
    path('change/user/email/', EmailChangeAPI, name="emailchange"),
    path('upload/profile/image/', UploadUserImageAPI, name="uploaduserimage"),

    #followers urls
    path('get/follower/', FollowerAPI, name="followers"),
    path('detect/follower/', DetectFollowerAPI, name="detectfollower"),
    path('list/followers/', ListFollowersAPI, name="listfollower"),
    path('list/following/', ListFollowingAPI, name="listfollowing"),
    path('updates/followers/anime/list/', GetFollowerUpdatesAPI, name="followerslistupdates"),

    #reviews and topics urls
    path('get/reviews/', AnimeReviewAPI, name="animereview"),
    path('get/all/reviews/', getAllReviewsAPI, name="getallreviews"),
    path('show/review/', getReviewAPI, name="showreview"),
    path('get/my/review/', getMyReviewAPI, name="getmyreview"),
    path('get/my/reviews/', MyReviewsAPI, name="getmyreviews"),

    #collect points
    path('user/collectpoint/', collectPointsAPI, name="collectpoint"),

    #delete section
    path('delete/review/', deleteReviewAPI, name="getmyreviews"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
