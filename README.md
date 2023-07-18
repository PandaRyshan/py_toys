# PandaToys

It's a flask starter project, like a toy. I'm trying to learn python in actions.

---

## Usage

1. create `.env` in root dir and put your environment in it, like:

   ```python
   # .env file
   FLASK_APP=src:create_app()
   FLASK_DEBUG=True
   SECRET_KEY='life-is-like-a-box-of-chocolates'
   # if you use sqlite3
   DATABASE=os.path.join(app.instance_path, 'db.sqlite')
   # if you use sqlalchemy
   SQLALCHEMY_DATABASE_URI=sqlite:///db.sqlite
   # MS Speech SDK
   MS_SPEECH_KEY='heres-looking-at-you-kid'
   MS_SPEECH_REGION='eastasia'
   ```

2. start project from shell:

   ```shell
   # install dependencies. you could install pytest with `pip install -e .[test]`
   pip install -e .

   # init db file, use --drop to drop all tables
   flask init-db
   flask run
   ```
