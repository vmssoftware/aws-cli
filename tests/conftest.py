import os

def pytest_addoption(parser):
    group = parser.getgroup('enable starting tests from a specified point')
    group.addoption('--start-from-file', dest='start-from-file', type=str,
                    help='The path to the file to start from')

def pytest_collection_modifyitems(session, config, items):
    start_from_file = config.getoption('start-from-file')
    if not start_from_file:
        return
    start_dir = os.path.dirname(start_from_file)
    start_file = os.path.basename(start_from_file)
    skip = 0
    for item in items:
        dir_name = os.path.dirname(item.location[0])
        if dir_name > start_dir:
            break
        if dir_name == start_dir:
            base_name = os.path.basename(item.location[0])
            if base_name >= start_file:
                break
        skip = skip + 1
    if skip:
        del items[:skip]
