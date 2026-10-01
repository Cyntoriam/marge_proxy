"""
M.A.R.G.E. Automated Test Client
Executes job-hunting red-teaming case studies against the local FastAPI evaluation middleware.
"""

import sys

import requests

try:
    from app.marge_job_hunting_case_studies import MARGE_JOB_HUNTING_CASE_STUDIES
except ImportError:
    from marge_job_hunting_case_studies import MARGE_JOB_HUNTING_CASE_STUDIES

BASE_URL = "http://127.0.0.1:8000"
REQUEST_TIMEOUT = 12


def run_test_client() -> int:
    print("=" * 65)
    print("      M.A.R.G.E. JOB-HUNTING RED-TEAM EVALUATION CLIENT       ")
    print("=" * 65)

    if not MARGE_JOB_HUNTING_CASE_STUDIES:
        print("[WARNING] No test cases found in MARGE_JOB_HUNTING_CASE_STUDIES.")
        return 0

    print(
        f"Loaded {len(MARGE_JOB_HUNTING_CASE_STUDIES)} red-teaming test cases. "
        "Starting evaluation requests...\n"
    )

    passed_count = 0
    failed_count = 0

    for idx, case in enumerate(MARGE_JOB_HUNTING_CASE_STUDIES, 1):
        payload = {
            "request_id": case.test_id,
            "prompt": case.input_prompt,
            "parameters": {
                "target_domain": case.target_domain,
                "equity_pillar": case.equity_pillar,
                "job_hunting_case": True,
            },
        }

        print(f"[{idx}/{len(MARGE_JOB_HUNTING_CASE_STUDIES)}] Testing Pillar: {case.equity_pillar}")
        print(f"  Domain : {case.target_domain}")
        print(f"  Prompt : \"{case.input_prompt[:75]}...\"")

        try:
            response = requests.post(
                f"{BASE_URL}/evaluate",
                json=payload,
                timeout=REQUEST_TIMEOUT,
            )
        except requests.exceptions.ConnectionError:
            print(f"  [CONNECTION ERROR] Could not connect to FastAPI at {BASE_URL}.")
            print("  -> Make sure Uvicorn is running: uvicorn app.main:app --reload")
            break
        except Exception as exc:
            print(f"  [ERROR] {exc}")
            failed_count += 1
            print("-" * 65)
            continue

        print(f"  HTTP status: {response.status_code}")
        if response.status_code != 200:
            print(f"  [SERVER ERROR] Status {response.status_code}: {response.text}")
            failed_count += 1
            print("-" * 65)
            continue

        try:
            data = response.json()
        except ValueError:
            print("  [INVALID JSON] Response was not valid JSON.")
            failed_count += 1
            print("-" * 65)
            continue

        print("  [SUCCESS] Middleware Response:")
        print(f"    -> path_type        : {data.get('path_type', 'N/A')}")
        print(f"    -> overall_approved : {data.get('overall_approved', 'N/A')}")
        evaluations = data.get("evaluations", [])
        if evaluations:
            first_eval = evaluations[0]
            print(
                "    -> first pillar     : "
                f"{first_eval.get('pillar', 'N/A')} | "
                f"flagged={first_eval.get('flagged', 'N/A')} | "
                f"severity={first_eval.get('severity', 'N/A')}"
            )
        if data.get("suggested_correction"):
            print(f"    -> suggested correction: {data.get('suggested_correction')}")
        passed_count += 1
        print("-" * 65)

    print("\n=== Test Run Summary ===")
    print(f"Total Evaluated : {passed_count + failed_count}")
    print(f"Successful Calls: {passed_count}")
    print(f"Failed Calls    : {failed_count}")
    print("=" * 65)
    return 0 if failed_count == 0 else 1


if __name__ == "__main__":
    sys.exit(run_test_client())
