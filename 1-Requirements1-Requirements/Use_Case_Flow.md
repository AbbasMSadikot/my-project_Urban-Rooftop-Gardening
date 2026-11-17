# Use Case Flow: Log Seasonal Crop Planting

**System:** Urban Rooftop Gardening Co-op App  
**Primary actor:** Co-op Gardener  
**Related requirements:** FR-001, FR-002

## Preconditions

- The gardener has an account and is signed in.
- The gardener has a registered rooftop plot.
- Crop and seasonal growing information needed to estimate harvest windows is available to the app.

## Trigger

The gardener chooses **Log Crop Planting** for a registered plot.

## Main success scenario

1. The gardener opens a registered rooftop plot and selects **Log Crop Planting**.
2. The system displays the crop, plot, planting-date, and growing-season fields.
3. The gardener selects a crop and enters the planting date and relevant seasonal details.
4. The gardener submits the planting record.
5. The system checks that the plot belongs to the gardener and that the crop and date values are complete and valid.
6. The system saves the planting record.
7. The system calculates an estimated harvest window and expected yield weight from the crop and seasonal information.
8. The system shows the saved record and estimated harvest information, and schedules a harvest alert for the predicted window.
9. The gardener confirms the information.

## Alternate flow: Invalid planting information

- **At step 5**, if required information is missing, the date is invalid, or the planting date sequence is inconsistent with the selected season, the system does not save the record.
- The system identifies the field or date that needs correction and explains the validation issue.
- The gardener corrects the information and resubmits; the flow resumes at step 5.
- If the gardener cancels, the system discards the unsaved entry and returns to the plot.

## Postconditions

- **Success:** The planting record is stored against the selected plot, the estimated harvest window and yield are available, and a harvest alert is scheduled.
- **Failure or cancellation:** No invalid or incomplete planting record is stored.

## Acceptance checks

- A valid planting record is saved with the selected plot, crop, and planting date.
- The system displays an estimated harvest window and expected yield and schedules an alert within that predicted window.
- An invalid planting date or incomplete record is rejected with an actionable message and is not saved.
