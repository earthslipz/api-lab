# API lab results

ITCS386 - API Testing with pytest and requests  
Test date: 8 November 2026

## Part 0

- **Step 0.1, number of pizza names:** 18. The request to `/api/names` returned 200.
- **Step 0.3, request to `/api/tools` without a token:** 401, with `{"error":"authentication failed"}`.
- **Step 0.4, vegetarian pizza name:** The Hurt Quattro Stagioni.
- **Step 0.12, three runs without a session:** I skipped this step because it was optional.
- **Step 0.16, blocks for the number of excluded tools:** 0, 1, 2, and 3 tools. My first tests did not cover all the blocks. Excluding all 3 tools showed the bug.

## Defect report

- **Title:** API returns 500 when all pizza cutting tools are excluded.
- **Request:** `POST /api/pizza` with my test user's token and this JSON body:

  ```json
  {"excludedTools": ["Knife", "Pizza cutter", "Scissors"]}
  ```

- **Expected result:** Status 400 and a JSON error saying that no pizza can meet the request.
- **Actual result:** Status 500 with an empty response body.
- **Severity:** Medium. The request is invalid, but the API treats it as a server error. The app would not know what message to show the user.

I kept this case in the tests as `xfail` because it is a known bug. If the API gets fixed, the strict `xfail` will tell us to check the test again.

## Part A

**Step A2 - Invalid rating inputs**

| Input | Status | Error returned |
|---|---|---|
| `stars = 3.5` | 400 | `json: cannot unmarshal number 3.5 into Go struct field Rating.stars of type int` |
| `stars = "3"` | 400 | `json: cannot unmarshal string into Go struct field Rating.stars of type int` |
| Missing `stars` | 400 | `number of stars must be between 1 and 5 (inclusive)` |
| Pizza ID `999999999` | 400 | `pizza ID 999999999 not found` |

**Step A4 - Another user trying to access a rating**

I created a 3-star rating with one account, then tried the three requests using another account.

| Request from second user | Status | What happened |
|---|---|---|
| GET rating | 404 | `not found` |
| PUT rating | 400 | `rating ID 158785 not found` |
| DELETE rating | 400 | `rating ID 158785 not found` |

After each request, the owner could still read the rating (200), and it was still 3 stars. I deleted my test rating at the end (204).

## Part B

**1.** API tests can find wrong status codes or JSON responses, and problems between the actual server and database. Unit tests using stubs might miss these because they do not contact the real server. I would still use unit tests because they run faster and make it easier to find which part of the code has a problem.

**2.** I used a new user for each test so my ratings would not mix with other students' ratings. Using the public token could affect shared data. For Project 2, I would do the same thing with test orders or bookings and clean up only the records my tests created.

**3.** One session keeps the `AWSALB` cookie, so requests are sent to the same backend server. Without it, the server handling login might not know the user created by the previous request. I did not do the optional three runs without a session.

**4.** The block with **3 excluded tools** found the bug. The API returned 500 and no message, so an app cannot tell the user what to fix. A 400 response with JSON would be clearer. I kept the test as `xfail` instead of deleting it because it is useful for checking whether the bug has been fixed later.

**5.** The four characteristics have 3, 4, 2 and 3 blocks. Base choice needs **9 tests**: `1 + 2 + 3 + 1 + 2 = 9`. All combinations need **72 tests**: `3 × 4 × 2 × 3 = 72`.

**6.** The other user got **404 for GET**, **400 for PUT**, and **400 for DELETE**. I expected the API to reject all three requests, usually with 403 or 404. The PUT and DELETE responses use 400 instead, which is not as clear, but they still rejected the requests. Since the rating was unchanged, I would not call this an access-control defect based on these results alone.

**7.** I used the made-up token `0000000000000000` to send `GET /api/ratings`. Surprisingly, the API returned **200** and a list of ratings. I think this is an authentication bug because a random token should not be enough to read rating data. Someone could potentially view ratings without logging in. I only tested GET, so I cannot say whether the token works for changing data.

**8.** API tests are better for checking exact status codes and JSON fields. Browser tests can check things an API test cannot, like whether the page looks correct and whether the buttons and forms work for a user.

## Final test run

Command:

```powershell
python -m pytest -v --html=report.html --self-contained-html
```

Result:

```text
32 passed, 1 xfailed in 47.34s
```

The full HTML report is saved as `report.html`.
