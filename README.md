# lambda-cron
Run Cron Jobs via Python

* Kinesis invokes lambdas too often, make sure lambda deliver messages only once,

There are two cases where duplicates can happens in Kinesis,

1. Producer

- Here data producer may try to write the same message to Kinesis more than one, this is due to Kinesis network issue or producer couldn't get the success response. This can rarely happens and very low compared to consumer related duplicates

2. Consumer
..* There are 4 instances where record processor receive more than one
  * worker terminates unexpectedly
  * Worker instances are added or removed
  * Shards are merged or split
  * The application is deployed

In order to mitigate our consumer application should be robust and following two mechanism can be implemented,
  * Destination - We ignore the duplicate when we process messages from Kinesis, Here we assume that the destination application should handle the duplicates.
  * Source it self - handle the duplicates when we process message from Kinesis.

Therefore one solution would be,
..1. Record Processor uses a fixed number of records
..2. The file name uses this schema, app prefix, shard-id and First-Sequence-Num. In this case it could be like sample-shard000001-10001.
..3. Then you need to check this against some data source to see whether that message has been processed

Another solution would be,
  * Without doing any duplicate checking you write them to a database (dynamodb) and it triggers another lambda to filter duplicates.
