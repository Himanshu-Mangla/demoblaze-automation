import json
from pathlib import Path
from datetime import datetime
from html import escape


class DailyQAReport:

    def __init__(
        self,
        report_dir,
        allure_results_dir,
        environment="QA",
        browser="Chromium"
    ):
        self.report_dir = Path(report_dir)
        self.allure_results_dir = Path(allure_results_dir)
        self.environment = environment
        self.browser = browser

        self.report_path = (
            self.report_dir /
            "daily-qa-report.html"
        )

        self.test_results = []


    # ========================================================
    # READ ALLURE RESULTS
    # ========================================================

    def read_allure_results(self):

        result_files = list(
            self.allure_results_dir.glob(
                "*-result.json"
            )
        )

        print(
            f"Allure Result Files Found: "
            f"{len(result_files)}"
        )

        for result_file in result_files:

            try:

                with open(
                    result_file,
                    "r",
                    encoding="utf-8"
                ) as file:

                    result = json.load(file)


                # ------------------------------------------------
                # TEST CASE ID
                # ------------------------------------------------

                test_id = "N/A"

                for label in result.get(
                    "labels",
                    []
                ):

                    label_name = label.get(
                        "name"
                    )

                    label_value = label.get(
                        "value",
                        ""
                    )

                    if (
                        label_name == "tag"
                        and label_value.startswith("TC_")
                    ):

                        test_id = label_value

                        break


                # ------------------------------------------------
                # DESCRIPTION
                # ------------------------------------------------

                description = result.get(
                    "name",
                    "Unknown Test"
                )


                # ------------------------------------------------
                # STATUS
                # ------------------------------------------------

                allure_status = result.get(
                    "status",
                    "unknown"
                )

                if allure_status == "passed":

                    status = "PASSED"

                elif allure_status == "failed":

                    status = "FAILED"

                elif allure_status in [
                    "skipped",
                    "pending"
                ]:

                    status = "SKIPPED"

                else:

                    status = allure_status.upper()


                # ------------------------------------------------
                # STORE RESULT
                # ------------------------------------------------

                self.test_results.append(
                    {
                        "test_id": test_id,
                        "description": description,
                        "status": status
                    }
                )


            except Exception as error:

                print()
                print(
                    "ERROR READING ALLURE RESULT:"
                )

                print(
                    f"File: {result_file}"
                )

                print(
                    f"Error: {error}"
                )

                print()


        # --------------------------------------------------------
        # SORT BY TEST CASE ID
        # --------------------------------------------------------

        self.test_results.sort(
            key=lambda test:
            test["test_id"]
        )


    # ========================================================
    # CALCULATE SUMMARY
    # ========================================================

    def calculate_summary(self):

        total = len(
            self.test_results
        )

        passed = sum(
            1
            for test in self.test_results
            if test["status"] == "PASSED"
        )

        failed = sum(
            1
            for test in self.test_results
            if test["status"] == "FAILED"
        )

        skipped = sum(
            1
            for test in self.test_results
            if test["status"] == "SKIPPED"
        )

        pass_percentage = (

            round(
                (passed / total) * 100,
                2
            )

            if total > 0

            else 0
        )

        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "pass_percentage": pass_percentage
        }


    # ========================================================
    # GENERATE TABLE ROWS
    # ========================================================

    def generate_table_rows(self):

        rows = ""

        for test in self.test_results:

            test_id = escape(
                test["test_id"]
            )

            description = escape(
                test["description"]
            )

            status = test["status"]


            if status == "PASSED":

                status_class = "passed"

                status_text = "PASS"


            elif status == "FAILED":

                status_class = "failed"

                status_text = "FAIL"


            elif status == "SKIPPED":

                status_class = "skipped"

                status_text = "SKIPPED"


            else:

                status_class = "unknown"

                status_text = status


            rows += f"""

            <tr>

                <td class="test-id">
                    {test_id}
                </td>

                <td class="description">
                    {description}
                </td>

                <td>

                    <span
                        class="status {status_class}"
                    >
                        {status_text}
                    </span>

                </td>

            </tr>

            """


        if not rows:

            rows = """

            <tr>

                <td
                    colspan="3"
                    class="no-results"
                >
                    No test results found.
                </td>

            </tr>

            """


        return rows


    # ========================================================
    # GENERATE HTML
    # ========================================================

    def generate_html(self):

        summary = self.calculate_summary()

        total = summary["total"]

        passed = summary["passed"]

        failed = summary["failed"]

        skipped = summary["skipped"]

        pass_percentage = (
            summary["pass_percentage"]
        )

        execution_date = (
            datetime.now().strftime(
                "%d-%b-%Y"
            )
        )

        execution_time = (
            datetime.now().strftime(
                "%I:%M:%S %p"
            )
        )

        table_rows = (
            self.generate_table_rows()
        )


        html = f"""

<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width,
             initial-scale=1.0"
>

<title>
    Daily QA Test Execution Report
</title>


<style>


* {{
    box-sizing: border-box;
}}


body {{

    margin: 0;

    padding: 0;

    font-family:
        "Segoe UI",
        Arial,
        sans-serif;

    background: #f4f6f8;

    color: #263238;

}}


.container {{

    width: 92%;

    max-width: 1250px;

    margin: 35px auto;

}}


/* ========================================================
   HEADER
   ======================================================== */


.header {{

    background: #ffffff;

    padding: 28px 32px;

    border-radius: 10px;

    box-shadow:
        0 2px 8px
        rgba(0, 0, 0, 0.08);

    margin-bottom: 20px;

}}


.header h1 {{

    margin: 0;

    font-size: 28px;

    font-weight: 600;

    color: #263238;

}}


.header p {{

    margin: 8px 0 0;

    font-size: 14px;

    color: #78909c;

}}


/* ========================================================
   EXECUTION INFORMATION
   ======================================================== */


.info-grid {{

    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap: 16px;

    margin-bottom: 20px;

}}


.info-card {{

    background: #ffffff;

    padding: 20px;

    border-radius: 10px;

    box-shadow:
        0 2px 8px
        rgba(0, 0, 0, 0.06);

}}


.info-title {{

    font-size: 12px;

    text-transform: uppercase;

    color: #90a4ae;

    margin-bottom: 8px;

}}


.info-value {{

    font-size: 18px;

    font-weight: 600;

    color: #37474f;

}}


/* ========================================================
   SUMMARY
   ======================================================== */


.summary {{

    background: #ffffff;

    padding: 24px;

    border-radius: 10px;

    margin-bottom: 20px;

    box-shadow:
        0 2px 8px
        rgba(0, 0, 0, 0.06);

}}


.summary h2 {{

    margin: 0 0 20px;

    font-size: 20px;

    color: #37474f;

}}


.summary-grid {{

    display: grid;

    grid-template-columns:
        repeat(5, 1fr);

    gap: 14px;

}}


.summary-card {{

    background: #f8fafb;

    padding: 20px;

    border-radius: 8px;

    text-align: center;

}}


.summary-number {{

    font-size: 28px;

    font-weight: 700;

}}


.summary-label {{

    margin-top: 6px;

    font-size: 13px;

    color: #78909c;

}}


.total {{

    color: #37474f;

}}


.pass {{

    color: #2e7d32;

}}


.fail {{

    color: #c62828;

}}


.skip {{

    color: #ef6c00;

}}


/* ========================================================
   TEST TABLE
   ======================================================== */


.test-section {{

    background: #ffffff;

    padding: 24px;

    border-radius: 10px;

    box-shadow:
        0 2px 8px
        rgba(0, 0, 0, 0.06);

}}


.test-section h2 {{

    margin: 0;

    font-size: 20px;

    color: #37474f;

}}


table {{

    width: 100%;

    border-collapse: collapse;

    margin-top: 18px;

}}


thead {{

    background: #f1f3f5;

}}


th {{

    text-align: left;

    padding: 15px;

    font-size: 13px;

    font-weight: 600;

    color: #546e7a;

    border-bottom:
        1px solid #e0e0e0;

}}


td {{

    padding: 15px;

    font-size: 14px;

    border-bottom:
        1px solid #eeeeee;

}}


tbody tr:hover {{

    background: #fafafa;

}}


.test-id {{

    width: 190px;

    font-weight: 600;

    color: #37474f;

}}


.description {{

    width: 60%;

    color: #455a64;

}}


/* ========================================================
   STATUS
   ======================================================== */


.status {{

    display: inline-block;

    min-width: 75px;

    padding: 6px 12px;

    border-radius: 20px;

    text-align: center;

    font-size: 12px;

    font-weight: 700;

}}


.status.passed {{

    background: #e8f5e9;

    color: #2e7d32;

}}


.status.failed {{

    background: #ffebee;

    color: #c62828;

}}


.status.skipped {{

    background: #fff3e0;

    color: #ef6c00;

}}


.status.unknown {{

    background: #eceff1;

    color: #546e7a;

}}


.no-results {{

    text-align: center;

    padding: 35px;

    color: #90a4ae;

}}


/* ========================================================
   FOOTER
   ======================================================== */


.footer {{

    text-align: center;

    margin-top: 25px;

    font-size: 12px;

    color: #90a4ae;

}}


/* ========================================================
   RESPONSIVE
   ======================================================== */


@media(max-width: 800px) {{

    .container {{

        width: 95%;

    }}

    .info-grid {{

        grid-template-columns: 1fr;

    }}

    .summary-grid {{

        grid-template-columns:
            repeat(2, 1fr);

    }}

}}


</style>

</head>


<body>


<div class="container">


    <!-- =================================================
         HEADER
         ================================================= -->


    <div class="header">

        <h1>
            Daily QA Test Execution
        </h1>

        <p>
            Automated Test Execution Summary
        </p>

    </div>


    <!-- =================================================
         EXECUTION INFORMATION
         ================================================= -->


    <div class="info-grid">


        <div class="info-card">

            <div class="info-title">
                Execution Date
            </div>

            <div class="info-value">
                {execution_date}
            </div>

        </div>


        <div class="info-card">

            <div class="info-title">
                Environment
            </div>

            <div class="info-value">
                {escape(self.environment)}
            </div>

        </div>


        <div class="info-card">

            <div class="info-title">
                Browser
            </div>

            <div class="info-value">
                {escape(self.browser)}
            </div>

        </div>


    </div>


    <!-- =================================================
         SUMMARY
         ================================================= -->


    <div class="summary">

        <h2>
            Execution Summary
        </h2>


        <div class="summary-grid">


            <div class="summary-card">

                <div class="summary-number total">
                    {total}
                </div>

                <div class="summary-label">
                    Total
                </div>

            </div>


            <div class="summary-card">

                <div class="summary-number pass">
                    {passed}
                </div>

                <div class="summary-label">
                    Passed
                </div>

            </div>


            <div class="summary-card">

                <div class="summary-number fail">
                    {failed}
                </div>

                <div class="summary-label">
                    Failed
                </div>

            </div>


            <div class="summary-card">

                <div class="summary-number skip">
                    {skipped}
                </div>

                <div class="summary-label">
                    Skipped
                </div>

            </div>


            <div class="summary-card">

                <div class="summary-number pass">
                    {pass_percentage}%
                </div>

                <div class="summary-label">
                    Pass %
                </div>

            </div>


        </div>

    </div>


    <!-- =================================================
         TEST EXECUTION DETAILS
         ================================================= -->


    <div class="test-section">

        <h2>
            Test Execution Details
        </h2>


        <table>


            <thead>

                <tr>

                    <th>
                        Test Case ID
                    </th>

                    <th>
                        Description
                    </th>

                    <th>
                        Status
                    </th>

                </tr>

            </thead>


            <tbody>

                {table_rows}

            </tbody>


        </table>


    </div>


    <!-- =================================================
         FOOTER
         ================================================= -->


    <div class="footer">

        Generated automatically by
        Demoblaze Automation Framework

        <br>

        Execution Time:
        {execution_time}

    </div>


</div>


</body>

</html>

"""

        return html


    # ========================================================
    # SAVE REPORT
    # ========================================================

    def save_report(self):

        self.report_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        html = self.generate_html()

        self.report_path.write_text(
            html,
            encoding="utf-8"
        )

        return self.report_path


    # ========================================================
    # MAIN GENERATOR
    # ========================================================

    def generate(self):

        print()

        print("=" * 70)

        print(
            "GENERATING DAILY QA REPORT"
        )

        print("=" * 70)

        print(
            f"Allure Results Directory: "
            f"{self.allure_results_dir}"
        )

        self.read_allure_results()

        print(
            f"Tests Found: "
            f"{len(self.test_results)}"
        )

        report_path = (
            self.save_report()
        )

        print()

        print(
            "DAILY QA REPORT GENERATED SUCCESSFULLY"
        )

        print(
            f"Location: {report_path}"
        )

        print()

        return report_path


# ============================================================
# FUNCTION FOR EXISTING CONFTEST
# ============================================================

def generate_daily_report(
    report_dir,
    allure_results_dir,
    environment="QA",
    browser="Chromium"
):

    report = DailyQAReport(
        report_dir=report_dir,
        allure_results_dir=allure_results_dir,
        environment=environment,
        browser=browser
    )

    return report.generate()