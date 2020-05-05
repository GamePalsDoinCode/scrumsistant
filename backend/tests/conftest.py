def pytest_collection_modifyitems(items):
    for item in items:
        skip = [m for m in item.own_markers if m.name == 'not_async']
        if not skip:
            item.add_marker('asyncio')
