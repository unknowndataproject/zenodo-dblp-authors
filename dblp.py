import sqlite3

con_orcid = sqlite3.connect("./orcid.db")

def is_dblp_orcid(orcid: str) -> bool:

    orcid_query_result = con_orcid.execute("SELECT pid FROM orcid WHERE orcid=?", (orcid,)).fetchone()

    if orcid_query_result is None:
        return False
    else:
        return True