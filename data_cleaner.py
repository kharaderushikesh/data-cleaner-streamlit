import streamlit as st
import pandas as pd
import json
import io
import plotly.express as px
import plotly.graph_objects as go

def assess_data_quality(df):
    """Assess and return data quality metrics."""
    quality = {}
    quality['Total Rows'] = len(df)
    quality['Total Columns'] = len(df.columns)
    quality['Missing Values'] = df.isnull().sum().to_dict()
    quality['Duplicate Rows'] = df.duplicated().sum()
    quality['Data Types'] = df.dtypes.to_dict()
    quality['Numeric Stats'] = df.describe().to_dict() if not df.select_dtypes(include=['number']).empty else "No numeric columns"
    return quality

def clean_data(df, operations, fill_method, outlier_threshold):
    """Apply selected cleaning to a DataFrame and track changes."""
    original_shape = df.shape
    original_missing = df.isnull().sum().sum()
    original_duplicates = df.duplicated().sum()
    
    changes = []
    
    if operations.get('remove_duplicates', False):
        df = df.drop_duplicates()
        if df.shape[0] < original_shape[0]:
            changes.append(f"Removed {original_duplicates} duplicate rows.")
    
    if operations.get('fill_missing', False):
        for col in df.columns:
            missing_before = df[col].isnull().sum()
            if df[col].dtype in ['int64', 'float64']:
                if fill_method == 'Mean':
                    df[col].fillna(df[col].mean(), inplace=True)
                elif fill_method == 'Median':
                    df[col].fillna(df[col].median(), inplace=True)
                elif fill_method == 'Mode':
                    df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else 0, inplace=True)
            else:
                df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else 'Unknown', inplace=True)
            missing_after = df[col].isnull().sum()
            if missing_before > missing_after:
                changes.append(f"Filled {missing_before - missing_after} missing values in '{col}' using {fill_method}.")
    
    if operations.get('convert_dates', False):
        for col in df.columns:
            if df[col].dtype == 'object':
                try:
                    df[col] = pd.to_datetime(df[col])
                    changes.append(f"Converted '{col}' to datetime.")
                except (ValueError, TypeError):
                    pass
    
    if operations.get('remove_outliers', False):
        outliers_removed = 0
        for col in df.select_dtypes(include=['number']).columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - outlier_threshold * IQR
            upper_bound = Q3 + outlier_threshold * IQR
            before_count = len(df)
            df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
            outliers_removed += (before_count - len(df))
        if outliers_removed > 0:
            changes.append(f"Removed {outliers_removed} outlier rows across numeric columns (IQR with multiplier {outlier_threshold}).")
    
    final_shape = df.shape
    final_missing = df.isnull().sum().sum()
    if final_shape != original_shape:
        changes.append(f"Shape changed from {original_shape} to {final_shape}.")
    if final_missing < original_missing:
        changes.append(f"Total missing values reduced from {original_missing} to {final_missing}.")
    
    return df, changes

def load_file(uploaded_file):
    """Load file based on type."""
    file_type = uploaded_file.name.split('.')[-1].lower()
    if file_type == 'csv':
        return pd.read_csv(uploaded_file)
    elif file_type in ['xlsx', 'xls']:
        return pd.read_excel(uploaded_file)
    elif file_type == 'json':
        data = json.load(uploaded_file)
        return pd.json_normalize(data) if isinstance(data, list) else pd.DataFrame([data])
    elif file_type == 'txt':
        content = uploaded_file.read().decode('utf-8')
        return pd.read_csv(io.StringIO(content), sep='\t')
    else:
        st.error("Unsupported file type. Supported: CSV, Excel, JSON, TXT.")
        return None

st.title("Interactive Data Cleaner for Data Analysts & Scientists")
st.write("Upload a file, assess its quality, customize cleaning operations, and visualize changes.")

uploaded_file = st.file_uploader("Choose a file", type=['csv', 'xlsx', 'xls', 'json', 'txt'])

if uploaded_file is not None:
    df = load_file(uploaded_file)
    if df is not None:
        # Sidebar for interactive controls
        st.sidebar.header("Cleaning Options")
        operations = {
            'remove_duplicates': st.sidebar.checkbox("Remove Duplicates", value=True),
            'fill_missing': st.sidebar.checkbox("Fill Missing Values", value=True),
            'convert_dates': st.sidebar.checkbox("Convert to Dates", value=True),
            'remove_outliers': st.sidebar.checkbox("Remove Outliers", value=False)
        }
        fill_method = st.sidebar.selectbox("Fill Method for Missing Values", ['Mean', 'Median', 'Mode']) if operations['fill_missing'] else None
        outlier_threshold = st.sidebar.slider("Outlier IQR Multiplier", 1.0, 3.0, 1.5) if operations['remove_outliers'] else 1.5
        show_viz = st.sidebar.checkbox("Show Visualizations", value=True)
        
        # Data Quality Assessment
        st.subheader("Data Quality Assessment")
        quality = assess_data_quality(df)
        with st.expander("View Quality Metrics"):
            st.write(f"**Total Rows:** {quality['Total Rows']}")
            st.write(f"**Total Columns:** {quality['Total Columns']}")
            st.write("**Missing Values per Column:**")
            st.json(quality['Missing Values'])
            st.write(f"**Duplicate Rows:** {quality['Duplicate Rows']}")
            st.write("**Data Types:**")
            st.json(quality['Data Types'])
            if quality['Numeric Stats'] != "No numeric columns":
                st.write("**Numeric Column Statistics:**")
                st.json(quality['Numeric Stats'])
        
        # Visualizations
        if show_viz:
            st.subheader("Data Quality Visualizations")
            col1, col2 = st.columns(2)
            with col1:
                missing_fig = px.bar(x=list(quality['Missing Values'].keys()), y=list(quality['Missing Values'].values()), title="Missing Values per Column")
                st.plotly_chart(missing_fig)
            with col2:
                if quality['Numeric Stats'] != "No numeric columns":
                    numeric_df = df.select_dtypes(include=['number'])
                    if not numeric_df.empty:
                        fig = px.histogram(numeric_df, title="Numeric Column Distributions")
                        st.plotly_chart(fig)
        
        st.subheader("Original Data Preview")
        st.dataframe(df.head())
        
        if st.button("Apply Cleaning"):
            cleaned_df, changes = clean_data(df.copy(), operations, fill_method, outlier_threshold)
            st.subheader("Cleaning Summary")
            if changes:
                st.write("**Operations Performed and Changes:**")
                for change in changes:
                    st.write(f"- {change}")
            else:
                st.write("No changes were applied based on selected options.")
            
            # After visualizations
            if show_viz:
                st.subheader("Post-Cleaning Visualizations")
                cleaned_quality = assess_data_quality(cleaned_df)
                col1, col2 = st.columns(2)
                with col1:
                    cleaned_missing_fig = px.bar(x=list(cleaned_quality['Missing Values'].keys()), y=list(cleaned_quality['Missing Values'].values()), title="Missing Values After Cleaning")
                    st.plotly_chart(cleaned_missing_fig)
                with col2:
                    if cleaned_quality['Numeric Stats'] != "No numeric columns":
                        cleaned_numeric_df = cleaned_df.select_dtypes(include=['number'])
                        if not cleaned_numeric_df.empty:
                            fig = px.histogram(cleaned_numeric_df, title="Numeric Distributions After Cleaning")
                            st.plotly_chart(fig)
            
            st.subheader("Cleaned Data Preview")
            st.dataframe(cleaned_df.head())
            
            # Download option
            csv = cleaned_df.to_csv(index=False)
            st.download_button(
                label="Download Cleaned CSV",
                data=csv,
                file_name="cleaned_data.csv",
                mime="text/csv"
            )