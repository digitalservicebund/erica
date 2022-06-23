# 2. Replace RQ with Huey

Date: 2022-06-23

## Status

Accepted

## Context

We introduced RQ to separate the actual workload of sending information to ELSTER from the response of the API. However,
we realised that we run into problems using RQ and the ELSTER security stick. Because the security stick can always only
be used by one process but each RQ worker runs in its own process we need a task queue that allows us to run multiple
workes in the same process to make use of ERiC multithreading.

## Decision

We are going to replace RQ with [https://huey.readthedocs.io/en/latest/](huey).


## Consequences

It is now possible to run multiple workers in separate threads and they can use the ERiC multithreading. This should
make the execution of tasks faster. Furthermore, if two workers need access to the stick they do not run into problems.
However, huey is more low-level. Therefore, we will need to implement some parts ourselves that come with rq (e.g. huey
does not have a dead letter queue). Furthermore, huey works a little different. Huey provides a decorator and, whenever
the function is called, a task is created.