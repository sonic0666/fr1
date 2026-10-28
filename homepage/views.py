from django.shortcuts import render

from db.database import get_connection
from db.queries import count_rows


def index(request):
    conn = get_connection()
    try:
        counts = count_rows(conn)
    finally:
        conn.close()

    context = {
        "counts": counts,
    }

    return render(
        request,
        "homepage/index.html",
        context,
    )


def page_not_found(request, exception):
    return render(
        request,
        "404.html",
        status=404,
    )
