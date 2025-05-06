from typing import Final

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect
from django.shortcuts import render

from timetable.core.utils.parsing_exel import parsing_audience_exel
from timetable.core.utils.parsing_exel import parsing_teachers_exel
from timetable.core.utils.parsing_exel import parsing_timetable_exel

ALLOWED_INDEXES: Final = frozenset(
    ["Обновление расписания", "Обновление преподавателей", "Обновление аудиторий"],
)


@staff_member_required
def update_timetable_view(request):
    if request.method == "POST":
        update_type = request.POST.get("update_type")

        if update_type not in ALLOWED_INDEXES:
            messages.error(request, "Недопустимый тип обновления.")
            return redirect(request.path)

        # Находим соответствующий индекс и файл
        file_field = None
        for key, value in request.POST.items():
            if key.startswith("index_type_") and value == update_type:
                suffix = key.split("_")[-1]
                file_field = f"excel_{suffix}"
                break

        if not file_field or file_field not in request.FILES:
            messages.error(request, "Файл не найден.")
            return redirect(request.path)

        excel_file = request.FILES[file_field]

        try:
            if update_type == "Обновление расписания":
                parsing_timetable_exel(excel_file)
            elif update_type == "Обновление преподавателей":
                parsing_teachers_exel(excel_file)
            elif update_type == "Обновление аудиторий":
                parsing_audience_exel(excel_file)
            messages.success(request, f"{update_type} успешно завершено.")
        except Exception as e:  # noqa: BLE001
            messages.error(request, f"Ошибка при обработке файла: {e}")

        return redirect(request.path)

    return render(
        request,
        "admin/update_data/view_data.html",
        {"indexes": ALLOWED_INDEXES},
    )
