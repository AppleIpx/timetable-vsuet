from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from timetable.search.service import ALLOWED_INDEXES
from timetable.search.service import CommandType
from timetable.search.service import OpensearchCommandExecutor


@staff_member_required
def rebuild_opensearch_view(request):
    if request.method == "POST":
        command_type = CommandType.index if CommandType.index.value in request.POST else CommandType.document
        index = request.POST[command_type.value]
        command_executor = OpensearchCommandExecutor()
        message = command_executor(command_type, index)

        return render(
            request,
            "admin/opensearch/rebuild_result.html",
            {"message": message},
        )

    return render(
        request,
        "admin/opensearch/rebuild_opensearch.html",
        {"indexes": ALLOWED_INDEXES},
    )
