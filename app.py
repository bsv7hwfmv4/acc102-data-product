import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="Shopify Profitability Analyzer", layout="wide", page_icon="🛍️")
st.title("Shopify Store: Discount & Profitability Analyzer")
st.markdown("An interactive dashboard for E-commerce Managers to evaluate how discount strategies impact net margins and revenue.")


@st.cache_data
def load_and_clean_data():
    file_path = 'data/shopify_sales_dataset_ml_eda.csv'
    
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        st.error("Dataset not found. Please ensure 'shopify_sales_dataset_ml_eda.csv' is in the 'data/' folder.")
        st.stop()

    if 'revenue' in df.columns and 'profit' in df.columns:

        df['net_margin_%'] = (df['profit'] / (df['revenue'] + 0.001)) * 100
    else:
        df['net_margin_%'] = 0.0
        
    if 'discount_percent' in df.columns:
        df.rename(columns={'discount_percent': 'discount_rate_%'}, inplace=True)
    else:
        df['discount_rate_%'] = 0.0

    df.fillna(0, inplace=True)
    return df

df = load_and_clean_data()


st.sidebar.header("Strategy Simulator")
st.sidebar.markdown("Filter the data to analyze specific discount impacts.")


max_discount = st.sidebar.slider(
    "Maximum Discount Rate Allowed (%):", 
    min_value=0.0, max_value=100.0, value=40.0, step=5.0
)

category_col = 'product_category' 
if category_col in df.columns:
    selected_categories = st.sidebar.multiselect(
        "Select Product Categories:", 
        options=df[category_col].unique(),
        default=df[category_col].unique()[:5] 
    )
else:
    selected_categories = None


if selected_categories:
    filtered_df = df[(df['discount_rate_%'] <= max_discount) & (df[category_col].isin(selected_categories))]
else:
    filtered_df = df[df['discount_rate_%'] <= max_discount]


col1, col2, col3 = st.columns(3)
total_revenue = filtered_df['revenue'].sum()
avg_margin = filtered_df['net_margin_%'].mean()
total_orders = len(filtered_df)

col1.metric("Total Revenue (Filtered)", f"${total_revenue:,.0f}")
col2.metric("Average Net Margin", f"{avg_margin:.2f}%", 
            delta=f"{(avg_margin - df['net_margin_%'].mean()):.2f}% vs All Data")
col3.metric("Qualifying Orders", f"{total_orders:,}")

st.markdown("---")

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Revenue vs Discount Rate")

    fig_scatter = px.scatter(
        filtered_df, x="discount_rate_%", y="revenue", 
        color="profit",
        color_continuous_scale="RdYlGn",
        title="Impact of Discounts on Transaction Revenue",
        opacity=0.5
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with col_chart2:
    st.subheader("Profit Margin Distribution")
    fig_box = px.box(
        filtered_df, y="net_margin_%", 
        color=category_col if category_col in df.columns else None,
        title="Net Margin Stability across Categories"
    )

    fig_box.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Break-even (Zero Profit)")
    st.plotly_chart(fig_box, use_container_width=True)


with st.expander("Audit Trail: View Loss-Making Transactions"):
    if 'profit' in filtered_df.columns:
        losses = filtered_df[filtered_df['profit'] < 0].sort_values('profit')
        if not losses.empty:
            columns_to_show = ['order_id', 'product_category', 'discount_rate_%', 'revenue', 'profit', 'net_margin_%']
            st.dataframe(losses[columns_to_show].head(50))
        else:
            st.success("No loss-making transactions under current filters!")