from app.middleware.permissions import require_permission
from astra_common.errors import AppError


class RequestState:
    user: dict


class FakeRequest:
    state = RequestState()


def test_admin_permission_allows():
    request = FakeRequest()
    request.state.user = {"permissions": ["*"]}
    require_permission(request, "strategy:create")


def test_missing_permission_rejected():
    request = FakeRequest()
    request.state.user = {"permissions": ["strategy:read"]}
    try:
        require_permission(request, "strategy:create")
    except AppError as exc:
        assert exc.code == "FORBIDDEN"
    else:
        raise AssertionError("permission should be rejected")


def test_market_data_permission_allows():
    request = FakeRequest()
    request.state.user = {"permissions": ["market_data:read"]}
    require_permission(request, "market_data:read")
