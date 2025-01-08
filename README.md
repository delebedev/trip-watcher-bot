## Trip watcher bot

Stateless lambda that monitors a few airline deals RSS feeds for particular destinations.

### Build and run

Setup the environment:

```bash
cp example.env .env
```

```bash
pipenv install
pipenv shell
python trip_watcher_bot.py
```

### Deploy

use your AWS lamda id :)

```bash
./deploy.sh
```
