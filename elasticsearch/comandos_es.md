# Comandos útiles para Elasticsearch

## Pipeline de Ingesta

```json
PUT _ingest/pipeline/tweet_pipeline
{
  "description": "Pipeline for indexing tweets",
  "processors": [
    {
      "set": {
        "field": "_index",
        "value": "tweets"
      }
    }
  ]
}
```

## Búsqueda en el índice

```json
GET /indice_tweets/_search
{
  "query":{
    "match_all" : {}
  }
}
```

## Estado del clúster

```json
GET /_cluster/health
```

## Búsqueda con formato

```json
GET /indice_tweets/_search?pretty
```

## Eliminación de índices

```json
DELETE /tweets
```

```json
DELETE /indice_tweets
```

## Creación de un nuevo índice con mappings

```json
PUT /indice_tweets
{
  "mappings": {
    "properties": {
      "raw": {
        "type": "text"
      },
      "label": {
        "type": "text"
      },
      "isa": {
        "type": "text"
      },
      "datelong": {
        "type": "text"
      },
      "flag": {
        "type": "text"
      },
      "user": {
        "type": "text"
      },
      "text": {
        "type": "text"
      },
      "day_short": {
        "type": "text"
      },
      "month_short": {
        "type": "text"
      },
      "day_long": {
        "type": "text"
      },
      "month_long": {
        "type": "text"
      },
      "day": {
        "type": "integer"
      },
      "month": {
        "type": "integer"
      },
      "year": {
        "type": "integer"
      },
      "time": {
        "type": "text"
      },
      "hour": {
        "type": "integer"
      },
      "minute": {
        "type": "integer"
      },
      "second": {
        "type": "integer"
      },
      "date": {
        "type": "date",
        "format": "yyyy-MM-dd"
      },
      "sentiment": {
        "type": "text"
      }
    }
  }
}