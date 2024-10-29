def athena_table(name, **others):
    """This should have the name of the table"""

    def _athena_table(func):
        func.meta_athena_table = {"name": name}
        func.meta_athena_table.update(others)
        return func

    return _athena_table
