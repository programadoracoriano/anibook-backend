import base64
from django.core.files.base import ContentFile
from datetime import date
from django.core.mail import send_mail
from rest_framework.authentication import TokenAuthentication

from rest_framework.response import Response

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.views import APIView

from ..models import *
from ..serializers import *
from django.db.models import Avg, Sum, FloatField, F, Count, Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@api_view(['GET'])
@authentication_classes([])
def LoginGuardAPI(request):
    if request.method == 'GET':
        tk      = request.GET['tk']
        count_u = User.objects.filter(auth_token=tk).count()
        if count_u == 0:
            isLogged = False
        elif count_u > 0:
            isLogged = True
        return Response({"isLogged":isLogged})

@api_view(['POST'])
@authentication_classes([])
def SignupAPI(request):
    if request.method == 'POST':
        msg = {}
        username = request.data['username']
        email    = request.data['email']
        password = request.data['password']
        getUsers = User.objects.filter(username=username)
        getEmail = User.objects.filter(email=email)
        if getUsers.count() > 0:
            msg = {'msg':'User already exists!Please choose other username!', 'success':False}
        elif getEmail.count() > 0:
            msg = {'msg':'E-mail already exists!Please choose another e-mail!', 'success':False}
        elif ' ' in username == True:
            msg = {'msg': 'Your username cannot have spaces!', 'success': False}
        elif len(username) < 6 or len(username)> 20:
            msg = {'msg': 'Your username needs to be 6 to 20 characters.', 'success':False}
        elif len(password) < 8 or len(password)>16:
            msg = {'msg': 'Your passwords needs to be 8 to 16 characters.', 'success':False}
        else:
            qs = User.objects.create_user(username=username, email=email, password=password)
            msg = {'msg': 'User created successfully!', 'success':True}
        return Response(msg)


@api_view(['POST'])
@authentication_classes([])
def LoginAPI(request):            # <-- And here
    if request.method == 'POST':
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        content = {}
        if user is not None:
            token = Token.objects.get_or_create(user=user)
            print(token[0])

            content = {'token': str(token[0]), 'msg':'You have successfully logged!', 'success':True}
        else:
            content = {'msg':'Username or password are wrong!', 'success':False}
        return Response(content)

    elif request.method == 'POST':
        content = {}
        username = request.data['username']
        password = request.data['password']
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            User.objects.create_user(username=username, password=password)
            message = {"msg":"You have successfully Registered!"}
        else:
            message = {"msg": "Some error has occured"}
        return Response(content)

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
def UploadUserImageAPI(request):
    if request.method == 'POST':
        msg     = {}
        getProfile = Profile.objects.get(user=request.user)
        data    = request.data['image']
        format, image_str = data.split(';base64,')
        ext     = format.split('/')[-1]
         # You can save this as $
        if data is None:
            msg = {"msg": "Some error has occured"}
        else:
            data = ContentFile(base64.b64decode(image_str), name='usr_.' + ext)
            getProfile.image = data
            getProfile.save()
            msg = {"msg": "Image Successfully Changed"}
        return Response(msg)

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
def UploadUserCoverAPI(request):
    if request.method == 'POST':
        msg     = {}
        getProfile = Profile.objects.get(user=request.user)
        data    = request.data['image']
        format, image_str = data.split(';base64,')
        ext     = format.split('/')[-1]
         # You can save this as $
        if data is None:
            msg = {"msg": "Some error has occured"}
        else:
            data = ContentFile(base64.b64decode(image_str), name='usr_.' + ext)
            getProfile.cover = data
            getProfile.save()
            msg = {"msg": "Cover Successfully Changed"}
        return Response(msg)


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
def EmailChangeAPI(request):
    if request.method == 'POST':
        msg         = {}
        email       = request.data['email']
        countMail   = User.objects.filter(email=email).count() 
        if email is None:
            msg = {"msg":"You need to Insert a E-mail"}
        elif countMail > 0:
            msg = {"msg":"This E-mail is Already Registered!"}
        else:
            getUser         = User.objects.get(id=request.user.id)
            getUser.email   = email
            getUser.save()
            msg = {"msg":"E-mail successfully changed"}
        return Response(msg)



@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
def DefaulAvatarAPI(request):
    if request.method == 'GET':
        getAv = DefaultAvatar.objects.order_by("id")
        serializer = DefaultAvatarSerializer(getAv, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        avId = request.data['avatar']
        instanceAv = DefaultAvatar.objects.get(id=avId)
        msg = {}
        if avId == None:
            msg = {"msg":"No Avatar has been Selected"}
        else:
            qs = Profile.objects.filter(user=request.user).update(image=instanceAv.image)
            msg = {"msg": "Avatar Changed Successfully!"}
        return Response(msg)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def UserDetailsAPI(request):
    if request.method == 'GET':
        getProfile = Profile.objects.get(user=request.user)
        uId         = request.GET['id']
        user        = User.objects.get(id=uId)
        serializer  = UserSerializer(user)
        return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def UserExtraDetailsAPI(request):
    if request.method == 'GET':
        uId = request.GET['id']
        u = User.objects.get(id=uId)
        user = User.objects.annotate(total_watching=Sum(F('animestatus__episodes_number') * F('animestatus__anime__minutes_per_episode'), output_field=FloatField()),
                                     total_completed=Sum((F('animestatus__completed') * F('animestatus__anime__episodes_number')) * F('animestatus__anime__minutes_per_episode'),
                                                         output_field=FloatField(), filter=Q(animestatus__status=2))).get(id=u.id)
        total_completed = AnimeStatus.objects.filter(user=u, status__id=2).count()
        total_watching  = AnimeStatus.objects.filter(user=u, status__id=1).count()
        total_dropped   = AnimeStatus.objects.filter(user=u, status__val=3).count()
        total_plan      = AnimeStatus.objects.filter(user=u, status__val=5).count()
        return Response({"total_hours":user.total_watching,
                         "total_completed":user.total_completed,
                         "animes_completed":total_completed,
                         "animes_watching":total_watching,
                         "animes_dropped":total_dropped, "animes_plan":total_plan})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def ProfileAPI(request):
    if request.method == 'GET':
        getUser = User.objects.get(id=request.user.id)
        serializer = UserSerializer(getUser, many=False)
        return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def UserDataAPI(request):
    if request.method == 'GET':

        user = User.objects.annotate(total_watching=Sum(F('animestatus__episodes_number') * F('animestatus__anime__minutes_per_episode'), output_field=FloatField()),
                                     total_completed=Sum((F('animestatus__completed') * F('animestatus__anime__episodes_number')) * F('animestatus__anime__minutes_per_episode'),
                                                         output_field=FloatField(), filter=Q(animestatus__status=2))).get(id=request.user.id)

        total_completed = AnimeStatus.objects.filter(user=request.user, status__id=2).count()
        total_watching = AnimeStatus.objects.filter(user=request.user, status__id=1).count()
        total_dropped = AnimeStatus.objects.filter(user=request.user, status__val=3).count()
        total_plan = AnimeStatus.objects.filter(user=request.user, status__val=5).count()
        return Response({"total_hours":user.total_watching,
                         "total_completed":user.total_completed,
                         "animes_completed":total_completed,
                           "animes_watching":total_watching,
                         "animes_dropped":total_dropped, "animes_plan":total_plan})

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def FollowerAPI(request):
    if request.method == 'GET':
        followerId      = request.GET['id']
        followers       = Followers.objects.filter(follower=request.user, followers=followerId)
        f_state         = 0
        if followers.count() == 0:
            qs = Followers.objects.create(follower=request.user, followers=followerId)
            f_state = 0
        elif followers.count() > 0:
            qs = Followers.objects.filter(follower=request.user, followers=followerId).delete()
            f_state = 1
        return Response({"f_state":f_state})

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def DetectFollowerAPI(request):
    followerId = request.GET['id']
    followers = Followers.objects.filter(follower=request.user, followers=followerId)
    f_state = 0
    if followers.count() == 0:
        f_state = 1
    elif followers.count() > 0:
        f_state = 0
    return Response({"f_state": f_state})

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def ListFollowersAPI(request):
    if request.method == 'GET':
        getProfile    = Profile.objects.get(user=request.user)
        followersList = []
        follower      = ''
        getF = Followers.objects.filter(follower=request.user).exclude(followers__id__in=getProfile.blockuser.values_list('id', flat=True))
        for i in getF:
            followersList.append(i.followers)
        qs = User.objects.filter(id__in=followersList)
        page = request.GET.get('page', 1)
        paginator = Paginator(qs, 15)
        try:
            follower = paginator.page(page)
        except PageNotAnInteger:
            follower = paginator.page(1)
        except EmptyPage:
            follower = paginator.page(paginator.num_pages)
        serializer = UserSerializer(follower, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def ListFollowingAPI(request):
    if request.method == 'GET':
        getProfile = Profile.objects.get(user=request.user)
        follower = ''
        qs = Followers.objects.filter(followers=request.user.id).exclude(followers__id__in=getProfile.blockuser.values_list('id', flat=True))
        page = request.GET.get('page', 1)
        paginator = Paginator(qs, 15)
        try:
            follower = paginator.page(page)
        except PageNotAnInteger:
            follower = paginator.page(1)
        except EmptyPage:
            follower = paginator.page(paginator.num_pages)
        serializer = FollowerSerializer(follower, many=True)
        return Response(serializer.data)

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
def AnimeReviewAPI(request):
    if request.method == 'GET':
        id = request.GET['id']
        qs = AnimeReview.objects.filter(anime__id=id, draft=1)
        serializer = AnimeReviewSerializer(qs, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        id          = request.data['id']
        rev         = request.data['review']
        draft       = request.data['draft']
        msg         = {}
        anime       = Anime.objects.get(id=id)
        getStatus   = AnimeStatus.objects.get(anime__id=id, user=request.user)
        countRev    = AnimeReview.objects.filter(anime__id=id, user=request.user)
        if countRev.count() > 0 and rev is not None:
            qs  = countRev.update(review=rev, status=getStatus, draft=draft)
            msg = {"msg": "Review Updated Successfully"}
        elif countRev.count() == 0 and rev is not None:
            qs          = AnimeReview.objects.create(anime=anime, user=request.user, review=rev, status=getStatus,
                                                     draft=draft)
            msg         = {"msg":"Review Added Successfully"}
        else:
            msg = {"msg": "You need to write a review!"}
        return Response(msg)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def getAllReviewsAPI(request):
    if request.method == 'GET':
        getProfile  = Profile.objects.get(user=request.user)
        id          = request.GET['id']
        qs          = AnimeReview.objects.filter(anime__id=id, draft=1).exclude(user__id__in=getProfile.blockuser.values_list('id', flat=True))
        serializer  = AnimeReviewSerializer(qs, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def getReviewAPI(request):
    if request.method == 'GET':
        id          = request.GET['id']
        qs          = AnimeReview.objects.get(id=id, draft=1)
        serializer  = AnimeReviewSerializer(qs)
        return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def getMyReviewAPI(request):
    if request.method == 'GET':
        id              = request.GET['id']
        qs              = None
        msg     = {'default':True}
        countReviews    =  AnimeReview.objects.filter(anime__id=id, user__id=request.user.id).count()
        if countReviews > 0:
            qs          = AnimeReview.objects.get(anime__id=id, user__id=request.user.id)
            serializer  = AnimeReviewSerializer(qs)
            msg         = serializer.data
        return Response(msg)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def MyReviewsAPI(request):
    if request.method == 'GET':
        qs          = AnimeReview.objects.filter(user=request.user).order_by("date")
        serializer  = AnimeReviewSerializer(qs, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def collectPointsAPI(request):
    if request.method == 'GET':
        valPoint    = CollectPoint.objects.filter(user=request.user, date=date.today())
        getPoints   = Profile.objects.get(id=request.user.pk)
        getAnime    = AnimeStatus.objects.filter(user=request.user)
        collected   = False
        msg = {'msg':''}
        if valPoint.count() == 0 and getAnime.count() == 0:
            p = getPoints.points + 1
            qs = Profile.objects.filter(id=request.user.id).update(points=p)
            msg = {'msg':'Point Collected Successfully', 'state':True}
        elif valPoint.count() > 0:
            msg = {'msg': 'Point Collected Successfully', 'state': True}
        return Response(msg)


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
def TopicAPI(request):
    if request.method == 'GET':
        qs          = Topic.objects.order_by("date")
        serializer  = TopicSerializer(qs, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        title       = request.data['title']
        description = request.data['description']
        anime       = request.data['animeId']
        getAnime    = Anime.objects.get(id=anime)
        msg = {}
        if title == None:
            msg = {'msg':'You need to Insert a title'}
        elif description == None:
            msg = {'msg': 'You need to Insert a topic Description.'}
        else:
            Topic.objects.create(user=request.user, anime=getAnime, title=request.data['title'],
                                 description=description)
            msg = {'msg': 'Topic Created Successfully.'}
        return Response(msg)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def GetFollowerUpdatesAPI(request):
    if request.method == 'GET':
        getProfile = Profile.objects.get(user=request.user)
        listF = []
        getFollowers = Followers.objects.filter(follower=request.user)
        for i in getFollowers:
            listF.append(i.followers)
        qs = AnimeStatus.objects.filter(user__pk__in=listF).exclude(anime__categorie__id__in=getProfile.rating.values_list('id', flat=True),
                                                                    user__id__in=getProfile.blockuser.values_list('id', flat=True)).order_by("-date")
        serializer = AnimeStatusSerializer(qs, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def ReportMotiveAPI(request):
    if request.method == 'GET':
        qs          = ReportMotive.objects.order_by("motive")
        serializer  = ReportMotiveSerializer(qs, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def ReportAPI(request):
    if request.method == 'GET':
        user            = request.user
        motiveId        = request.GET['motive']
        type            = request.GET['type']
        pid             = request.GET['pid']
        motive          = ReportMotive.objects.get(id=motiveId) #instance motive
        qs              = ReportSection.objects.create(user=user, type=type, pid=pid, motive=motive)
        subject         = 'Report - %s' % (type)
        msgBody         = 'We are sending you a report of user %s about %s with id %s because of %s' % (request.user.username, type, pid, motive.motive)
        send_mail(subject, msgBody, 'report.anibook@programadoracoriano.com', ['report.anibook@programadoracoriano.com', ])
        msgStr          = '%s successfully reported' % (type)
        msg             = {'msg': msgStr}
        return Response(msg)



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def GetRatingAPI(request):
    if request.method == 'GET':
        qs          = Rating.objects.order_by("id")
        serializer  = RatingSerializer(qs, many=True)
        return Response(serializer.data)

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
def AddRatingFilterAPI(request):
    if request.method == 'POST':
        ratingId     = request.data['rating']
        getRating    = Rating.objects.get(id=ratingId)
        profile     = Profile.objects.get(user=request.user)
        qs          = profile.rating.add(getRating)
        msg         =  {"msg": "Rating excluded Successfully!"}
    return Response(msg)

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
def RemoveRatingFilterAPI(request):
    if request.method == 'POST':
        ratingId     = request.data['rating']
        getRating    = Rating.objects.get(id=ratingId)
        profile     = Profile.objects.get(user=request.user)
        qs          = profile.rating.remove(getRating)
        msg         =  {"msg": "Rating excluded Successfully!"}
    return Response(msg)

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
def AddBlockUserAPI(request):
    if request.method == 'POST':
        userId     = request.data['user']
        getUser    = User.objects.get(id=userId)
        profile    = Profile.objects.get(user=request.user)
        qs          = profile.blockuser.add(getUser)
        msg         =  {"msg": "User successfully Blocked!"}
    return Response(msg)

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
def RemoveBlockUserAPI(request):
    if request.method == 'POST':
        userId     = request.data['user']
        getUser    = User.objects.get(id=userId)
        profile    = Profile.objects.get(user=request.user)
        qs          = profile.blockuser.remove(getUser)

        msg         =  {"msg": "User successfully unblocked!"}
    return Response(msg)





@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def LogoutAPI(request):
    return Response({"isLoggout":True})


#delete section
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def deleteReviewAPI(request):
    if request.method == 'GET':
        id          = request.GET['id']
        qs          = AnimeReview.objects.filter(id=id, user=request.user).delete()
        query       = AnimeReview.objects.filter(user=request.user).order_by("date")
        serializer  = AnimeReviewSerializer(query, many=True)
        return Response(serializer.data)

