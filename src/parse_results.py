from junitparser import JUnitXml

xml = JUnitXml.fromfile("./pytest-results.xml")
for suite in xml:
    for case in suite:
        if case.result and case.result[0].type == "failure":
            print(
                f"::error file={case.file},line={case.line}::{case.result[0].message}"
            )
