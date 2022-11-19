from rest_framework import permissions
from goals.models import BoardParticipant, Board, GoalCategory, Goal, GoalComment


class BoardPermissions(permissions.BasePermission):
    """Allows read/write access permission for the given Board instance.

    Attribute:
       message (str): Human readable string describing the denied permission.

    Returns:
        True if HTTP method is in ['GET', 'OPTIONS', 'HEAD'] and
        the current user is in board participants list, or the current user is in board participants list with the
        owner role for PUT, PATCH and DELETE methods. Otherwise, False.

    """
    message = "У Вас нет права редактирования или удаления данной доски"

    def has_object_permission(self, request, view, obj: Board) -> bool:

        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user, board=obj, role=BoardParticipant.Role.owner
        ).exists()


class CategoryPermissions(permissions.BasePermission):
    """Allows read/write access permission for the given GoalCategory instance.

    Attribute:
       message (str): Human readable string describing the denied permission.

    Returns:
        True if HTTP method is in ['GET', 'OPTIONS', 'HEAD'] and
        the current user is in board participants list, or the current user is in board participants list with the
        owner or writer role for PUT, PATCH and DELETE methods. False otherwise.

    """
    message = "У Вас нет права редактирования или удаления данной категории"

    def has_object_permission(self, request, view, obj: GoalCategory) -> bool:

        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj.board,
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user,
            board=obj.board,
            role__in=(BoardParticipant.Role.owner, BoardParticipant.Role.writer),
        ).exists()


class GoalPermissions(permissions.BasePermission):
    """Allows read/write access permission for the given Goal instance.

    Attribute:
       message (str): Human readable string describing the denied permission.

    Returns:
        True if HTTP method is in ['GET', 'OPTIONS', 'HEAD'] and
        the current user is in board participants list, or the current user is in board participants list with the
        owner or writer role for PUT, PATCH and DELETE methods. False otherwise.

    """
    message = "У Вас нет права редактирования или удаления данной цели"

    def has_object_permission(self, request, view, obj: Goal) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj.category.board
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user,
            board=obj.category.board,
            role__in=(BoardParticipant.Role.owner, BoardParticipant.Role.writer),
        ).exists()


class CommentsPermissions(permissions.BasePermission):
    """Allows read/write access permission for the given GoalComment instance.

    Attribute:
        message (str): Human readable string describing the denied permission.

    Returns:
        True if HTTP method is in ['GET', 'OPTIONS', 'HEAD'] and the current user is in board participants list,
        or the current user is in board participants list with any role and is the owner of the comment for PUT,
        PATCH and DELETE HTTP methods. False otherwise.

    """

    message = "У Вас нет права редактирования или удаления данного комментария"

    def has_object_permission(self, request, view, obj: GoalComment) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj.goal.category.board,
            ).exists()
        return request.user == obj.user or BoardParticipant.objects.filter(
            user=request.user,
            board=obj.goal.category.board,
            role__in=(BoardParticipant.Role.owner, BoardParticipant.Role.writer),
        ).exists()
