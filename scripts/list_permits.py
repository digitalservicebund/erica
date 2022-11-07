import os

import click

from erica.worker.jobs.list_permission_jobs import get_idnr_status_list_with_huey, get_idnr_status_list


@click.command()
@click.option('--idnr')
@click.option('--status', multiple=True)
@click.option('--start_date')
@click.option('--end_date')
@click.option('--show_xml')
@click.option('--use_huey')
def main(idnr=None, status=None, start_date=None, end_date=None, show_xml=False, use_huey=False):
    if use_huey:
        return get_idnr_status_list_with_huey(idnr, status, start_date, end_date, show_xml)
    return get_idnr_status_list(idnr, status, start_date, end_date, show_xml)


if __name__ == "__main__":
    os.chdir('../')  # Change the working directory to be able to find the eric binaries
    main()
