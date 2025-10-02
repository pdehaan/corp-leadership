import json
import os
from datetime import date

import lib
from adobe import Adobe
from mozilla import Mozilla

COMPANIES = [Adobe, Mozilla]
TODAY = date.today().strftime("%Y-%m-%d")


def main():
    for Company in COMPANIES:
        c = Company()
        orgchart = c.get_leadership()
        orgchart_hash = lib.hash(orgchart)

        latest_company_file = lib.get_company_files(c.slug, 1)
        if latest_company_file:
            _, file_date, file_hash = lib.get_basename(str(latest_company_file)).split(
                "_", 3
            )

            if orgchart_hash == file_hash:
                # Found a matching hash, do nothing...
                return
            if file_date == TODAY:
                # We already have an existing file from today, delete it (because the hash doesn't match -- and two archives with the same day is chaos).
                os.remove(str(latest_company_file))

        filename = f"{c.slug}_{TODAY}_{orgchart_hash}.json"
        with open(lib.DATA_DIR / filename, "w") as fp:
            json.dump(orgchart, fp, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
