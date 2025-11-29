import re
import logging

def resolve_placeholders(str: str, paths_map: dict[str,str], placeholder: str = "$") -> str:
    logger = logging.getLogger()
    logger.debug("Resolving placeholders on " + str)

    pattern = "\\{0}([^\\{0}]*)\\{0}".format(placeholder)
    logger.debug("Pattern: " + pattern)
    while m := re.search(pattern, str):
        logger.debug("Current string: " + str)
        logger.debug("Match found: " + m[0])
        try:
            str = str.replace(m[0], paths_map[m[1]])
        except KeyError as ke:
            logger.exception("No mapping for placeholder " + m[0])
            raise KeyError("No mapping for placeholder " + m[0]) from ke
        logger.debug("Placeholder replaced: " + str)
    return str