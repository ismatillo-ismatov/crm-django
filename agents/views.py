from django.shortcuts import render
from django.core.mail import send_mail
from django.views import generic
from django.shortcuts import reverse
from django.urls import reverse_lazy
from app.models import Agent,UserProfile
from .forms import AgentModelForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import OrganisorAndLoginMixin
import random
from django.contrib import messages
class AgentListView(OrganisorAndLoginMixin,generic.ListView):
    template_name = "agents/agent_list.html"
#
    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentCreateView(OrganisorAndLoginMixin,generic.CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")


    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organisor = False
        user.set_password(f"{random.randint(0,1000000)}")
        user.save()
        Agent.objects.create(
            user=user,
            organisation=self.request.user.userprofile,

        )
        send_mail(
            subject="You are Invited to be agent",
            message="You were added as an agent on DJCRM. please come login to start working",
            from_email="ismatilloismatov@gmail.com",
            recipient_list=[user.email]
        )
        return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(OrganisorAndLoginMixin,generic.DetailView):
    template_name = "agents/agent_detail.html"
    context_object_name = "agent"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

class AgentUpdateView(OrganisorAndLoginMixin,generic.UpdateView):
    template_name = "agents/agent_update.html"
    form_class = AgentModelForm
    def get_success_url(self):
        return reverse("agents:agent-list")
    def get_queryset(self):
        user = self.request.user
        return Agent.objects.filter(organisation=user.userprofile)


    # def form_valid(self, form):
    #     form.save()
    #     messages.info(self.request, "update agent")
    #     return super(AgentUpdateView,self).form_valid(form)



class AgentDeleteView(OrganisorAndLoginMixin,generic.DeleteView):
    template_name = "agents/agent_delete.html"
    queryset = Agent.objects.all()
    def get_success_url(self):
        return reverse('agents:agent-list')

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)