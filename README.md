# Django Multi-app

It means that we launch one main Django engine on server with database, but app has several independent entrypoins with different UI stacks.

This repo is marketplace app example, like Amazon. This app has several entrypoints:
- seller section `/seller`. UI: Bootstrap 5. Only users with Seller profile are allowed.
- admin section, `/admin`. UI: default Django admin site. Only users with `is_staff=True` are allowed.
- public app, `/*`. UI: TailwindCSS. Any authorized or anonymous user.

## Structure

- `app` - main module with global settings.
- `core, retail` - shared modules for all parts
- `public_app/assets, public_app/templates` - frontend part of `public_app`, namespaced with `public`
- `public_app/index` - first Django app of `public_app` namespace, can be several, as usual Django project.
- same for `seller_app`

Advantages:
- Separation of core domain logic from modules with UI part. Core modules don't have forms, views and templates, only models, storages and business-logic.
- Each entrypoint have own scope.
    - It imports core models and defines it's own.
    - May have own UI stack, or include base layouts from another app.

## Demo

```bash
# install public_app frontend deps
cd public_app/assets/public
npm i
cd ../../../

# install seller_app frontend deps
cd seller_app/assets/seller
npm i
cd ../../../

# install python deps
poetry install
poetry shell
# run django
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```

Open `http://localhost:8000/`, `http://localhost:8000/admin`, `http://localhost:8000/seller` and try to create create new user and attach Shop or Partner profile to it.
