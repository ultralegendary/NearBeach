from django.core.exceptions import PermissionDenied
from django.db.models import Q, Max
from functools import wraps

from NearBeach.models import UserGroup, Group, ObjectAssignment, KanbanCard,\
    RequirementItem, Requirement, ChangeTask


def check_change_task_permissions(min_permission_level):
    """Check the user's ability to interact with change tasks via the RFC"""

    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            # If user is admin - grant them all permission
            if request.user.is_superuser:
                # Return the function with a user_level of 4
                return func(request, *args, **kwargs, user_level=4)

            # Default user level is 0
            user_group_results = UserGroup.objects.filter(
                is_deleted=False,
                username=request.user,
            )

            # If we are passing in any args like change_task_id, we want to do the following
            if len(kwargs) > 0:
                # Get the rfc id
                rfc_id = ChangeTask.objects.get(
                    change_task_id=kwargs["change_task_id"]
                ).request_for_change_id

                # Determine if there are any cross over change tasks
                group_results = Group.objects.filter(
                    Q(
                        is_deleted=False,
                        # The object_lookup groups
                        group_id__in=ObjectAssignment.objects.filter(
                            is_deleted=False,
                            # **{object_lookup: kwargs[object_lookup]},
                            request_for_change_id=rfc_id,
                        ).values("group_id"),
                    )
                    & Q(group_id__in=user_group_results.values("group_id"))
                )

                # Check to make sure the user groups intersect
                if len(group_results) == 0:
                    # There are no matching groups - i.e. the user does not have any permission
                    raise PermissionDenied

            # Get the max permission value from user_group_results
            user_level = user_group_results.aggregate(
                Max("permission_set__request_for_change")
            )["permission_set__request_for_change__max"]

            if user_level >= min_permission_level:
                # Everything is fine - continue on
                return func(request, *args, **kwargs, user_level=user_level)

            # Does not meet conditions
            raise PermissionDenied

        return inner

    return decorator


def check_user_customer_permissions(min_permission_level):
    """
    Function is only used when checking user permissions against customers
     - as they are different
    """

    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            # if user is admin -grant them all permissions
            if request.user.is_superuser:
                # Return the function with a user_level of 4
                return func(request, *args, **kwargs, user_level=4)

            # Default user level is 0
            user_group_results = UserGroup.objects.filter(
                is_deleted=False,
                username=request.user,
            )

            # Get the max permission value from user_group_results
            user_level = user_group_results.aggregate(Max("permission_set__customer"))[
                "permission_set__customer__max"
            ]

            if user_level >= min_permission_level:
                # Everything is fine - continue on
                return func(request, *args, **kwargs, user_level=user_level)

            # Does not meet conditions
            raise PermissionDenied

        return inner

    return decorator


def check_user_kanban_permissions(min_permission_level):
    def decorator(func):
        @wraps(func)
        def inner(request, kanban_card_id, *args, **kwargs):
            # If user is admin - grant them all permissions
            if request.user.is_superuser:
                # Return the function with a user_level of 4
                return func(request, kanban_card_id, *args, **kwargs, user_level=4)

            # Default user level is 0
            user_group_results = UserGroup.objects.filter(
                is_deleted=False,
                username=request.user,
            )

            # Determine if there are any cross over with user groups and object_lookup groups
            group_results = Group.objects.filter(
                Q(
                    is_deleted=False,
                    # The object_lookup groups
                    group_id__in=ObjectAssignment.objects.filter(
                        is_deleted=False,
                        kanban_board_id__in=KanbanCard.objects.filter(
                            kanban_card_id=kanban_card_id,
                        ).values("kanban_board_id"),
                    ).values("group_id"),
                )
                & Q(group_id__in=user_group_results.values("group_id"))
            )

            # Check to make sure the user groups intersect
            if len(group_results) == 0:
                # There are no matching groups - i.e. the user does not have any permission
                raise PermissionDenied

            # Get the max permission value from user_group_results
            user_level = user_group_results.aggregate(
                Max("permission_set__kanban_board")
            )["permission_set__kanban_board__max"]

            if user_level >= min_permission_level:
                # Everything is fine - continue on
                return func(
                    request, kanban_card_id, *args, **kwargs, user_level=user_level
                )

            # Does not meet conditions
            raise PermissionDenied

        return inner

    return decorator


def check_user_organisation_permissions(min_permission_level):
    """
    Function is only used when checking user permissions against
    customers - as they are different
    """

    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            # if user is admin -grant them all permissions
            if request.user.is_superuser:
                # Return the function with a user_level of 4
                return func(request, *args, **kwargs, user_level=4)

            # Default user level is 0
            user_group_results = UserGroup.objects.filter(
                is_deleted=False,
                username=request.user,
            )

            # Get the max permission value from user_group_results
            user_level = user_group_results.aggregate(
                Max("permission_set__organisation")
            )["permission_set__organisation__max"]

            if user_level >= min_permission_level:
                # Everything is fine - continue on
                return func(request, *args, **kwargs, user_level=user_level)

            # Does not meet conditions
            raise PermissionDenied

        return inner

    return decorator


def check_user_permissions(min_permission_level, object_lookup=""):
    """
    Check the user permissions - if they pass they can implement the function.
    Otherwise send them to the permission denied page
    """

    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            # If user is admin - grant them all permissions
            if request.user.is_superuser:
                # Return the function with a user_level of 4
                return func(request, *args, **kwargs, user_level=4)

            # Default user level is 0
            user_group_results = UserGroup.objects.filter(
                is_deleted=False,
                username=request.user,
            )

            # If we are passing the object_lookup through, we will use a different function
            if len(kwargs) > 0:
                # Determine if there are any cross over with user groups and object_lookup groups
                group_results = Group.objects.filter(
                    Q(
                        is_deleted=False,
                        # The object_lookup groups
                        group_id__in=ObjectAssignment.objects.filter(
                            is_deleted=False,
                            **{object_lookup: kwargs[object_lookup]},
                        ).values("group_id"),
                    )
                    & Q(group_id__in=user_group_results.values("group_id"))
                )

                # Check to make sure the user groups intersect
                if len(group_results) == 0:
                    # There are no matching groups - i.e. the user does not have any permission
                    raise PermissionDenied

            # Get the max permission value from user_group_results
            user_level = user_group_results.aggregate(
                Max(f"permission_set__{object_lookup.replace('_id', '')}")
            )[f"permission_set__{object_lookup.replace('_id', '')}__max"]

            if user_level >= min_permission_level:
                # Everything is fine - continue on
                return func(request, *args, **kwargs, user_level=user_level)

            # Does not meet conditions
            raise PermissionDenied

        return inner

    return decorator


def check_user_requirement_item_permissions(min_permission_level):
    """
    Function is only used when checking user permissions against
    customers - as they are different
    """

    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            # if user is admin -grant them all permissions
            if request.user.is_superuser:
                # Return the function with a user_level of 4
                return func(request, *args, **kwargs, user_level=4)

            # Get the requirement_item instance
            requirement_item_results = RequirementItem.objects.get(
                **{"requirement_item_id": kwargs["requirement_item_id"]},
            )

            # Get the requirement instance
            requirement_results = Requirement.objects.get(
                requirement_id=requirement_item_results.requirement_id,
            )

            # Get the requirement groups
            user_group_results = UserGroup.objects.filter(
                Q(
                    is_deleted=False,
                    group_id__in=ObjectAssignment.objects.filter(
                        is_deleted=False,
                        group_id__isnull=False,
                        requirement_id=requirement_results.requirement_id,
                    ).values("group_id"),
                )
                & Q(
                    username=request.user,
                )
            )

            # Get the max permission value from user_group_results
            user_level = user_group_results.aggregate(
                Max("permission_set__requirement")
            )["permission_set__requirement__max"]

            if user_level >= min_permission_level:
                # Everything is fine - continue on
                return func(request, *args, **kwargs, user_level=user_level)

            # Does not meet conditions
            raise PermissionDenied

        return inner

    return decorator


def check_rfc_permissions(min_permission_level):
    """Check the user's RFC permissions"""

    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            # If user is admin - grant them all permissions
            if request.user.is_superuser:
                # Return the function with a user_level of 4
                return func(request, *args, **kwargs, user_level=4)

            # Default user level is 0
            user_group_results = UserGroup.objects.filter(
                is_deleted=False,
                username=request.user,
            )

            # If we are passing the object_lookup through, we will use a different function
            if len(kwargs) > 0:
                # Determine if there are any cross over with user groups and object_lookup groups
                group_results = Group.objects.filter(
                    Q(
                        is_deleted=False,
                        # The object_lookup groups
                        group_id__in=ObjectAssignment.objects.filter(
                            is_deleted=False,
                            # **{object_lookup: kwargs[object_lookup]},
                            request_for_change_id=kwargs["rfc_id"],
                        ).values("group_id"),
                    )
                    & Q(group_id__in=user_group_results.values("group_id"))
                )

                # Check to make sure the user groups intersect
                if len(group_results) == 0:
                    # There are no matching groups - i.e. the user does not have any permission
                    raise PermissionDenied

            # Get the max permission value from user_group_results
            user_level = user_group_results.aggregate(
                Max("permission_set__request_for_change")
            )["permission_set__request_for_change__max"]

            if user_level >= min_permission_level:
                # Everything is fine - continue on
                return func(request, *args, **kwargs, user_level=user_level)

            # Does not meet conditions
            raise PermissionDenied

        return inner

    return decorator


def check_permission_denied():
    """Just a test function - don't worry about it"""

    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            # Does not meet conditions
            raise PermissionDenied

        return inner

    return decorator
