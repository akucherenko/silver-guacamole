# Shortener service API

Flask-powered API app to create short URL redirects.

## Setup

Start service using `docker-compose`:

```shell script
docker-compose build
docker-compose up
```

## Usage

Creating a short link:

```shell script
curl \
  -H "Content-Type: application/json" \
  --data '{"url":"http://test.com"}' \
  http://127.0.0.1/api/short/
```

In response service returns something like:

```json
{
  "result": {
    "full_link": "http://localhost/BhBaZ",
    "short_code": "BhBaZ"
  }
}
```

To test newly created redirect:

```shell script
curl http://localhost/BhBaZ -v
```

If response it returns a redirect:

```
< HTTP/1.0 302 FOUND
< Content-Type: text/html; charset=utf-8
< Content-Length: 237
< Location: http://test.com
<
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>Redirecting...</title>
<h1>Redirecting...</h1>
<p>You should be redirected automatically to target URL: <a href="http://test.com">http://test.com</a>.  If not click the link.
```

The service also counts statistics per redirect invoked, but endpoint to retrieve this data is not implemented. Use DB query to check the data:

```shell script
docker exec -it short_db_1 psql shortener -U short -c "SELECT * FROM daily_stats LIMIT 10"
```
