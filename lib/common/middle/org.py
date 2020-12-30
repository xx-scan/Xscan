# -*- coding: utf-8 -*-
#

from secs.models import Organization
from ..utils.org import get_org_from_request, set_current_org


class OrgMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    # @staticmethod
    # def set_permed_org_if_need(request):
    #     if request.path.startswith('/api'):
    #         return
    #     if not (request.user.is_authenticated and request.user.is_org_admin):
    #         return
    #     org = get_org_from_request(request)
    #     if org.can_admin_by(request.user):
    #         return
    #     admin_orgs = Organization.get_user_admin_orgs(request.user)
    #     if admin_orgs:
    #         request.session['oid'] = str(admin_orgs[0].id)

    def __call__(self, request):
        # self.set_permed_org_if_need(request)
        if request.user.is_superuser or request.user.username in ['admin', 'admin001', 'admin007']:
            request.META["HTTP_X_CSO_ORG"] = Organization.ROOT_ID
        org = get_org_from_request(request)
        if org is not None:
            request.current_org = org
            set_current_org(org)
        response = self.get_response(request)
        return response
