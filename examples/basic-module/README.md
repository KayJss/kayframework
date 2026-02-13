# Basic Module Example

After creating a project:

```bash
kay new app demo
cd demo
```

Create a module:

```bash
kay new module billing --app-dir app
```

Enable it in `.env`:

```env
MODULES=billing
```
