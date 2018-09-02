from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,JsonResponse,HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView,UpdateView,CreateView,View
from django.contrib.auth.models import User
from .models import *
from user_profile.models import *
from meal.forms import feedbackCreateForm,Add_meal
from django.views.generic import View
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from unidecode import unidecode
from django.views.generic.edit import ModelFormMixin
import json
from django.db.models import Max
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.shortcuts import get_list_or_404, get_object_or_404
import datetime
from django.utils.timezone import utc
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

def userlike(request , **kwargs):
    qs_user = UserProfile.objects.filter(user=request.user)
    if not qs_user:
        return HttpResponseRedirect('/Home/chief')
    meal_id = kwargs['pk']
    user = request.user
    user_like = str(request.GET.get('like', None))
    meal = Meal.objects.get(id=meal_id)
    like = UserLike.objects.filter(user__username=request.user).filter(meal__id=meal_id)
    if user_like == 'true':
        if like:
            like.update(like=1)
        else:
            like.create(
                user=request.user,
                like=1,
                meal=meal
            )
    else:
        if like:
            like.delete()
    return  HttpResponse(json.dumps({'data': user_like}), content_type="application/json")

def rate(request,**kwargs):
    qs_user = UserProfile.objects.filter(user=request.user)
    if not qs_user:
        return HttpResponseRedirect('/Home/chief')
    meal_id = kwargs['pk']
    meal_old_rate = Rate.objects.filter(meal__id=meal_id)
    meal = Meal.objects.get(id = meal_id)
    new_user_rate = float(request.GET.get('rating', None))
    user_old_rate = UserRate.objects.filter(user__username=request.user).filter(meal__id = meal_id)
    if user_old_rate:
        votes = meal_old_rate[0].Votes
        new_meal_rate = ((meal_old_rate[0].rate_value * votes)- user_old_rate[0].rate_value + new_user_rate)/votes
        new_meal_rate = round(new_meal_rate,2)
        obj = meal_old_rate .update(rate_value=new_meal_rate)
        user_old_rate.update(rate_value=new_user_rate)
    else:
        UserRate.objects.create(meal=meal,rate_value=new_user_rate,user=request.user)
        votes = meal_old_rate [0].Votes
        if votes == 0 :
            new_meal_rate = new_user_rate
        else:
            new_meal_rate = ((meal_old_rate [0].rate_value * votes)+ new_user_rate)/(votes+1)
        new_meal_rate = round(new_meal_rate, 2)
        obj = meal_old_rate.update(rate_value=new_meal_rate,Votes=votes+1)
    user_rate = UserRate.objects.filter(user__username=request.user).filter(meal__id = meal_id)
    meal_rate = Rate.objects.get(meal__id = meal_id)
    return HttpResponse(json.dumps({'user_rate': user_rate[0].rate_value,"meal_rate": meal_rate.rate_value }), content_type="application/json")

def comment(request, **kwargs):
    if request.user.is_authenticated:
        meal_id         = kwargs['pk']
        meal            = Meal.objects.get(id=meal_id)
        user            = request.user
        qs_user         = UserProfile.objects.filter(user=user)

        if not qs_user:
            qs_user     = ChiefProfile.objects.filter(user=user)

        comment         = request.GET.get('comment', None)
        obj             = Comment.objects.create(meal=meal, comment=comment, user=user)
        meal_comments   = Comment.objects.filter(meal=meal)
        meal_comm_count = Comment.objects.filter(meal=meal).count()
        index           = int(meal_comm_count)-1
        comments        = []

        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        for com in meal_comments:
            diff = now - com.timeStemp
            if diff.days < 1:
                if diff.seconds / 3600 < 1:
                    if diff.seconds / 60 < 1:
                        last_time = str(int(diff.seconds)) + 'seconds'
                    else:
                        last_time = str(int(diff.seconds / 60)) + 'minutes'
                else:
                    last_time = str(int(diff.seconds / 3600)) + 'hours'
            else:
                last_time = str(int(diff.days)) + 'days'

            if qs_user[0].img:
                comments.append([com.comment,com.user.first_name,com.user.last_name,qs_user[0].img.url,last_time, com.id])
            else:
                comments.append([com.comment, com.user.first_name, com.user.last_name, "",last_time, com.id])
        return HttpResponse(json.dumps({'comments': comments[index]}), content_type="application/json")

    return HttpResponse(json.dumps({}), content_type="application/json")


def reply(request, **kwargs):
    if request.user.is_authenticated:
        comment_id          = kwargs['pk']
        comment             = Comment.objects.get(id=comment_id)
        user                = request.user
        qs_user             = UserProfile.objects.filter(user=user)

        if not qs_user:
            qs_user         = ChiefProfile.objects.filter(user=user)

        reply               = request.GET.get('reply', None)
        obj                 = Reply.objects.create(comment=comment, user=user, reply=reply)
        comment_reply       = Reply.objects.filter(comment=comment)
        replys_count        = Reply.objects.filter(comment=comment).count()
        index               = int(replys_count)-1
        replys              = []
        now                 = datetime.datetime.utcnow().replace(tzinfo=utc)

        for com in comment_reply:
            diff = now - com.timeStemp
            if diff.days < 1:
                if diff.seconds / 3600 < 1:
                    if diff.seconds / 60 < 1:
                        last_time = str(int(diff.seconds)) + 'seconds'
                    else:
                        last_time = str(int(diff.seconds / 60)) + 'minutes'
                else:
                    last_time = str(int(diff.seconds / 3600)) + 'hours'
            else:
                last_time = str(int(diff.days)) + 'days'

            if qs_user[0].img:
                replys.append([reply, com.user.first_name, com.user.last_name, qs_user[0].img.url,last_time,obj.id])
            else:
                replys.append([reply, com.user.first_name, com.user.last_name, "",last_time,obj.id])
        return HttpResponse(json.dumps({'comments': replys[index]}), content_type="application/json")

    return HttpResponse(json.dumps({}), content_type="application/json")


def comment_like(request, **kwargs):
    comment_id  = kwargs['pk']
    comment     = Comment.objects.filter(id = comment_id)
    check       = LikeComment.objects.filter(user=request.user).filter(comment=comment[0])
    like_val    = request.GET.get('like', None)

    if check:
        if like_val == 'true':
            LikeComment.objects.filter(user=request.user).filter(comment=comment[0]).update(
                react_value= True
            )
        else:
            LikeComment.objects.filter(user=request.user).filter(comment=comment[0]).update(
                react_value= False
            )
    else:
        LikeComment.objects.create(
            comment=comment[0],
            user=request.user,
            react_value=True
        )

    return HttpResponse(json.dumps({'data': like_val}), content_type="application/json")


def reply_like(request, **kwargs):
    reply_id = kwargs['pk']
    reply = Reply.objects.filter(id=reply_id)
    check = LikeComment.objects.filter(user=request.user).filter(reply=reply[0])
    like_val = request.GET.get('like', None)
    if check:

        if like_val == 'true':
            LikeComment.objects.filter(user=request.user).filter(reply=reply[0]).update(
                react_value=True
            )
        else:
            LikeComment.objects.filter(user=request.user).filter(reply=reply[0]).update(
                react_value=False
            )
    else:
        LikeComment.objects.create(
            reply=reply[0],
            user=request.user,
            react_value=True
        )

    return HttpResponse(json.dumps({'data': like_val}), content_type="application/json")


def calc_diff_time(replys,user):
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    replys_with_time = []
    for reply in replys:
        diff    = now - reply.timeStemp
        if user.is_authenticated:
            state = LikeComment.objects.filter(user=user).filter(reply=reply)
        else:
            state = None

        if diff.days < 1:
            if diff.seconds / 3600 < 1:
                if diff.seconds / 60 < 1:
                    last_time = str(int(diff.seconds)) + 'seconds'
                    replys_with_time.append([last_time, reply, state])
                else:
                    last_time = str(int(diff.seconds / 60)) + 'minutes'
                    replys_with_time.append([last_time, reply, state])
            else:
                last_time = str(int(diff.seconds / 3600)) + 'hours'
                replys_with_time.append([last_time, reply, state])
        else:
            last_time = str(int(diff.days)) + 'days'
            replys_with_time.append([last_time, reply, state])

    return replys_with_time



class meal_new(View):
    def get(self, request, **kwargs):
        template_name   = "meal.html"
        meal_id         = kwargs['pk']
        meal            = Meal.objects.get(id=meal_id)
        meal_rate       = Rate.objects.get(meal__id=meal_id)
        comments        = Comment.objects.filter(meal__id=meal_id)
        now             = datetime.datetime.utcnow().replace(tzinfo=utc)
        comments_time   = []

        for comment in comments:
            replys      = Reply.objects.filter(comment=comment)
            if request.user.is_authenticated:
                c_state = LikeComment.objects.filter(user=request.user).filter(comment=comment)
            else:
                c_state = None

            diff        = now - comment.timeStemp

            if diff.days < 1:
                if diff.seconds/3600 < 1:
                    if diff.seconds/60 < 1:
                        last_time   = str(int(diff.seconds))+'seconds'
                        replys_time = calc_diff_time(replys, request.user)
                        comments_time.append([last_time, comment,replys_time,c_state])
                    else:
                        last_time   = str(int(diff.seconds/60))+'minutes'
                        replys_time = calc_diff_time(replys, request.user)
                        comments_time.append([last_time, comment, replys_time, c_state])
                else:
                    last_time   = str(int(diff.seconds/3600))+'hours'
                    replys_time = calc_diff_time(replys, request.user)
                    comments_time.append([last_time, comment, replys_time, c_state])
            else:
                last_time   = str(int(diff.days))+'days'
                replys_time = calc_diff_time(replys, request.user)
                comments_time.append([last_time, comment, replys_time, c_state])

        likes_count         = UserLike.objects.filter(meal=meal).count()
        context = {
            'meal': meal,
            'likes_count': likes_count,
            'comments'  : comments_time,
            'meal_rate' : meal_rate
        }
        if request.user.is_authenticated:
            comment_likes = LikeComment.objects.filter(user=request.user)
            user_rate   = UserRate.objects.filter(user = request.user).filter(meal__id = meal_id)
            rate_stars = [
                [5, 'star5', 'full'],
                [4.5, 'star4half', 'half'],
                [4, 'star4', 'full'],
                [3.5, 'star3half', 'half'],
                [3,'star3','full'],
                [2.5, 'star2half', 'half'],
                [2, 'star2', 'full'],
                [1.5, 'star1half', 'half'],
                [1, 'star1', 'full'],
                [.5, 'starhalf', 'half'],
            ]
            if user_rate:
                u_rate      = float(user_rate[0].rate_value)
                i           = 0.5
                rate_arr    = []
                while i<= u_rate:
                    rate_arr.append(i)
                    i = i + .5
            else:
                u_rate  = None
                rate_arr = None

            meal_rate.rate_value    = round(meal_rate.rate_value,2)
            qs                      = ChiefProfile.objects.filter(user__username=self.request.user)
            like                    = UserLike.objects.filter(user__username=self.request.user).filter(meal__id=meal_id)

            if qs and not qs[0].state:
                    return HttpResponseRedirect('/Home/chief')

            context['comment_likes']    = comment_likes
            context['user_rate']        = u_rate
            context['like']             = like
            context['rate_arr']         = rate_arr
            context['rate_stars']       = rate_stars

        return render(request, template_name, context)


def ViewFeedback(request,**kwargs):
    template_name   = 'feedback_view.html'
    qs              = ChiefProfile.objects.filter(user=request.user)
    meal_id         = kwargs['pk']
    obj             = Feedback.objects.filter(meal_id__id=meal_id)
    meal            = Meal.objects.filter(id=meal_id)

    if UserProfile.objects.filter(user=request.user) or meal[0].meal_owner != request.user:
        return HttpResponseRedirect('/')
    elif not qs[0].state:
        return HttpResponseRedirect('/Home/chief')
    context = {
        'feedback': obj,
        'meal': meal_id
    }
    return render(request,template_name,context)

class FeedbackDetails(LoginRequiredMixin,DetailView):
    template_name = 'feed_details.html'
    def get_context_data(self, **kwargs):
        context = super(FeedbackDetails, self).get_context_data(**kwargs)
        qs      = ChiefProfile.objects.filter(user__username=self.request.user)
        context['profile_info'] = qs
        context['group']        = "chief"

        if not qs:
            qs                      = UserProfile.objects.filter(user__username=self.request.user)
            context['profile_info'] = qs
            context['group']        = "user"
        return context

    queryset = Feedback.objects.all()


def deleteMeal(request,**kwargs):
    meal_id     = kwargs['pk']
    meal        = Meal.objects.filter(id=meal_id)
    qs          = ChiefProfile.objects.filter(user=request.user)

    if qs and qs[0].user==meal[0].meal_owner or request.user.is_superuser:
        obj = meal.delete()

    if request.user.is_superuser:
        return redirect('admin_pannel:view-meals')
    return HttpResponseRedirect('/Home/chief')


class UpdateMeal(LoginRequiredMixin,UpdateView):
    template_name   = 'update_meal.html'
    login_url       = reverse_lazy('accounts:login')
    # form_class      = Add_meal
    model = Meal

    fields = [
        'meal_name',
        'meal_recipe',
        'meal_category',
        'ingredients',
        'img',
        'video'
    ]

    def get_success_url(self):
        return "/meal/"+str(self.kwargs['pk'])


    def get_context_data(self, **kwargs):
        context = super(UpdateMeal, self).get_context_data(**kwargs)
        if not self.request.user.is_superuser:
            chef_state          = ChiefProfile.objects.filter(user__username=self.request.user)
            context['state']    = chef_state[0].state
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Meal, pk=self.kwargs['pk'])

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(meal_owner=self.request.user)



class AddMeal(LoginRequiredMixin,CreateView):
    template_name   = "addMeal.html"
    login_url       = reverse_lazy('accounts:login')
    model           = Meal
    fields = [
        'meal_name',
        'meal_recipe',
        'meal_category',
        'ingredients',
        'img',
        'video'
    ]

    def get_success_url(self):
        print("done")
        if self.request.user.is_superuser:
            return reverse_lazy('admin_pannel:home')
        else:
            return reverse_lazy('user_profile:chief-home')

    def form_valid(self, form):
        self.object             = form.save(commit=False)
        self.object.meal_owner  = self.request.user
        self.object.save()
        meal    = Meal.objects.get(id = self.object.id)

        obj     = Rate.objects.create(
            meal= meal,
            rate_value = 0,
            Votes     = 0
        )
        return super(AddMeal, self).form_valid(form)


    def get_context_data(self, **kwargs):
        context = super(AddMeal, self).get_context_data(**kwargs)
        qs      = ChiefProfile.objects.filter(user__username=self.request.user)
        context['profile_info'] = qs
        if qs:
            context['state'] = qs[0].state
        return context


class feedback(View):
    def get(self, request, *args, **kwargs):
        template_name   = "feedback.html"
        form            = feedbackCreateForm(request.GET or None)
        error           = None
        meal_id         = kwargs['pk']
        meal            = Meal.objects.all()

        for meal in meal:
            if meal.id == meal_id:
                if form.is_valid():
                    obj = Feedback.objects.create(
                        meal_id=meal,
                        name=form.cleaned_data.get('name'),
                        user_mail=form.cleaned_data.get('email'),
                        content=form.cleaned_data.get('content'),
                    )
                    return HttpResponseRedirect('/meal/'+str(meal_id))
                if form.errors:
                    error = form.errors
        context = {
            "meal_id": meal_id,
            "form": form,
            "error": error
        }
        if request.user.is_authenticated:
            q_user  = ChiefProfile.objects.filter(user__username=self.request.user)
            qs      = ChiefProfile.objects.filter(user__username=self.request.user)
            if q_user and not qs[0].state:
                return HttpResponseRedirect('/Home/chief')


        return render(request, template_name, context)

