# Shopify E-Commerce: Discount & Profitability Analyzer

## 1. Problem & User
E-commerce managers frequently rely on aggressive discount strategies to drive sales volume, but often lack real-time visibility into how these discounts silently erode net profit margins. This interactive dashboard empowers **Shopify Store Managers and Pricing Analysts** to dynamically simulate pricing thresholds and instantly identify the precise point where a transaction becomes unprofitable.

## 2. Data
* **Source**: [Shopify Sales Dataset for ML and EDA](https://www.kaggle.com/datasets/aliiihussain/shopify-sales-dataset-for-ml-and-eda/data) (Kaggle).
* **Access Date**: April 24, 2026.
* **Key Fields**: `product_category`, `discount_percent`, `revenue`, `profit`, and `order_id`. The dataset comprises approximately 60,000 structured, real-world e-commerce transaction records.

## 3. Methods
1. **Data Ingestion & Safety Mechanisms**: Loaded the dataset using `pandas.read_csv()` and implemented offset mechanisms (e.g., adding `0.001` to denominators) to proactively prevent zero-division errors during metric calculation.
2. **Feature Engineering**: Engineered the critical business metric, `net_margin_%`, by calculating `(profit / revenue) * 100` utilizing Pandas vectorized operations for high-speed computation over large datasets.
3. **Interactive UI Logic**: Connected Streamlit widgets (`st.slider` and `st.multiselect`) directly to Pandas boolean indexing. This creates a reactive data pipeline that dynamically groups and cross-filters the dataframe in real-time based on user input.

## 4. Key Findings
* **The Margin Trap**: Interacting with the scatter plot reveals a clear trend: while discounts exceeding 30% successfully drive gross revenue per transaction, they frequently push the `net_margin_%` into dangerous, negative territory.
* **Category-Specific Sensitivity**: The boxplot visualization demonstrates that baseline margins vary significantly across departments. Categories like "Beauty" can absorb deeper discounts while remaining profitable, whereas "Accessories" quickly generate losses under the same promotional pressure.
* **Actionable Auditing**: By adjusting the discount threshold, the "Audit Trail" successfully isolates specific loss-making transactions. It pinpoints the exact `order_id`s where `profit < 0`, transitioning the tool from high-level visualization to granular, executable risk management.

## 5. How to run & Interactive Guide

### Initial Setup
1. Clone this repository and ensure the dataset (`shopify_sales_dataset_ml_eda.csv`) is placed inside a `data/` directory.
2. Install the required Python dependencies via your terminal: `pip install -r requirements.txt` (requires `streamlit`, `pandas`, `plotly`).
3. Launch the application locally by executing: `streamlit run app.py`.

### Dashboard Operations & Expected Results
Once the dashboard renders in your browser, the following interactive workflows are available:

* **Operation 1: Adjust the "Maximum Discount Rate" Slider (Sidebar)**
  * **Action:** Slide the threshold from 100% down to a stricter policy (e.g., 20%).
  * **Result:** The underlying Pandas dataframe instantly filters out transactions with a discount exceeding 20%. The top KPI metrics (Total Revenue, Average Net Margin) automatically recalculate. This simulates how capping discounts improves overall profitability at the expense of sales volume.

* **Operation 2: Toggle the "Product Categories" Multiselect (Sidebar)**
  * **Action:** Select or deselect specific business units (e.g., isolating the view to "Electronics" and "Fashion").
  * **Result:** The "Profit Margin Distribution" boxplot updates to display only the selected categories. This allows analysts to compare which departments maintain healthier margins under identical pricing pressures.

* **Operation 3: Hover over Visualizations (Main Dashboard)**
  * **Action:** Hover the cursor over individual data points on the Scatter Plot.
  * **Result:** Plotly renders a dynamic tooltip displaying the exact financial figures (Revenue, Discount Rate, and Profit) for that specific transaction, providing granular visibility without requiring custom SQL queries.

* **Operation 4: Expand the "Audit Trail" (Bottom of Dashboard)**
  * **Action:** Click the expander titled "🚨 Audit Trail: View Loss-Making Transactions".
  * **Result:** Unfolds a detailed data table. Based on the active slider and category settings, this table isolates the exact records where profit fell below zero, providing management with a targeted list of high-risk orders for review.

## 6. Product link / Demo
* **Live App**: [https://acc102-data-appuct-zf2qwjvq9ypw82qrd9pnzj.streamlit.app/]
* **Demo Video**: [https://video.xjtlu.edu.cn/Mediasite/Play/50dcba5141bf4e24a3d3f664199545691d]

## 7. Limitations & next steps
* **Limitation**: This tool evaluates profitability on a strict, isolated per-transaction basis. It does not account for Customer Acquisition Cost (CAC). In reality, a loss-making first order might be a justified business expense if it secures a customer with a high long-term value.
* **Next Steps**: Utilize the `customer_id` field within the dataset to perform Pandas `.groupby()` cohort analysis. This would track Customer Lifetime Value (CLTV) to determine if shoppers acquired via deep discounts actually return for profitable subsequent purchases.
