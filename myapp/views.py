from django.contrib.auth.models import User
from django.shortcuts import render,get_object_or_404
from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm,UserUpdateForm,ProfileForm
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm,CommentForm
from myapp.models import Video,Category,Profile,Comment,Wishlist
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView,RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse
from django.urls import reverse_lazy
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account created for {username}! Now make your Profile')
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('/')
    else:
        form = UserRegisterForm()
    return render(request,'register.html',{'form':form})

@login_required
def home(request):
    vdo = Video.objects.all().order_by('-added_date')
    cats = Category.objects.all()
    if request.method == 'POST':
        user_id = request.user
        video_id = request.POST['video_id']

        wishlist = Wishlist(video_id=video_id,user_id=user_id)
        wishlist.save()
        return redirect(f'/home/')

    data={"vdo":vdo,"cats":cats}
    return render(request,'index.html',data)

@login_required
def category_page(request,pk):
    print(pk)
    cats = Category.objects.all()
    category = Category.objects.get(pk=pk)
    
    vdo = Video.objects.filter(cat=category).order_by('-added_date')

    data={"vdo":vdo, "cats":cats}
    return render(request,'index.html',data)

@login_required
def search(request):
    vdo = Video.objects.all().order_by('-added_date')
    cats = Category.objects.all()
    if request.method=='GET':
        keywords = request.GET.get('keywords')
        vdo = Video.objects.filter(Q(title__icontains=keywords))
        if keywords:
            if vdo:
                vdo = Video.objects.filter(Q(title__icontains=keywords))
            else:
                messages.warning(request,'No Result Found')

    return render(request,'result.html',{'keywords':keywords,'vdo':vdo,'cats':cats,'vdo':vdo})

@login_required
def vdodetail(request,pk):
    vdos = Video.objects.filter(pk=pk)
    author = Profile.objects.filter(pk=pk)
    vdo = Video.objects.all().order_by('-added_date')
    cats = Category.objects.all()
    coment = Comment.objects.filter(video=pk, parent__isnull=True)
    video = get_object_or_404(Video, pk=pk)
    user = User.objects.get(pk=request.user.id)
    if request.method == 'POST' :
        formc = CommentForm(request.POST, request.FILES)
        print('hi')
        if formc.is_valid():
            parent_obj = None
            # get parent comment id from hidden input
            try:
                # id integer e.g. 15
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            # if parent_id has been submitted get parent_obj id
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                # if parent object exist
                if parent_obj:
                    # create replay comment object
                    replay_comment = formc.save(commit=False)
                    # assign parent_obj to replay comment
                    replay_comment.parent = parent_obj
            # form save 
            formc = formc.save(commit=False)
            # Assign the current post to the comment
            formc.video = video
            user = request.user
            formc.user = user
            try:
                reply = int(request.POST.get('reply'))
            except:
                reply = None
            # Save the comment to the database
            formc.save()
            messages.success(request,f'Comment Added')
            return redirect(f'/home/video/{video.pk}')
    else:
        formc = CommentForm()
    
    if request.method == 'POST' and not formc.is_valid():
        lvideo = get_object_or_404(Video,pk= request.POST.get('video_id'))
        lvideo.like.add(request.user.pk)
    
    data={"vdo":vdo,"cats":cats,"vdos":vdos,
    "coment":coment,"vdos":vdos,"author":author,
    'formc':formc,'video':video} 
    return render(request,'vdodetail.html',data)

class VideoCreateView(LoginRequiredMixin, CreateView):
    model = Video
    template_name = "vdoform.html"
    fields = ('title','description','path','cat')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class VideoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Video
    template_name = "vdoform.html"
    fields = ('title','description','path','cat')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        else:
            return False

class VideoDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Video
    template_name = "vdodelete.html"
    success_url = ('/home/')

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        else:
            return False

@login_required
def profile_user(request,pk):
    author = Profile.objects.filter(pk=pk)
    vdos = Video.objects.filter(user=pk)
    vdo = Video.objects.filter(user=pk)
    
    return render(request,'user_profile.html',{'author':author,'vdos':vdos,'vdo':vdo})

@login_required
def update(request,pk):
    author = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'Your Account Has Been Updated!')
            return redirect(f'/userprofile/{author.pk}')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileForm(instance=request.user.profile)
    return render(request,'update.html',{'u_form':u_form,'p_form':p_form,'author':author})

@login_required
def commentdelete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.user == request.user:
        comment.is_removed = True
        comment.save()
        return render(request,'commentdelete.html',{'comment': comment})

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    template_name = "commentform.html"
    fields = ('text','img')
    success_url = ('/home/')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        else:
            return False

class CommentDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Comment
    template_name = "commentdelete.html"
    success_url = ('/home/')
 

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        else:
            return False

def vlikes(request,pk):
    video = get_object_or_404(Video,pk= request.POST.get('video_id'))
    video.like.add(request.user.pk)
    return render(request,'vdodetail.html',{'video':video})

def watchlist(request):
    wishlist = Wishlist.objects.all()
    return render(request,'watchlist.html',{'wishlist':wishlist})


# @login_required
# def cupdate(request,pk):
#     video = Video.object.filter(pk=pk)
#     user = User.objects.get(pk=request.user.id)
#     if request.method == 'POST' :
#         form = CommentForm(request.POST, request.FILES)
#         print('hi')
#         if form.is_valid():
#             print('hello')
#             form = form.save(commit=False)
#             # Assign the current post to the comment
#             form.video = video
#             user = request.user
#             form.user = user
#             # Save the comment to the database
#             form.save()
#             messages.success(request,f'Comment Added')
#             return redirect(f'/home/video/{video.pk}')
#     else:
#         form = CommentForm()
#     return render(request,'commentform.html',{'video':video} )



# @login_required
# def profile(request):
#     return render(request,'profile.html')


# class VideoDetailView(LoginRequiredMixin,DetailView):
#     model = Video
#     template_name = "vdodetail.html"