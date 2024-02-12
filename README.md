## Trip watcher bot

Simple lambda that monitors a few airline deals RSS feeds for particular destinations.

### Build

```bash
python3 -m venv trip-watch-env
source trip-watch-env/bin/activate
pip install --target ./package requests feedparser python-dateutil python-dotenv
```

Edit example.env, then `mv example.env .env`


### Deploy

use your AWS lamda id :) 

```bash
./deploy.sh
```
