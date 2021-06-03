from calendar import monthrange

from datetime import datetime
from datetime import timedelta

from os import makedirs
from os.path import abspath, exists

import config
import csv
import json
import xlsxwriter


def convert_to_date(value=''):
    try:
        return datetime.strptime(value, '%Y')
    except ValueError:
        try:
            return datetime.strptime(value, '%Y-%m')
        except ValueError:
            try:
                return datetime.strptime(value, config.DATE_FORMAT)
            except ValueError:
                msg = 'Not a valid date: ‘{0}’.'.format(value)
                raise ValueError(msg)


def convert_to_price(value):
    try:
        return int(value)

    except ValueError:
        try:
            return float(value)

        except ValueError:
            msg = 'Not a valid price: ‘{0}’.'.format(value)
            raise ValueError(msg)


def is_valid_export_type(value=''):
    if value not in ('csv', 'json', 'xlsx'):
        raise ValueError('We need a valid export type: csv, json or xlsx')
    return value


def format_date(date):
    if isinstance(date, datetime):
        return date.strftime(config.DATE_FORMAT)
    raise ValueError('We need a a valid datetime object')


def make_date():
    return datetime.today().strftime(config.DATE_FORMAT)


def make_filename(prefix='', suffix=''):
    return f'{prefix}{datetime.today().strftime(config.DATE_FORMAT_FILENAME)}{suffix}'


def filter_list(data=[], column='', keys=[]):
    if len(keys) == 0 or len(data) == 0:
        return []
    return list(filter(lambda row: row[column] in keys, data))


def filter_list_by_date(data=[], column='', date=''):
    if len(data) == 0:
        return []

    if not isinstance(date, datetime):
        raise ValueError('We need a valid datetime object')

    return [d for d in data if d[column] <= date]


def filter_list_by_date_range(data=[], column='', start='', end=''):
    if len(data) == 0:
        return []

    if not isinstance(start, datetime) or not isinstance(end, datetime):
        raise ValueError('We need a valid datetime object')

    return [d for d in data if d[column] >= start and d[column] <= end]


def sort_list(data=[], column=''):
    if len(data) == 0:
        return []
    if len(data) == 1:
        return data
    return sorted(data, key=lambda key: key[column])


def last_day_of_month(date=''):
    if not isinstance(date, datetime):
        raise ValueError('We need a valid datetime object')

    year = int(date.strftime('%Y'))
    month = int(date.strftime('%m'))
    day = monthrange(year, month)[1]

    return datetime(year, month, day)


def last_day_of_year(date=''):
    if not isinstance(date, datetime):
        raise ValueError('We need a valid datetime object')

    year = int(date.strftime('%Y'))

    return datetime(year, 12, 31)


def format_currency(value=0):
    return '€ {:,.2f} '.format(float(value))


def date_as_string(date=''):
    if not isinstance(date, datetime):
        raise ValueError('We need a valid datetime object')


def export_csv(filename, fieldnames, data):
    directory = config.EXPORTS_DIR
    make_missing_dir(directory)
    filepath = abspath(f'./{directory}/{filename}')
    create_csv_file(filepath, fieldnames, data)


def export_xlsx(filename, fieldnames, data):
    directory = config.EXPORTS_DIR
    make_missing_dir(directory)
    filepath = abspath(f'./{directory}/{filename}')
    create_xlsx_file(filepath, fieldnames, data)


def export_json(filename, data):
    directory = config.EXPORTS_DIR
    make_missing_dir(directory)
    filepath = abspath(f'./{directory}/{filename}')
    create_json_file(filepath, data)


def report_csv(filename, fieldnames, data):
    directory = config.REPORTS_DIR
    make_missing_dir(directory)
    filepath = abspath(f'./{directory}/{filename}')
    create_csv_file(filepath, fieldnames, data)


def report_xlsx(filename, fieldnames, data):
    directory = config.REPORTS_DIR
    make_missing_dir(directory)
    filepath = abspath(f'./{directory}/{filename}')
    create_xlsx_file(filepath, fieldnames, data)


def report_json(filename, data):
    directory = config.REPORTS_DIR
    make_missing_dir(directory)
    filepath = abspath(f'./{directory}/{filename}')
    create_json_file(filepath, data)


def create_csv_file(filepath, fieldnames, data):
    with open(filepath, mode='w+') as f:
        file_ref = csv.DictWriter(
            f, fieldnames=fieldnames, delimiter=',', doublequote=True, escapechar='\\',
            lineterminator='\r\n', quotechar='"', quoting=csv.QUOTE_MINIMAL, skipinitialspace=True,
            strict=True)
        file_ref.writeheader()
        for row in data:
            file_ref.writerow(row)


def create_xlsx_file(filepath, headers, data):
    with xlsxwriter.Workbook(filepath) as w:
        worksheet = w.add_worksheet()
        worksheet.write_row(row=0, col=0, data=headers)
        for index, item in enumerate(data):
            row = map(lambda field_id: item.get(field_id, ''), headers)
            worksheet.write_row(row=index + 1, col=0, data=row)


def create_json_file(filepath, data):
    with open(filepath, 'w+') as j:
        json.dump(data, j, sort_keys=True, indent=4, ensure_ascii=False)


def make_missing_dir(dir: str = ''):
    if dir == '':
        raise ValueError('We need a valid directory name')
    try:
        if not exists(abspath(f'./{dir}')):
            makedirs(abspath(f'./{dir}'))
    except:
        raise OSError(f'We require a ./{dir} directory')


def main():
    pass


if __name__ == '__main__':
    main()
