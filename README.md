# PandaToys

It's a flask starter project, like a toy. I'm trying to learn python in actions.

---

## Usage

1. create `.env` in root dir and put your environment in it:
 
   ```shell
   cd py_toys
   cp .env.template .env
   ```

2. start project from shell:

   ```shell
   # install dependencies. you could install pytest with `pip install -e .[test]`
   pip install -e .

   # init db file, use --drop to drop all tables
   flask init-db
   flask run
   ```
