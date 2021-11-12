# 4chan Leak RSS

Too much cool stuff leaks on that godawful website, so let's visit it as little as possible.

## Install
```bash
poetry install
# For the lazy...
python3 main.py 
# For the more upstanding
gunicorn 'fourchan_leak_rss:create_app()'
```

Steals code from:
- https://github.com/SuperSonicHub1/CRManga-RSS
- https://search4chan.org/
