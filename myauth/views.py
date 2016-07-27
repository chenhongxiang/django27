# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse  
from django.contrib.auth.forms import AuthenticationForm #,UserCreationForm,  
from django.contrib.auth.models import User



# qiu


from django.views.generic import View
# from django.http import HttpResponseRedirect
from django.shortcuts import render

class Loging_View(View):
    form_class = AuthenticationForm
    initial = {'key': 'value'}
    template_name = 'myauth/login.html'

    def get(self, request, *args, **kwargs):
        _get = request.GET
        if _get.get('next'):
            next_url = request.GET['next']
            print 'next_url = %s' % next_url
        else:
            next_url = 'new_next'
            print 'next_url = %s' % next_url
            

        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'app_path': '/myauth/login_info_show/?next=%s' % next_url ,
                                                    'form': form})
    # post 转向窗口，需考虑功能需求
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return HttpResponseRedirect('/success/')

        return render(request, self.template_name, {'app_path': '/myauth/login_info_show/?next=%s' % 'next_url' ,
                                                    'form': form})





@login_required(login_url='/myauth/login_view/')
#@login_required(login_url = '/accounts/login/') 
def my_view(request):
    myuser = request.user
    if not myuser.is_authenticated():
        print '....'
    else:
        print '+++++++++', myuser.id, myuser.username
        
    u = User.objects.get(username__exact=myuser.username)
    print u.last_name
      
    if myuser is not None:
        if myuser.is_active:
            data = {'user':myuser}
            request.session['member_id'] = myuser.id
        else:
            pass
            data = {'user':myuser}
            # Return a 'disabled account' error message
    else:
        # Return an 'invalid login' error message.
        data = {'user':{'last_name':'invalid login',
                        'first_name':'invalid login',
                         'is_active':"否",                        
                        }}
        pass
    
    member_id = request.session.get('member_id', False)
    
    if member_id:
        # user.objects.all()
        data['member'] = {}
        data['member']['member_id'] = member_id
        data['member']['member_name'] = myuser.username
        
    return render_to_response(
        'myauth/show_login_results.html',
        data,
        context_instance=RequestContext(request))
    


# def register(request):  
#     form = UserCreationForm()  
#   
#     if request.method == 'POST':  
#         data = request.POST.copy()  
#         errors = form.get_validation_errors(data)  
#         if not errors:  
#             new_user = form.save()  
#             return HttpResponseRedirect("/accounts/created/")  
#     else:  
#         data, errors = {}, {}  
#     return render_to_response("registration/register.html", {  
#          'form' : forms.FormWrapper(form, data, errors)  
#      })


def login_info_show(request):
    if 'username' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
    else:
        user = None
        
    if 'next' in request.GET:
        next_url = request.GET['next']
    else:
        next_url = "/myauth/my_view/"
    
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
            #'show_login_results.html'
            
            print user.has_perm('foo.add_bar')
            print user.get_all_permissions()
            #set([u'auth.add_user', u'admin.delete_logentry', u'auth.add_group', u'sessions.add_session', u'contenttypes.delete_contenttype', u'auth.add_permission', u'polls.delete_person', u'auth.change_permission', u'sessions.change_session', u'polls.add_question', u'polls.change_question', u'polls.add_person', u'polls.add_choice', u'contenttypes.add_contenttype', u'auth.delete_group', u'auth.delete_user', u'auth.delete_permission', u'polls.delete_question', u'admin.add_logentry', u'polls.delete_choice', u'contenttypes.change_contenttype', u'auth.change_user', u'polls.change_person', u'sessions.delete_session', u'admin.change_logentry', u'polls.change_choice', u'auth.change_group'])

            
            return HttpResponseRedirect(next_url)  
            #return HttpResponseRedirect("/myauth/my_view/")  
        else:
            data = {'user':{'last_name': username,
                            'first_name':'禁止登录',
                             'is_active':"帐号非活动",                        
                            }}

            # Return a 'disabled account' error message
    else:
        # Return an 'invalid login' error message.
        data = {'user':{'last_name':'无此用户',
                        'first_name':'禁止登录',
                         'is_active':"帐号非活动",                        
                        }}
        pass
    
    return render_to_response(
        'myauth/show_login_results.html',
        data,
        context_instance=RequestContext(request))
    


def login_view(request):
    form = AuthenticationForm()  
    next_url = request.GET['next']
    
    # Redirect to a success page.    
    return render_to_response(
        'myauth/login.html',
        {'app_path': '/myauth/login_info_show/?next=%s' % next_url , 
         'form':form},
        context_instance=RequestContext(request))


def logout_view(request):
    logout(request)
    try:
        del request.session['member_id']
    except KeyError:
        pass
    return HttpResponse("You're logged out.")
    
#     # Redirect to a success page.    
#     return render_to_response(
#         'myauth/login.html',
#         {},
#         context_instance=RequestContext(request))
        
    
    