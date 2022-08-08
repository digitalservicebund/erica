from invoke import task


@task
def test_integration_queue(c):
    c.run("pytest ./contract_tests/test_integration_queue.py")


@task
def test(c):
    c.run("pytest -n 3")


@task
def lint(c):
    # fail the build if there are Python syntax errors or undefined names
    c.run("flake8 . --count --select=E9,E112,E113,E117,E711,E713,E714,F63,F7,F82 --show-source --statistics")
    # exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
    c.run("flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics")

@task
def database_migrations(c):
    c.run("alembic upgrade head")

@task
def run_api(c):
    c.run("python -m erica")

@task
def run_worker(c, number_of_workers=10):
    c.run(f"huey_consumer.py erica.worker.huey.huey -k thread -w {number_of_workers}")

@task
def download_eric(c):
    c.run("python scripts/load_eric_binaries.py download-eric-cert-and-binaries", pty=True)
