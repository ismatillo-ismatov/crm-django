from django.shortcuts import render,redirect,reverse
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.views import generic
from agents.mixins import OrganisorAndLoginMixin
from .models import *
from .form import LeadForm,LeadModelForm,CustomCreateForm, AssignAgentForm,LeadCategoryUpdateForm


class SignUp(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomCreateForm

    def get_success_url(self):
        return reverse("login")

class LandingPageView(generic.TemplateView):
    template_name = "landing.html"


def leanding_page(request):
    leads = Lead.objects.all()
    context = {
        "leads":leads
    }
    return render(request,'landing.html',context)

class LeadListView(LoginRequiredMixin,generic.ListView):
    template_name = "leads/lead_list.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile, agent__isnull=False)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation, agent__isnull=False)
            queryset = queryset.filter(agent__user=user)
        return queryset
    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile,
                agent__isnull=True
            )
            context.update({
                "unassigned_leads":queryset
            })
            return context

def lead_list(request):
    leads = Lead.objects.all()
    context = {
        "leads":leads
    }
    return render(request,'leads/lead_list.html',context)


class LeadDetailView(LoginRequiredMixin,generic.DetailView):
    template_name = "leads/lead_detail.html"
    queryset = Lead.objects.all()
    context_object_name = "leads"

def lead_detail(request,pk):
    lead = Lead.objects.get(id=pk)
    context = {
        "lead":lead
    }

    return render(request,'leads/lead_detail.html',context)


class LeadCreateView(LoginRequiredMixin,generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm
    def get_success_url(self):
        return reverse("app:list")

    def form_valid(self, form):
        send_mail(
            subject='created lead',
            message='go to new lead',
            from_email='ismatov1995@gmail.com',
            recipient_list=['ismatov1995@gmail.com']
        )
        messages.success(self.request,"You have successfully created a lead")
        return super(LeadCreateView,self).form_valid(form)

def create_lead(request):
    form = LeadModelForm()
    if request.method == "POST":
        form = LeadModelForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect("/app")
    context = {
        "form":form
    }
    return render(request,"leads/lead_create.html",context)


class LeadUpdateView(LoginRequiredMixin,generic.UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadModelForm
    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation=user.userprofile)
def lead_update(request,pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)
    if request.method == "POST":
        form = LeadModelForm(request.POST,instance=lead)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect("/app")
    context = {
        "lead":lead,
        "form":form
    }
    return render(request, "leads/lead_update.html",context)


class LeadDeleteView(LoginRequiredMixin,generic.DeleteView):
    template_name = "leads/lead_delete.html"
    queryset = Lead.objects.all()
    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation=user.userprofile)



def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/app")

class AssignAgentView(OrganisorAndLoginMixin,generic.FormView):
    template_name = "leads/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self,**kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update( {
            "request": self.request
        })
        return kwargs
    def get_success_url(self):
        return reverse("app:list")

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead =  Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)


class CategoryListView(LoginRequiredMixin,generic.ListView):
    template_name = "leads/category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation
            )
        context.update({
            "unassigned_lead_count": queryset.filter(category__isnull=True).count()
        })
        return context

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset


class CategoryDetailView(LoginRequiredMixin,generic.DetailView):
    template_name = "leads/category_detail.html"
    context_object_name = "category"


    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset

class CategoryUpdateView(LoginRequiredMixin,generic.UpdateView):
    template_name = "leads/lead_category_update.html"
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset
    def get_success_url(self):
        return reverse("app:detail",kwargs={"pk":self.get_object().id})