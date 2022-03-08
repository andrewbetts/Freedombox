# SPDX-License-Identifier: AGPL-3.0-or-later
"""
Views for the Janus app.
"""

from django.views.generic import TemplateView

from plinth.modules import janus


class JanusRoomView(TemplateView):
    """A simple page to host Janus video room."""
    template_name = 'janus_video_room.html'

    def get_context_data(self, *args, **kwargs):
        """Add user's TURN server information to view context."""
        config = janus.app.get_component('turn-janus').get_configuration()
        context = super().get_context_data(*args, **kwargs)
        context['user_turn_config'] = config.to_json()
        return context
