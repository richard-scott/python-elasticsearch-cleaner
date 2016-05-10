# python-elasticsearch-cleaner
Elasticsearch cleaner


## Example

### CLI

Clean all indices older that 30 days

```sh
python cleaner.py --host search-xxx.eu-west-1.es.amazonaws.com  --days 30
```

### Lambda


```sh
Change in cleaner-aws-lambda
 - c['host']
 - c['days']
Upload to AWS Lambda
Attach Scheduled event to the function
```
