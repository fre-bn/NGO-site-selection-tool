import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from math import pi

# Configure the Streamlit page
st.set_page_config(
    page_title="Marine Conservation Community Assessment",
    layout="wide"
)

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
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    
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
    ax.set_xticklabels(categories, fontsize=10)
    
    # Set y-axis limits and labels
    ax.set_ylim(0, 10)
    ax.set_yticks(range(0, 11, 2))
    ax.set_yticklabels(range(0, 11, 2), fontsize=8)
    ax.grid(True)
    
    # Add legend
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
    
    # Add title
    plt.title('NGO-Community Fit Assessment\nMarine Conservation Strategy', 
              size=16, fontweight='bold', pad=20)
    
    return fig

def main():
    st.title(" Marine Conservation Community Assessment")
    st.markdown("### Evaluate the fit between NGO capabilities and community capacities")
    
    # Define the sustainability themes
    themes = [
        'Generational Development',
        'Community Cohesion', 
        'Tradition Preservation',
        'Infrastructure',
        'Employment',
        'Revenue',
        'Habitat Conservation',
        'Shark Population',
        'Protected Land'
    ]
    
    # Define constant NGO capabilities (you can adjust these values)
    ngo_capabilities = [5, 4, 5, 3, 4, 2, 4, 6, 6]  # Example values
    
    # Create two columns
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.header("Community Capacity Assessment")
        st.markdown("*Use the sliders below to assess the community's current capacity in each sustainability theme.*")
        
        # Create sliders for community capacities
        community_capacities = []
        
        for i, theme in enumerate(themes):
            capacity = st.slider(
                f"{theme}",
                min_value=0,
                max_value=10,
                value=0,  # Default value
                step=1,
                help=f"Rate the community's current capacity in {theme.lower()} (0 = Very Low, 10 = Very High)"
            )
            community_capacities.append(capacity)
        
        # Display NGO capabilities info
        st.header("NGO Capabilities")
        st.markdown("*These represent the organization's established strengths:*")
        
        for i, (theme, capability) in enumerate(zip(themes, ngo_capabilities)):
            st.markdown(f"**{theme}:** {capability}/10")
    
    with col2:
        st.header("Fit Assessment Visualization")
        
        # Create and display the radar chart
        fig = create_radar_chart(ngo_capabilities.copy(), community_capacities.copy(), themes)
        st.pyplot(fig)
        
        # Add interpretation
        st.markdown("### Interpretation Guide")
        st.markdown("""
        - **Blue area (NGO Capability)**: Shows the organization's strengths radiating from the center
        - **Green area (Community Capacity)**: Shows community strengths radiating from the outer edge inward
        - **Overlap areas**: Indicate strong alignment between NGO capabilities and community needs
        - **Gaps**: Areas where there's little overlap may require additional support or different approaches
        """)
        
        # Calculate and display fit score
        fit_scores = []
        for ngo_cap, comm_cap in zip(ngo_capabilities[:-1], community_capacities):  # Exclude duplicate first element
            # Calculate how well they complement each other
            # Higher scores when both are high or when they balance each other
            fit_score = min(ngo_cap, comm_cap) + (abs(ngo_cap - comm_cap) * 0.1)
            fit_scores.append(fit_score)
        
        overall_fit = np.mean(fit_scores)
        
        st.metric(
            label="Overall Fit Score", 
            value=f"{overall_fit:.1f}/10",
            help="Higher scores indicate better alignment between NGO capabilities and community capacities"
        )
        
        # Recommendations based on fit score
        if overall_fit >= 8:
            st.success("🎯 Excellent fit! This community shows strong alignment with the NGO's capabilities.")
        elif overall_fit >= 6:
            st.warning("⚖️ Good fit with some areas for development. Consider targeted capacity building.")
        else:
            st.error("⚠️ Limited fit. This community may require significant preliminary work or alternative approaches.")

if __name__ == "__main__":
    main()