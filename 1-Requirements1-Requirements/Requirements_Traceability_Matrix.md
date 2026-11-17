# Requirements Traceability Matrix

This matrix links the Lab 1 requirements in the [requirements workbook](PES1UG25CS840_Urban_Rooftop_Gardening_Requirements%20(2).xlsx) to the use cases in the [diagram](Urban_Rooftop_Gardening_Use_Case_Diagram.svg) and [flow specification](Use_Case_Flow.md).

| Requirement | Requirement summary | Use case coverage | Verification evidence / method |
|---|---|---|---|
| FR-001 | Record seasonal planting dates and calculate estimated harvest window and yield | Log Seasonal Crop Planting; Calculate Harvest Window & Expected Yield | Use the flow's valid and invalid date acceptance checks; verify a valid entry stores and displays its harvest estimate |
| FR-002 | Register and manage rooftop plots | Register / Manage Rooftop Plot | Verify create, view, and update for valid plot records; verify incomplete or invalid details are rejected |
| FR-003 | Record harvested crop and actual yield for a registered plot | Record Harvest & Actual Yield | Verify a valid record stores crop, harvest date, plot, and yield; verify missing or invalid required values are rejected |
| FR-004 | Share soil maintenance tips | Share / Browse Soil Maintenance Tips; Manage Co-op Plots, Tips & Listings | Verify a valid tip can be submitted and viewed; verify empty or invalid tips are not published |
| FR-005 | Create and manage surplus produce listings for trading | Browse Surplus Listings; Request / Trade Surplus Produce; Manage Co-op Plots, Tips & Listings | Verify a valid listing is visible with produce and availability; verify invalid listings cannot be published and a member can request/trade available produce |
| NFR-001 | Keep surplus listings current across members and protect access | Browse Surplus Listings; Request / Trade Surplus Produce | Performance/security testing is required. The source requirement does not specify numeric latency or security thresholds; agree those targets with the project stakeholders before treating this row as fully testable. |
| NFR-002 | Provide a clear, reliable interface and preserve valid records | All user-facing use cases | Usability and reliability testing is required. Define measurable task-success and record-retrieval targets with stakeholders before final acceptance. |

## Coverage note

Every functional requirement maps to at least one use case and a verification method. NFR-001 and NFR-002 are mapped, but their source acceptance criteria need agreed measurable thresholds before they can be considered fully testable. The matrix describes planned verification; it does not claim that application tests have been run.
