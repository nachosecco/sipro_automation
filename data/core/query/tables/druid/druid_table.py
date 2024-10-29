def druid_table(name, **others):
    """This should have the name of the table"""

    def _druid_table(func):
        func.meta_druid_table = {"name": name}
        func.meta_druid_table.update(others)
        return func

    return _druid_table
