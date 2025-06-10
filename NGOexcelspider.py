import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from math import pi

# Configure the Streamlit page
st.set_page_config(
    page_title="Marine Conservation Community Assessment",
    page_icon="🌊",
    layout="wide"
)

def load_data_from_csv(uploaded_file):
    """
   

    Load data from uploaded CSV file
    Expected format:
    - Column 1: Theme names
    - Column 2: Community capacity values
    - Column 3: NGO capability values
    First row can be headers (will be skipped)
    """
    try:
        # Read CSV file
        df = pd.read_csv(uploaded_file)
        
        # Check if we have at least 3 columns
        if df.shape[1] < 3:
            st.error("Error: CSV file must have at least 3 columns (Theme, Community Capacity, NGO Capability)")
            return None, None, None
        
        # Skip header row if it exists (check if first row contains non-numeric values in columns 2 and 3)
        start_row = 0
        try:
            # Try to convert first row's second and third columns to float
            pd.to_numeric(df.iloc[0, 1])
            pd.to_numeric(df.iloc[0, 2])
        except (ValueError, TypeError):
            # First row is likely headers, skip it
            start_row = 1
        
        # Extract data from the appropriate rows
        end_row = start_row + 9
        
        if df.shape[0] < end_row:
            st.error(f"Error: CSV file must have at least {9 + start_row} rows of data (including headers if present)")
            return None, None, None
        
        themes = df.iloc[start_row:end_row, 0].tolist()  # Column 1
        community_capacities = df.iloc[start_row:end_row, 1].tolist()  # Column 2
        ngo_capabilities = df.iloc[start_row:end_row, 2].tolist()  # Column 3
        
        # Validate data length
        if len(themes) != 9 or len(community_capacities) != 9 or len(ngo_capabilities) != 9:
            st.error("Error: Expected exactly 9 rows of data")
            return None, None, None
        
        # Convert numeric values and validate
        try:
            community_capacities = [float(x) for x in community_capacities]
            ngo_capabilities = [float(x) for x in ngo_capabilities]
        except (ValueError, TypeError) as e:
            st.error(f"Error: All capacity values must be numeric. Found non-numeric value.")
            return None, None, None
        
        # Check if values are within valid range (0-10)
        for i, (comm_cap, ngo_cap) in enumerate(zip(community_capacities, ngo_capabilities)):
            if not (0 <= comm_cap <= 10) or not (0 <= ngo_cap <= 10):
                st.error(f"Error: Values in row {i + start_row + 1} are out of range. All values must be between 0 and 10.")
                return None, None, None
        
        return themes, community_capacities, ngo_capabilities
        
    except Exception as e:
        st.error(f"Error reading CSV file: {str(e)}")
        return None, None, None

def create_radar_chart(ngo_capabilities, community_capacities, categories):
    """
    Create a radar chart comparing NGO capabilities with community capacities
    """
    # Number of variables
    N = len(categories)
    
    # Compute angle for each axis
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]  # Complete the circle
    
    # Add the first value to the end to close the radar chart
    ngo_capabilities += ngo_capabilities[:1]
    community_capacities += community_capacities[:1]
    
    # Create the figure
    fig, ax = plt.subplots(figsize=(12, 12), subplot_kw=dict(projection='polar'))
    
    # NGO Capabilities (from center outward) - Blue
    ax.plot(angles, ngo_capabilities, 'o-', linewidth=2, label='NGO Capability', color='#1f77b4')
    ax.fill(angles, ngo_capabilities, alpha=0.25, color='#1f77b4')
    
    # Community Capacities (from outside inward) - Green
    # Create the outer boundary (max ring) and fill inward based on capacity
    max_value = 10
    community_outer = [max_value] * len(community_capacities)
    community_fill_values = [max_value - val for val in community_capacities]
    
    # Plot the outer ring for community capacity
    ax.plot(angles, community_outer, '-', linewidth=1, alpha=0.3, color='#2ca02c')
    
    # Fill from outer ring inward based on capacity values
    # We create the filled area by plotting from max_value down to (max_value - capacity)
    ax.fill_between(angles, community_outer, community_fill_values, 
                   alpha=0.25, color='#2ca02c', label='Community Capacity')
    
    # Plot the inner boundary line for community capacity
    ax.plot(angles, community_fill_values, 'o-', linewidth=2, color='#2ca02c')
    
    # Add category labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=9, wrap=True)
    
    # Set y-axis limits and remove default labels
    ax.set_ylim(0, 10)
    ax.set_yticks(range(0, 11))
    ax.set_yticklabels([])  # Remove default labels
    ax.grid(True)
    
    # Add custom numbered labels for NGO capabilities (blue, from center outward)
    for i in range(1, 11):
        ax.text(0, i, str(i), color='#1f77b4', fontweight='bold', 
                ha='center', va='center', fontsize=8)
    
    # Add custom numbered labels for community capacities (green, from outside inward)
    for i in range(1, 11):
        # Position these at a different angle to avoid overlap
        angle_offset = pi/N  # Offset by half the angular spacing
        ax.text(angle_offset, 10-i+1, str(i), color='#2ca02c', fontweight='bold',
                ha='center', va='center', fontsize=8)
    
    # Add legend
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
    
    # Add title
    plt.title('NGO-Community Fit Assessment\nMarine Conservation Strategy', 
              size=16, fontweight='bold', pad=20)
    
    return fig

def main():
    st.title("🌊 Marine Conservation Community Assessment")
    st.markdown("### Evaluate the fit between NGO capabilities and community capacities")
    
    # File upload section
    st.header("📁 Upload Assessment Data")
    st.markdown("""
                
     Hi visitor! Great to see that you have an ecotourism project running.
    We would like to help you with the leap into unknown territory; the selection of new project sites for developing more projects.
    Alternatively, the app can be used for a check-up of a current project. 

    Tourism can be of great benefit or detriment to an area. Therefore, ecotourism aims to ensure benefits to not only the tourism business, 
    but also that of the natural resource and the community that has traditionally managed the resource. 
    Because the situation in every area is different, determining the right strategy can be a complex task.
    Based on academic marine ecotourism literature, we have created a holistic assessment rubric with the three pillars of sustainability in mind 
    to guarentee that also future generations can enjoy the cultural and natural wonders (see file in the github package).
    This tool is developed to communicate the suitability of an ecoutourism strategy from the results of the assessments.
    For every theme, we show the fit and give suggestions on possible improvements. 
    Show what is on your radar!

    -Lieke, Malik, Javier, Lars and Frederique
   (This project is open source and part of a consultancy project of Msc Sustainable development students)


  **Upload a CSV file (.csv) with the following format:**
    - **Column 1**: Theme names
    - **Column 2**: Community capacity values (0-10)
    - **Column 3**: NGO capability values (0-10)
    
    *Note: First row can contain headers (they will be automatically detected and skipped)*
    """)
    
    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
    
    if uploaded_file is not None:
        # Load data from uploaded file
        themes, community_capacities, ngo_capabilities = load_data_from_csv(uploaded_file)
        
        if themes is not None and community_capacities is not None and ngo_capabilities is not None:
            # Display loaded data in a preview table
            st.header("📊 Loaded Data Preview")
            preview_df = pd.DataFrame({
                'Theme': themes,
                'Community Capacity': community_capacities,
                'NGO Capability': ngo_capabilities
            })
            st.dataframe(preview_df)
            
            # Create two columns for layout
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("### Interpretation Guide")
                st.markdown("""
                - **Blue area (NGO Capability)**: Shows the organization's strengths radiating from the center (numbered 1-10 in blue)
                - **Green area (Community Capacity)**: Shows community strengths radiating from the outer edge inward (numbered 1-10 in green)
                - **Overlap areas**: Indicate possible redundancies in efforts of NGO capabilities and community needs
                - **Gaps**: Areas where there's little overlap may require additional support or different approaches
                """)
            
            with col2:
                st.header("Fit Assessment Visualization")
                
                # Create and display the radar chart
                fig = create_radar_chart(ngo_capabilities.copy(), community_capacities.copy(), themes)
                st.pyplot(fig)
                
    
               
                
                # Calculate and display scores for each theme
                st.markdown("### Theme-by-Theme Assessment")
                
                # Define strategic recommendations for each theme
                strategic_recommendations = {
                    '1.1 Awareness & Education': "improving communication on the effects of conservation, or reaching out to younger generations",
                    '1.2 Community Governance': "strengthening ties with community members to gain trust",
                    '1.3 Tradition Preservation': "collaborating with the community to include traditional elements in ecotourism",
                    '2.1 Income & Revenue': "adapting business model to increase the portion of the revenue reserved for tour guide salaries and conservation",
                    '2.2 Employment': "offer employment to more local residents with opportunities to develop skills and expertise",
                    '2.3 Amenities': "improve infrastructure for the daily lives of residents and adapt it to accommodate tourists",
                    '3.1 Habitat Conservation': "creating habitat improvements for the natural resource",
                    '3.2 Shark Preservation': "strengthening fishing conservation efforts",
                    '3.3 Protected Area': "strengthening and implementing area protection regulations"
                }
                
                for i, theme in enumerate(themes):
                    ngo_cap = ngo_capabilities[i]
                    comm_cap = community_capacities[i]
                    score = -10 + ngo_cap + comm_cap
                    
                    col_theme, col_score, col_comment = st.columns([2, 1, 3])
                    
                    with col_theme:
                        st.markdown(f"**{theme}**")
                    
                    with col_score:
                        if score == 0:
                            st.markdown(f"<span style='color: green; font-weight: bold;'>{score}</span>", unsafe_allow_html=True)
                        elif score > 0:
                            st.markdown(f"<span style='color: orange; font-weight: bold;'>{score}</span>", unsafe_allow_html=True)
                        elif score < -2:
                            st.markdown(f"<span style='color: red; font-weight: bold;'>{score}</span>", unsafe_allow_html=True)
                        else:  # -2 <= score < 0
                            st.markdown(f"<span style='color: blue; font-weight: bold;'>{score}</span>", unsafe_allow_html=True)
                    
                    with col_comment:
                        if score == 0:
                            st.success("Congratulations! On this theme, the project seems to be suitable for this community.")
                        elif score > 0:
                            st.warning("The capacity and capability seems to overlap for this theme. The added benefit from the NGO's strategy may be negated. Strategic effort should be placed on other themes.")
                        elif score < -2:
                            st.error("There is a gap between the community context and the strategy of the NGO. It might be indicative of a bad fit.")
                        else:  # -2 <= score < 0
                            # Use the theme name from the uploaded file to find the recommendation
                            recommendation = None
                            for key, value in strategic_recommendations.items():
                                if key.lower() in theme.lower() or any(word in theme.lower() for word in key.lower().split()):
                                    recommendation = value
                                    break
                            
                            if recommendation is None:
                                recommendation = "general strategic adjustments"
                            
                            st.info(f"There is a gap between the community context and the strategy of the NGO. This could potentially be solved by changing the strategy to include: {recommendation}")
                
                # Calculate overall assessment
                #all_scores = [-10 + ngo_capabilities[i] + community_capacities[i] for i in range(len(themes))]
               # avg_score = np.mean(all_scores)
                
              #  st.markdown("### Overall Assessment")
              #  st.metric(
              #      label="Average Theme Score", 
              #      value=f"{avg_score:.1f}",
              #      help="Average of all theme scores (-10 + NGO capability + Community capacity)"
              #  )
    
    #else:
        # Show example format when no file is uploaded
      #  st.header("📋 Example CSV Format")
      #  st.markdown("Here's an example of how your CSV file should be structured:")
        
      #  example_data = {
     #       'Theme': ['1.1 Awareness & Education', '1.2 Community Governance', '1.3 Tradition Preservation',
      #                '2.1 Income & Revenue', '2.2 Employment', '2.3 Amenities', 
       #               '3.1 Habitat Conservation', '3.2 Shark Preservation', '3.3 Protected Area'],
        #    'Community Capacity': [7, 5, 8, 6, 4, 5, 9, 7, 8],
         #   'NGO Capability': [8, 6, 7, 5, 7, 4, 9, 8, 9]
       # }
        
      #  example_df = pd.DataFrame(example_data)
     #   st.dataframe(example_df)
        
        st.markdown("""
        **Instructions:**
        1. Create a CSV file (.csv) with the format shown above
        2. Column 1: Theme names
        3. Column 2: Community capacity values 0-10
        4. Column 3: NGO capability values 0-10
        5. Headers are optional (will be automatically detected)
        6. Upload the file using the file uploader above
        """)
        
        # Provide download link for example template
    #    st.markdown("### 📥 Download Template")
    #    csv_data = example_df.to_csv(index=False)
    #    st.download_button(
    #        label="Download CSV Template",
      #      data=csv_data,
      #      file_name="marine_assessment_template.csv",
     #       mime="text/csv"
     #   )
    
    # Footer
    st.markdown("---")
    st.markdown("*Marine Conservation Community Assessment Tool - Upload your CSV data to begin analysis*")

if __name__ == "__main__":
    main()