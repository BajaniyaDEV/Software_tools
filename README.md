# MapleFreight Delivery Delay Prediction & Slack Alerts

**Course:** AML 3303 --- Assessment 1

## Project Overview

This project explores whether historical shipment information can
identify deliveries at risk of arriving late. The goal is to support
MapleFreight dispatch staff with early risk indicators and a Slack-style
alert format.

## Dataset

-   Input file: `maplefreight_delivery_delay_dataset(1).csv`
-   Original size: 6,035 rows × 23 columns
-   Target: `delivered_late` (`1` = late, `0` = on time)
-   Cleaned analysis set: 5,999 records after category normalization,
    duplicate removal, and exclusion of conflicting shipment ID
    `SHP-101906`
-   Late shipments in the cleaned set: 1,234 (20.6%)

## Workflow

1.  Load and inspect shipment data.
2.  Normalize category text and remove exact duplicate rows.
3.  Exclude the conflicting shipment ID rather than guess which record
    is correct.
4.  Explore target balance, late rates, numeric distributions, and
    operational patterns.
5.  Exclude `shipment_id` and leakage-prone `actual_transit_hours` from
    model inputs.
6.  Split data into stratified train, validation, and test sets (3,599 /
    1,200 / 1,200).
7.  Apply numeric imputation/scaling and categorical imputation/one-hot
    encoding in a pipeline.
8.  Compare an all-on-time baseline, balanced Logistic Regression,
    balanced Decision Tree, and balanced Random Forest.
9.  Select the model by validation PR-AUC and choose an alert threshold
    on validation data.
10. Evaluate the selected model on the held-out test set and prepare
    Slack-style alert text.

## Main Findings

-   Observed late-delivery rate after cleaning: **20.6%**.
-   Contract Owner-Op shipments had a higher observed late rate (36.0%)
    than MapleFreight Fleet shipments (12.8%) in this dataset.
-   Late shipments had higher median distance, number of stops, pickup
    delay, and traffic index in the notebook's exploratory analysis.
-   Weather condition, traffic index, number of stops, and carrier were
    the top four features by test-set permutation importance.
-   These findings describe associations; they do not prove causation.

## Model and Threshold

-   Selected model: **Balanced Logistic Regression**, selected by
    validation PR-AUC.
-   Alert threshold: **0.61**.
-   Threshold rule: require at least 50% recall on validation data, then
    choose the eligible threshold with the highest F1-score.
-   Validation precision: 0.518; recall: 0.636; F1-score: 0.571.

### Held-out Test Results

  Metric                         Result
  ---------------------------- --------
  Accuracy                        0.789
  Late-shipment precision         0.490
  Late-shipment recall            0.591
  Late-shipment F1-score          0.536
  PR-AUC / average precision      0.535

Confusion matrix counts: **801 true negatives, 152 false positives, 101
false negatives, 146 true positives**. The model caught 146 of 247 late
shipments and missed 101, while producing 152 false alerts.

## Slack Alert Status

The notebook prepares a Slack-style alert with the number of high-risk
examples and the top five examples. The reviewed notebook output
explicitly says **Dry run only** because `SLACK_WEBHOOK_URL` is not
configured. Do not claim a real Slack message was sent unless you
configure the webhook and verify delivery.

To complete a real integration, create a Slack Incoming Webhook for
`#dispatch-alerts`, place the URL in a local `.env` file as
`SLACK_WEBHOOK_URL`, ensure `.env` is in `.gitignore`, and save
`screenshots/slack_alert.png` only after a real successful message.
Never commit or display the real webhook URL.

## Setup and Run

1.  Place the notebook and dataset in the expected project folder, or
    update the notebook's data path.
2.  Install the packages used by the notebook (for example, pandas,
    numpy, scikit-learn, matplotlib, seaborn, python-dotenv, and
    requests).
3.  Open `MapleFreight_Delivery_Delay_Prediction_Reviewed.ipynb` in
    Jupyter or VS Code.
4.  Restart the kernel and run all cells from top to bottom.
5.  Confirm the outputs and metrics match this README before submitting.

## Limitations and Next Steps

-   Verify unusually large weight values and confirm their units.
-   Confirm each feature is available at prediction time.
-   Validate performance on newer shipments.
-   Select thresholds based on the actual cost of missed delays and
    dispatch alert capacity.
-   Complete and test the real Slack webhook before claiming operational
    integration.

## AI Assistance Disclosure --- Edit Before Submission

Disclose only the AI tools you actually used and follow the course
policy. The assignment guide asks for one example of an AI output that
was wrong and how it was checked. Use a real, verifiable example from
your own work; do not invent one.

## Repository Checklist

-   [ ] `MapleFreight_Delivery_Delay_Prediction_<your_id>.ipynb`
-   [ ] `README.md`
-   [ ] `requirements.txt`
-   [ ] `.gitignore`
-   [ ] `.env.example` (placeholder only; no real webhook URL)
-   [ ] `screenshots/slack_alert.png` (only after real Slack delivery)
-   [ ] Dataset or permitted download instructions
