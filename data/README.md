# Dataset Notes

## Dataset
DataCo Smart Supply Chain for Big Data Analysis

## Source
https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis

## Purpose
Initial dataset audit for the SupplyPrescript shipment delay-risk project.

## Audit Summary
- Rows: 180,519
- Columns: 53
- Unique Order Ids: 65,752
- Unique Order Item Ids: 180,519
- Exact duplicate rows: 0
- Target column: `Late_delivery_risk`

## Current Status
Initial audit completed. Feature selection, data cleaning, and validation are pending.

## Data Handling
- Original CSV is stored locally in `data/raw/` and excluded from Git.
- Customer personal information will not be included in shared modeling files.
- Model features are not finalized; post-shipment outcome fields will be reviewed for target leakage.