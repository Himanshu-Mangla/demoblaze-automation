import os
import subprocess
from pathlib import Path
from datetime import datetime

import allure
import pytest
import yaml

from playwright.sync_api import sync_playwright

from utils.daily_report import generate_daily_report


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).parent


# ============================================================
# REPORT DIRECTORIES
# ============================================================

REPORT_DIR = None
ALLURE_RESULTS_DIR = None
ALLURE_REPORT_DIR = None
SCREENSHOTS_DIR = None
VIDEOS_DIR = None
TRACES_DIR = None


# ============================================================
# CREATE REPORT DIRECTORY
# ============================================================

def pytest_configure(config):

    global REPORT_DIR
    global ALLURE_RESULTS_DIR
    global ALLURE_REPORT_DIR
    global SCREENSHOTS_DIR
    global VIDEOS_DIR
    global TRACES_DIR

    # --------------------------------------------------------
    # WORKER PROCESS
    # --------------------------------------------------------

    if hasattr(config, "workerinput"):

        REPORT_DIR = Path(
            config.workerinput["report_dir"]
        )

        ALLURE_RESULTS_DIR = Path(
            config.workerinput["allure_results_dir"]
        )

        ALLURE_REPORT_DIR = Path(
            config.workerinput["allure_report_dir"]
        )

        SCREENSHOTS_DIR = Path(
            config.workerinput["screenshots_dir"]
        )

        VIDEOS_DIR = Path(
            config.workerinput["videos_dir"]
        )

        TRACES_DIR = Path(
            config.workerinput["traces_dir"]
        )

    # --------------------------------------------------------
    # MASTER PROCESS
    # --------------------------------------------------------

    else:

        timestamp = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

        REPORT_DIR = (
            PROJECT_ROOT /
            "reports" /
            timestamp
        )

        ALLURE_RESULTS_DIR = (
            REPORT_DIR /
            "allure-results"
        )

        ALLURE_REPORT_DIR = (
            REPORT_DIR /
            "allure-report"
        )

        SCREENSHOTS_DIR = (
            REPORT_DIR /
            "screenshots"
        )

        VIDEOS_DIR = (
            REPORT_DIR /
            "videos"
        )

        TRACES_DIR = (
            REPORT_DIR /
            "traces"
        )

        # Create directories

        for directory in [
            ALLURE_RESULTS_DIR,
            ALLURE_REPORT_DIR,
            SCREENSHOTS_DIR,
            VIDEOS_DIR,
            TRACES_DIR
        ]:

            directory.mkdir(
                parents=True,
                exist_ok=True
            )

        # Store paths for workers

        config._report_dir = str(
            REPORT_DIR
        )

        config._allure_results_dir = str(
            ALLURE_RESULTS_DIR
        )

        config._allure_report_dir = str(
            ALLURE_REPORT_DIR
        )

        config._screenshots_dir = str(
            SCREENSHOTS_DIR
        )

        config._videos_dir = str(
            VIDEOS_DIR
        )

        config._traces_dir = str(
            TRACES_DIR
        )

    # --------------------------------------------------------
    # ALLURE RESULTS
    # --------------------------------------------------------

    config.option.allure_report_dir = str(
        ALLURE_RESULTS_DIR
    )


# ============================================================
# SEND PATHS TO XDIST WORKERS
# ============================================================

def pytest_configure_node(node):

    node.workerinput["report_dir"] = (
        node.config._report_dir
    )

    node.workerinput["allure_results_dir"] = (
        node.config._allure_results_dir
    )

    node.workerinput["allure_report_dir"] = (
        node.config._allure_report_dir
    )

    node.workerinput["screenshots_dir"] = (
        node.config._screenshots_dir
    )

    node.workerinput["videos_dir"] = (
        node.config._videos_dir
    )

    node.workerinput["traces_dir"] = (
        node.config._traces_dir
    )


# ============================================================
# STORE TEST RESULT
# ============================================================

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield

    report = outcome.get_result()

    setattr(
        item,
        f"rep_{report.when}",
        report
    )


# ============================================================
# CONFIG FIXTURE
# ============================================================

@pytest.fixture(scope="session")
def config():

    config_path = (
        PROJECT_ROOT /
        "config" /
        "qa.yaml"
    )

    with open(
        config_path,
        "r"
    ) as file:

        return yaml.safe_load(file)


# ============================================================
# BASE URL FIXTURE
# ============================================================

@pytest.fixture(scope="session")
def base_url(config):

    return config["application"]["url"]


# ============================================================
# PLAYWRIGHT PAGE FIXTURE
# ============================================================

@pytest.fixture
def page(config, request):

    with sync_playwright() as playwright:

        # ----------------------------------------------------
        # BROWSER
        # ----------------------------------------------------

        browser = playwright.chromium.launch(

            headless=config["browser"]["headless"],

            slow_mo=config["browser"]["slow_mo"]

        )

        # ----------------------------------------------------
        # CONTEXT
        # ----------------------------------------------------

        context = browser.new_context(

            record_video_dir=str(
                VIDEOS_DIR
            )

        )

        # ----------------------------------------------------
        # PAGE
        # ----------------------------------------------------

        page = context.new_page()

        page.set_default_timeout(

            config["timeouts"]["default"]

        )

        # ----------------------------------------------------
        # START TRACE
        # ----------------------------------------------------

        context.tracing.start(

            screenshots=True,

            snapshots=True,

            sources=True

        )

        # ----------------------------------------------------
        # RUN TEST
        # ----------------------------------------------------

        yield page

        # ----------------------------------------------------
        # CHECK FAILURE
        # ----------------------------------------------------

        failed = (

            hasattr(
                request.node,
                "rep_call"
            )

            and
            request.node.rep_call.failed

        )

        # ----------------------------------------------------
        # UNIQUE TEST NAME
        # ----------------------------------------------------

        test_name = request.node.name

        worker_id = os.environ.get(

            "PYTEST_XDIST_WORKER",

            "master"

        )

        file_prefix = (
            f"{test_name}_{worker_id}"
        )

        # ====================================================
        # SCREENSHOT
        # ====================================================

        if failed:

            screenshot_path = (

                SCREENSHOTS_DIR /

                f"{file_prefix}.png"

            )

            screenshot_bytes = page.screenshot(

                path=str(
                    screenshot_path
                ),

                full_page=True

            )

            allure.attach(

                screenshot_bytes,

                name="Failure Screenshot",

                attachment_type=(
                    allure.attachment_type.PNG
                )

            )

        # ====================================================
        # TRACE
        # ====================================================

        if failed:

            trace_path = (

                TRACES_DIR /

                f"{file_prefix}.zip"

            )

            context.tracing.stop(

                path=str(
                    trace_path
                )

            )

            allure.attach.file(

                str(trace_path),

                name="Playwright Trace",

                attachment_type=(
                    allure.attachment_type.ZIP
                )

            )

        else:

            context.tracing.stop()

        # ====================================================
        # VIDEO
        # ====================================================

        video = page.video

        # Video finalized here

        context.close()

        if failed and video:

            video_path = video.path()

            allure.attach.file(

                str(video_path),

                name="Failure Video",

                attachment_type=(
                    allure.attachment_type.WEBM
                )

            )

        # ====================================================
        # CLOSE BROWSER
        # ====================================================

        browser.close()


# ============================================================
# GENERATE REPORTS
# ============================================================

def pytest_sessionfinish(
    session,
    exitstatus
):

    # --------------------------------------------------------
    # ONLY MASTER CREATES REPORTS
    # --------------------------------------------------------

    if hasattr(
        session.config,
        "workerinput"
    ):

        return

    print()

    print("=" * 70)

    print(
        "GENERATING TEST REPORTS"
    )

    print("=" * 70)

    # ========================================================
    # ALLURE HTML REPORT
    # ========================================================

    command = [

        "allure",

        "generate",

        str(
            ALLURE_RESULTS_DIR
        ),

        "-o",

        str(
            ALLURE_REPORT_DIR
        ),

        "--clean"

    ]

    try:

        subprocess.run(

            command,

            check=True

        )

        print()

        print(
            "ALLURE REPORT GENERATED SUCCESSFULLY"
        )

    except FileNotFoundError:

        print()

        print(
            "ERROR: ALLURE CLI NOT FOUND"
        )

        print()

        print(
            "Run: allure --version"
        )

        print()

    except subprocess.CalledProcessError:

        print()

        print(
            "ERROR: ALLURE REPORT GENERATION FAILED"
        )

    # ========================================================
    # DAILY QA REPORT
    # ========================================================

    try:

        daily_report = generate_daily_report(

            report_dir=REPORT_DIR,

            allure_results_dir=(
                ALLURE_RESULTS_DIR
            ),

            environment="QA",

            browser="Chromium"

        )

        print()

        print(
            "DAILY QA REPORT GENERATED SUCCESSFULLY"
        )

        print()

        print(
            f"Daily QA Report : {daily_report}"
        )

    except Exception as error:

        print()

        print(
            "ERROR GENERATING DAILY QA REPORT"
        )

        print(
            error
        )

    # ========================================================
    # FINAL LOCATIONS
    # ========================================================

    print()

    print("=" * 70)

    print(
        "REPORT LOCATIONS"
    )

    print("=" * 70)

    print(
        f"Report Directory : {REPORT_DIR}"
    )

    print(
        f"Allure Results   : {ALLURE_RESULTS_DIR}"
    )

    print(
        f"Allure Report    : {ALLURE_REPORT_DIR}"
    )

    print(
        f"Screenshots      : {SCREENSHOTS_DIR}"
    )

    print(
        f"Videos           : {VIDEOS_DIR}"
    )

    print(
        f"Traces           : {TRACES_DIR}"
    )

    print(
        f"Daily QA Report  : "
        f"{REPORT_DIR / 'daily-qa-report.html'}"
    )

    print()