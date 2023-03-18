# PandaToys

It's a flask starter project, like a toy. I'm trying to learn python in actions.

---

## Usage

1. create `.env` in root dir and put your environment in it, like:

   ```python
   # .env file
   Flask_APP=src:create_app()
   Flask_DEBUG=True
   SECRET_KEY='dev'
   DATABASE=os.path.join(app.instance_path, 'assistant.sqlite')
   ```

2. start project from shell:

   ```shell
   # install dependencies. you could install pytest with `pip install -e .[test]`
   pip install -e .

   # init db file
   flask init-db
   flask run
   ```
