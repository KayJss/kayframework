from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from app.auth import models, schema, service
from app.core.dependencies import get_current_user, get_db
from app.core.security import Security

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def _wants_html(request: Request) -> bool:
    accept = request.headers.get("accept", "")
    return "text/html" in accept.lower()


@cbv(router)
class AuthCBV:
    db: Session = Depends(get_db)

    @router.post("/register", response_model=schema.UserOut)
    def register(self, user_in: schema.UserCreate):
        return service.create_user(self.db, user_in)

    @router.post("/login", response_model=schema.UserOut)
    def login(self, request: Request, response: Response, credentials: schema.UserLogin):
        user = service.authenticate_user(self.db, credentials)
        csrf_token = Security.create_csrf_token()
        access_token = Security.create_access_token(str(user.id), csrf_token)

        if _wants_html(request):
            template_response = templates.TemplateResponse(
                "profile.html",
                {"request": request, "user": user},
            )
            Security.set_auth_cookies(template_response, access_token, csrf_token)
            return template_response

        Security.set_auth_cookies(response, access_token, csrf_token)
        return user

    @router.get("/login")
    def login_page(self, request: Request):
        return templates.TemplateResponse("login.html", {"request": request})

    @router.get("/profile")
    def profile(self, request: Request, current_user: models.User = Depends(get_current_user)):
        return templates.TemplateResponse(
            "profile.html",
            {"request": request, "user": current_user},
        )

    @router.put("/profile", response_model=schema.UserOut)
    def update_profile(
        self,
        user_in: schema.UserUpdate,
        current_user: models.User = Depends(get_current_user),
    ):
        return service.update_profile(self.db, current_user, user_in)

    @router.get("/me", response_model=schema.UserOut)
    def get_my_info(self, current_user: models.User = Depends(get_current_user)):
        return current_user

    @router.put("/me", response_model=schema.UserOut)
    def update_me(
        self,
        user_in: schema.UserUpdate,
        current_user: models.User = Depends(get_current_user),
    ):
        return service.update_profile(self.db, current_user, user_in)

    @router.post("/me/password", response_model=schema.MessageOut)
    def change_password(
        self,
        data: schema.PasswordChange,
        current_user: models.User = Depends(get_current_user),
    ):
        return service.change_password(self.db, current_user, data)

    @router.get("/logout")
    def logout_get(self, request: Request, current_user: models.User = Depends(get_current_user)):
        if _wants_html(request):
            response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
            Security.clear_auth_cookies(response)
            return response
        response = Response()
        Security.clear_auth_cookies(response)
        return response

    @router.post("/logout", response_model=schema.MessageOut)
    def logout(self, response: Response, current_user: models.User = Depends(get_current_user)):
        return service.logout(response)
