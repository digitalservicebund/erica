import json

import click
from influxdb import InfluxDBClient

BATCH_SIZE = 500

import time
from contextlib import contextmanager
@contextmanager
def t(msg):
    tic = time.perf_counter()
    yield
    toc = time.perf_counter()
    print(f"{msg} took {toc-tic:0.4f}")


@click.command()
@click.argument('results_file', type=click.File())
@click.argument('influx_url')
def send(results_file, influx_url):
    client = InfluxDBClient.from_dsn(influx_url)

    batch = []
    for line in results_file:
        line_dict = json.loads(line)
        if line_dict["type"] != "Point":
            continue
        batch.append(dict(
            measurement=line_dict["metric"],
            tags=line_dict["data"]["tags"] or {},
            fields=dict(
                value=float(line_dict["data"]["value"]),
            ),
            time=line_dict["data"]["time"],
        ))
        if len(batch) >= BATCH_SIZE:
            client.write_points(batch)
            batch = []

    if len(batch) > 0:
        client.write_points(batch)


if __name__ == '__main__':
    send()
