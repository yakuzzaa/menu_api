from fastapi import FastAPI

from views.menu import router as router_menu
from views.submenu import router as router_submenu
from views.dish import router as router_dish

app = FastAPI()
app.include_router(router_menu)
app.include_router(router_submenu)
app.include_router(router_dish)


