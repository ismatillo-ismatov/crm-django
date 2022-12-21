import datetime
from django.shortcuts import render,redirect,reverse
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.views import generic
from agents.mixins import OrganisorAndLoginMixin
from .models import *
from .form import *


class SignUp(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomCreateForm

    def get_success_url(self):
        return reverse("login")

class LandingPageView(generic.TemplateView):
    template_name = "landing.html"


# lead_list
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



class LeadDetailView(LoginRequiredMixin,generic.DetailView):
    template_name = "leads/lead_detail.html"
    queryset = Lead.objects.all()
    context_object_name = "leads"



class LeadCreateView(OrganisorAndLoginMixin,generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm

    # def get_queryset(self):
    #     user = self.request.user
    #     return Lead.objects.filter(organisation=user.userprofile)

    def get_success_url(self):
        return reverse("app:list")

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organisation = self.request.user.userprofile
        lead.save()
        send_mail(
            subject='created lead',
            message='go to new lead',
            from_email='ismatov1995@gmail.com',
            recipient_list=['ismatov1995@gmail.com']
        )
        messages.success(self.request,"You have successfully created a lead")
        return super(LeadCreateView,self).form_valid(form)



class LeadUpdateView(OrganisorAndLoginMixin,generic.UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadModelForm
    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation=user.userprofile)
    def get_success_url(self):
        return reverse("app:list")


    def form_valid(self, form):
        form.save()
        messages.info(self.request, "update lead")
        return super(LeadUpdateView,self).form_valid(form)




class LeadDeleteView(LoginRequiredMixin,generic.DeleteView):
    template_name = "leads/lead_delete.html"
    queryset = Lead.objects.all()
    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation=user.userprofile)




class AssignAgentView(OrganisorAndLoginMixin,generic.FormView):
    template_name = "leads/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self,**kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs
    def get_success_url(self):
        return reverse("app:list")

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
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
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

        # if user.is_organisor:
        #     queryset = Category.objects.filter(
        #         organisation=user.userprofile
        #     )
        # else:
        #     queryset = Category.objects.filter(
        #         organisation=user.agent.organisation
        #     )
        # return queryset
    def get_success_url(self):
        return reverse("app:detail",kwargs={"pk":self.get_object().id})

class CategoryCreateView(OrganisorAndLoginMixin,generic.CreateView):
    template_name = "leads/category_create.html"
    form_class = CategoryModelForm

    # def get_queryset(self):
    #     user = self.request.user
    #     return Lead.objects.filter(organisation=user.userprofile)

    def get_success_url(self):
        return reverse("app:category-list")

    def form_valid(self, form):
        category = form.save(commit=False)
        category.organisation = self.request.user.userprofile
        category.save()
        return super(CategoryCreateView,self).form_valid(form)

class UpdateCategoryView(OrganisorAndLoginMixin,generic.UpdateView):
    template_name = "leads/category_update.html"
    form_class = CategoryModelForm

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
        return reverse("app:category-list")



class FollowUpCreateView(LoginRequiredMixin,generic.CreateView):
    template_name = "leads/follow_create.html"
    form_class = FollowForm

    def get_success_url(self):
        return reverse("app:detail",kwargs={"pk":self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super(FollowUpCreateView, self).get_context_data(**kwargs)
        context.update({
            "lead": Lead.objects.get(pk=self.kwargs["pk"])
        })
        return context

    def form_valid(self, form):
        lead = Lead.objects.get(pk=self.kwargs["pk"])
        followup = form.save(commit=False)
        followup.lead = lead
        followup.save()
        return super(FollowUpCreateView, self).form_valid(form)

class FollowUpUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "leads/followup_update.html"
    form_class = FollowForm

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = FollowUp.objects.filter(lead__organisation=user.userprofile)
        else:
            queryset = FollowUp.objects.filter(lead__organisation=user.agent.organisation)
            queryset = queryset.filter(lead__agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("app:detail", kwargs={"pk": self.get_object().lead.id})


class FollowUpDeleteView(OrganisorAndLoginMixin,generic.DeleteView):
    template_name = "leads/followup_delete.html"

    def get_success_url(self):
        followup = FollowUp.objects.get(id=self.kwargs["pk"])
        return reverse("app:detail",kwargs={"pk":followup.lead.pk})

    def get_queryset(self):
        user = self.request.user

        if user.is_organisor:
            queryset = FollowUp.objects.filter(lead__organisation=user.userprofile)
        else:
            queryset = FollowUp.objects.filter(lead__organisation=user.agent.organisation)
            queryset = queryset.filter(Lead__agent__user=user)
        return queryset


