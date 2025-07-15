import pprint


def pretty_print(title: str, data: any):
    """A centralized pretty-printer for debugging node inputs and outputs."""
    print(f"\n- - - [ {title} ] - - -")
    pprint.pprint(data)
    print(f"- - - {'-' * len(title)} - - -")
