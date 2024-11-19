import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title of the app
st.title("CSV Data Visualization App")

# File uploader for CSV
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # Read the CSV file and clean column names
        data = pd.read_csv(uploaded_file)
        data.columns = data.columns.str.strip()  # Remove extra spaces in column names

        # Handle datetime conversion
        for col in data.columns:
            try:
                data[col] = pd.to_datetime(data[col], errors='coerce')  # Convert to datetime, set invalid to NaT
            except Exception:
                continue  # Ignore columns that cannot be converted

        st.write("### Data Preview")
        st.dataframe(data)

        # Dropdown for selecting columns
        columns = data.columns.tolist()
        x_column = st.selectbox("Select X-axis column", columns)
        y_column = st.selectbox("Select Y-axis column", columns)

        # Dropdown for graph type
        graph_type = st.selectbox(
            "Select Graph Type",
            ["Line", "Scatter", "Bar", "Pie"]
        )

        # Validate selected columns
        if graph_type != "Pie":
            if pd.api.types.is_datetime64_any_dtype(data[x_column]):
                # Drop rows with NaT in the datetime column
                data = data.dropna(subset=[x_column])
                # Convert datetime to a numeric format for plotting
                data['numeric_x'] = data[x_column].map(lambda x: x.timestamp())
                x_column = 'numeric_x'
            elif not pd.api.types.is_numeric_dtype(data[x_column]):
                st.error(f"X-axis column '{x_column}' must be numeric or datetime.")
            if not pd.api.types.is_numeric_dtype(data[y_column]):
                st.error(f"Y-axis column '{y_column}' must be numeric.")
            else:
                # Plot button
                if st.button("Plot Graph"):
                    fig, ax = plt.subplots()

                    if graph_type == "Line":
                        ax.plot(data[x_column], data[y_column], marker='o')
                        ax.set_title(f"{y_column} vs {x_column} (Line Plot)")

                    elif graph_type == "Scatter":
                        ax.scatter(data[x_column], data[y_column])
                        ax.set_title(f"{y_column} vs {x_column} (Scatter Plot)")

                    elif graph_type == "Bar":
                        ax.bar(data[x_column], data[y_column])
                        ax.set_title(f"{y_column} vs {x_column} (Bar Chart)")

                    ax.set_xlabel(x_column)
                    ax.set_ylabel(y_column)
                    st.pyplot(fig)
        else:
            # For Pie Chart
            if data[x_column].nunique() <= 10:  # Limit to 10 unique categories
                fig, ax = plt.subplots()
                ax.pie(
                    data[y_column],
                    labels=data[x_column],
                    autopct='%1.1f%%',
                    startangle=90,
                )
                ax.set_title(f"{y_column} (Pie Chart)")
                st.pyplot(fig)
            else:
                st.error("Pie chart requires fewer than 10 unique categories in the X-axis.")

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
else:
    st.info("Please upload a CSV file to get started.")
