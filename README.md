# pyspark-loglikelihood
PySpark Loglikelihood Examples.

Inspired by [Mahout](http://mahout.apache.org/):
* [LogLikelihood](https://github.com/apache/mahout/blob/master/math/src/main/java/org/apache/mahout/math/stats/LogLikelihood.java)
* [User / Item Similarity](https://github.com/apache/mahout/blob/master/mr/src/main/java/org/apache/mahout/cf/taste/impl/similarity/LogLikelihoodSimilarity.java)
* [Nearest N-Neighborhood](https://github.com/apache/mahout/blob/master/mr/src/main/java/org/apache/mahout/cf/taste/impl/neighborhood/NearestNUserNeighborhood.java) 


### Installation

```sh
$ pip install https://github.com/talmago/pyspark-loglikelihood/archive/master.zip
```

> **NOTICE:** PySpark Loglikelihood requires [python2.7](https://www.python.org/download/releases/2.7/) to run. We highly recommend to use [pyenv](https://github.com/yyuu/pyenv).


### Usage

After the installation you can `spark-submit-loglikelihood-sim`, a dedicated
command line run `spark-submit` with your loglikelihood similarity application.


#### Item-Item Similarity (LogLikelihood)

```sh
$ SPARK_HOME=/usr/lib/spark spark-submit-loglikelihood-sim \
                            item_similarity \
                            input.csv \
                            output.csv \
                            --maxPrefs=10000 \
                            --maxSimilaritiesPerItem 100
```
> **NOTICE:** Input file lines are expected to be a comma seperated vector of `USER_ID`,`ITEM_ID`. Output format will be consisted of `ITEM_ID1`,`ITEM_ID2`,`SCORE`, for each pair of items in the input file.


#### User-User Similarity (N-neighborhood + Loglikelihood)

```sh
$ SPARK_HOME=/usr/lib/spark spark-submit-loglikelihood-sim \
                            user_similarity \
                            input.csv \
                            output.csv \
                            --numOfNeighbors=40 \
                            --numOfRecommendations 1000
```
> **NOTICE:** Input file lines are expected to be a comma seperated vector of `USER_ID`,`ITEM_ID`. Output format will be consisted of `USER_ID`,`ITEM_ID`,`SCORE`.

### Example

##### Run [exmple](https://github.com/talmago/pyspark-loglikelihood/blob/master/examples/item-sim-ml-100l-dataset) from command line

```sh
wget -O - https://raw.githubusercontent.com/talmago/pyspark-loglikelihood/master/examples/item-sim-ml-100l-dataset | bash -x
```

##### Step by Step

Download and re-format the [movielens 100k](https://grouplens.org/datasets/movielens/100k/) dataset.

```sh
$ wget -O - http://files.grouplens.org/datasets/movielens/ml-100k/u.data | cut -f1 -f2 | tr '\t' ',' > input.csv
```

Upload data set to hadoop

```sh
$ hadoop fs -rm -r /item-sim
$ hadoop fs -mkdir -p /item-sim
$ hadoop fs -copyFromLocal input.csv /item-sim/input.csv
```

Run item silmilarity on hadoop data set

```sh
$ SPARK_HOME=/usr/lib/spark spark-submit-loglikelihood-sim \
                            item_similarity \
                            /item-sim/input.csv \
                            /item-sim/output \
                            --maxPrefs=10000 \
                            --maxSimilaritiesPerItem 100
```

Merge parquet files back to csv format

```sh
$ hadoop fs -getmerge /item-sim/output result.csv

$ head result.csv
26,381,0.9889748
26,732,0.9876871
26,70,0.98738647
26,715,0.98685825
26,238,0.98625606
26,58,0.98580784
26,1,0.985786
26,83,0.9857064
26,88,0.9856318
26,367,0.9854448
```
