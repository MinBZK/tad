from amt.api.deps import templates
from tests.constants import default_fastapi_request


def test_tempate_error():
    # given
    request = default_fastapi_request()

    # when
    response = templates.TemplateResponse(request, "error.html.j2")

    # then
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"
    assert b"This is an error message" in response.body
