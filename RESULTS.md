# API lab results

> Live verification pending. The development environment could not resolve `quickpizza.grafana.com`, so observed values below are **not** presented as measured results. Run the commands on a machine with internet access and replace the pending entries before submission.

## Part 0

- Step 0.1, number of pizza names: **pending** (`curl https://quickpizza.grafana.com/api/names`)
- Step 0.3, unauthenticated `/api/tools`: **401 expected from lab**; confirm with curl.
- Step 0.4, vegetarian pizza name: **pending**, randomly selected.
- Step 0.12, three no-session runs: **not performed (optional)**.
- Step 0.16, blocks of excluded tools: **0, 1, 2, 3**. Three excluded tools is the unsatisfiable case.

## Defect report — Defect 1

- **Title:** Excluding every cutting tool produces an internal server error.
- **Request:** `POST /api/pizza`, with own logged-in token and JSON `{"excludedTools":["Knife","Pizza cutter","Scissors"]}`.
- **Expected:** HTTP 400 with a JSON error explaining that no pizza can meet the restriction.
- **Actual:** The lab document reports HTTP 500 and an empty body. **Not independently verified in this environment.**
- **Severity:** Medium — client cannot distinguish invalid input from a server failure or show a useful error.
- **Regression test:** `test_all_tools_excluded_returns_clear_error` is marked strict `xfail` until the API is fixed.
- **Curl reproduction:** `curl -i -H "@auth.txt" -H "Content-Type: application/json" -d "@all_tools.json" https://quickpizza.grafana.com/api/pizza` (the public token is used here only for pizza recommendation, not ratings).

## Part A

- Step A4, other user GET / PUT / DELETE status codes: **pending live run**. All must be 4xx; exact codes should be recorded here.
- Error bodies for decimal/text/missing stars and nonexistent pizza: **pending curl confirmation**.

## Part B — Reflection

1. API tests can catch incorrect HTTP responses and problems caused by server/database integration, which stubbed unit tests can miss. Unit tests are still useful because they are fast and can isolate logic without relying on a network.
2. A fresh user prevents my tests from interfering with other students' data. In Project 2 I would create separate shop or hotel records for each test and clean up only my own data.
3. A single session keeps the AWSALB cookie so registration and login reach the same backend. Without it, requests may go to different servers and login can fail even when the credentials are correct.
4. The **3 excluded tools** block reveals the documented defect. A 500 with no message leaves the client unsure how to correct the request; a 400 with JSON is actionable. Keeping a strict xfail preserves the regression check and alerts us when the defect is fixed.
5. Base choice: `1 + 2 + 3 + 1 + 2 = 9` tests. All combinations: `3 × 4 × 2 × 3 = 72` tests.
6. Exact GET/PUT/DELETE codes: **pending**. Expected: each request should be rejected with a 4xx status and the owner's rating should remain unchanged. A successful unauthorized read/update/delete would be an access-control defect; different 4xx codes need interpretation against the documented API contract.
7. Made-up 16-character token: **pending live observation**. Run `curl -i -H "@madeup.txt" https://quickpizza.grafana.com/api/ratings` for a read-only check. If it grants access without a real login, that is an authentication defect: a stranger could access private ratings, and possibly modify data if write endpoints share the same weakness. Do not test writes with this token.
8. API tests check response codes and JSON fields directly and precisely. Browser tests can check whether the page actually renders correctly and whether the user can complete a UI flow.

## Final run

```bash
pytest -v --html=report.html --self-contained-html
```

- Observed summary: **pending** (lab target: 32 passed, 1 xfailed).
- Do not commit `report.html` until generated from a real run.
