from typing import Any

from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'wishlists/index.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)

        context['title'] = 'Wheesh'
        return context
