def description(description_to_case, **others):
    """This should have a detailed description of our assumptions and expectations"""

    def _description(func):
        func.meta_description = {"description": description_to_case}
        func.meta_description.update(others)
        return func

    return _description
