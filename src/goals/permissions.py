from rest_framework import permissions
from goals.models import BoardParticipant


class BoardPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user, board=obj, role=BoardParticipant.Role.owner
        ).exists()


class CategoryPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board__categories__in=(obj,)
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user,
            board__categories__in=(obj,),
            role__in=(BoardParticipant.Role.owner, BoardParticipant.Role.writer),
        ).exists()


class GoalPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board__categories__goals__in=(obj,)
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user,
            board__categories__goals__in=(obj,),
            role__in=(BoardParticipant.Role.owner, BoardParticipant.Role.writer),
        ).exists()


class CommentsPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board__categories__goals__in=(obj.goal,)
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user,
            board__categories__goals__in=(obj.goal,),
            role__in=(BoardParticipant.Role.owner, BoardParticipant.Role.writer),
        ).exists()
