It's a flask starter project. Trying to learn python in actions.

---

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
   pip install -e .

   flask run
   ```

