# This returns the multiple matching logs like list of bidders
import logging


def get_logs(logs, matchByName, endIdentifier):
    find_all = lambda _str, _w: [i for i in range(len(_str)) if _str.startswith(_w, i)]
    indices = find_all(logs, matchByName)
    endPos = logs.find(endIdentifier)
    parts = [logs[i:j] for i, j in zip(indices, indices[1:] + [endPos - 1])]
    return parts


def subStringBetween(
    value: str, startToken: str, endToken: str, logWarningOnNotFound=False
):
    """It will return a substring between 2 tokens or empty if the tokens are not found"""

    indexFoundToken = value.find(startToken)
    if indexFoundToken != -1:
        currentValue = value[(indexFoundToken + len(startToken)) :]
        indexEndToken = currentValue.find(endToken)

        if indexEndToken != -1:
            return currentValue[0:indexEndToken]
        else:
            if logWarningOnNotFound:
                logging.warn(
                    "The end token["
                    + endToken
                    + "] was not found in the string "
                    + value
                )

        return ""
    else:
        if logWarningOnNotFound:
            logging.warn(
                "The start token["
                + startToken
                + "] was not found in the string "
                + value
            )

    return ""
