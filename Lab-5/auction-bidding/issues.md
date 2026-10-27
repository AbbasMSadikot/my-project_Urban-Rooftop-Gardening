# Static Analysis Issue Table

Line numbers refer to the unmodified `auction_system.py` from the assigned starter repository. Severity follows Bandit where applicable; other entries are ranked by likely impact.

| Issue | Type / severity | Line(s) | Description | Fix approach |
| --- | --- | ---: | --- | --- |
| XML-RPC parser handles untrusted XML (Bandit B411) | Security / High | 5, 73-75 | `xmlrpc.client` is flagged for XML entity and parser attacks. | Replaced the XML-RPC client with a JSON request over an HTTPS-only connection. |
| Jinja autoescaping disabled (Bandit B701) | Security / High | 65-67 | Auction titles can contain HTML or script content and are rendered without escaping. | Enabled Jinja autoescaping for rendered listings. |
| Untrusted bidder name marked safe (Bandit B704) | Security / Medium | 69-70 | `Markup` bypasses output escaping for bidder-controlled text. | Removed `Markup` and HTML-escaped bidder names before placing them in the badge. |
| Overly broad exception handling (Pylint W0718) | Reliability / Medium | 47-51 | Catching every `Exception` hides programming errors and unrelated failures as a rejected bid. | Removed the catch-all; unknown auction IDs are handled explicitly while invalid input is visible. |
| Reserve price not enforced | Logic / High | 21-27 | The first bid only needs to be at least zero, so a below-reserve bid can become the winner. | Require the first bid to meet the reserve and return no winner if the reserve is not met. |
| Minimum increment unused; equal bids accepted | Logic / Medium | 9, 24-28 | `MIN_INCREMENT` is never applied and `>=` allows a tie to replace the current leader. | Require later bids to exceed the current high by the configured increment. |
| Seller can bid on own auction | Logic / Medium | 21-28 | The seller is not excluded from bidding, enabling self-bidding. | Reject bids whose bidder matches the seller. |
| Bid times compared as strings | Logic / Medium | 22, 96 | Lexicographic comparison rejects a valid time such as `9:30` before an `18:00` close. | Parse both bid and close times as datetimes before comparison. |
| Naming, missing docstrings, import order, and whitespace | Style / Low | 1-107 | Pylint and Flake8 report non-snake-case names, missing documentation, import ordering, long lines, and spacing. | Applied PEP 8 names and spacing, added docstrings, ordered imports, and wrapped long lines. |

## Verification summary

The corrected file reports Pylint 10.00/10, no Bandit findings, and no Flake8 findings. Full captured reports are in `reports/before/` and `reports/after/`.
