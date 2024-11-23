from django.http import HttpResponseForbidden


class CommonContextMixin:
    title = None

    def get_context_data(self, **kwargs):
        context = super(CommonContextMixin, self).get_context_data(**kwargs)
        context['title'] = self.title

        return context


class OwnershipRequiredMixin:
    forbidden_message = None

    def dispatch(self, request, *args, **kwargs):
        present = self.get_object()
        if present.user != request.user:
            return HttpResponseForbidden(self.forbidden_message)
        return super().dispatch(request, *args, **kwargs)
