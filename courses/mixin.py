from django.contrib.auth.mixins import PermissionRequiredMixin


class CourseCreatePermissionMixin(PermissionRequiredMixin):
    permission_required = ["courses.add_course", ]


class CourseUpdatePermissionMixin(PermissionRequiredMixin):
    permission_required = ["courses.change_course", ]


class CourseDeletePermissionMixin(PermissionRequiredMixin):
    permission_required = ["courses.delete_course", ]


class CourseViewPermissionMixin(PermissionRequiredMixin):
    permission_required = ["courses.view_course", ]

    def get_permission_denied_message(self) -> str:
        message = "You are not allowed to view this page."

        return message


class LessonCreatePermissionMixin(PermissionRequiredMixin):
    permission_required = ["courses.add_lesson", ]


class LessonUpdatePermissionMixin(PermissionRequiredMixin):
    permission_required = ["courses.change_lesson", ]


class LessonDeletePermissionMixin(PermissionRequiredMixin):
    permission_required = ["courses.delete_lesson", ]


class LessonViewPermissionMixin(PermissionRequiredMixin):
    permission_required = ["courses.view_lesson", ]

    def get_permission_denied_message(self) -> str:
        message = "You are not allowed to view this page."

        return message
