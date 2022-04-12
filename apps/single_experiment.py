from typing import Any
from typing import Union
from pandas import DataFrame
import streamlit
import pandas
from apps.render_first_dataframe import first_dataframe
from apps.render_basic_plots import render_label_based_plot, render_size_signal_plot, render_sizes_plot_histogram, \
    render_signal_plot
from apps.render_second_dataframe import calculate_total_object_and_other, calculate_total_positive_in_each_label, \
    calculate_total_negative_in_each_label, calculate_average_volume, listing_labels_in_the_dataframe
from apps.render_growth_heterogeneity import render_required_antibiotic_concentration_range, \
    render_growth_heterogeneity_module
from apps.render_polydisperse_analysis import render_size_distribution_in_polydisperse_module
from apps.render_threshold import render_threshold
from apps.upload_data import data_frame_by_rendering_file_upload_section


def page():
    # Initialize page and get uploaded file data
    data_frame: Union[dict[Any, DataFrame], DataFrame, None] = data_frame_by_rendering_file_upload_section()

    if data_frame is None:
        return
    #streamlit.write(data_frame.head())
    # Display table with the uploaded data
    # Calculating the average, radian, and volume which will be used in the calculation
    first_dataframe(data_frame)

    if data_frame is not TypeError or ValueError or KeyError:
    # Graphs starting here
        try:
            streamlit.header("Data Visualization")

            column1, column2, column3 = streamlit.columns(3)
            threshold = render_threshold(column1, data_frame)
            column1.warning("This threshold will change the visualization below.")

            with streamlit.expander("More information about the threshold", expanded=False):
                streamlit.write("The threshold will be shown as a red line within figures below. "
                                "This threshold also determines the classification between two types"
                                "of droplets.")

            #These render the basic modules

            render_signal_plot(data_frame, threshold)
            render_sizes_plot_histogram(data_frame)
            render_size_signal_plot(data_frame, threshold)
            render_label_based_plot(data_frame, threshold)
        except:
            streamlit.warning("Please adjust the file input accordingly. For further explanation, check the 'Instruction' tab")

        streamlit.header("")

        streamlit.button("Download Data")

        streamlit.header("Specific-case module")
        try:
            if 'type' not in streamlit.session_state or 'hetero' not in streamlit.session_state:
                streamlit.session_state['type'] = 'Select here'
                streamlit.session_state['hetero'] = 'Growth heterogeneity'
                streamlit.session_state['poly'] = 'Polydisperse droplet analysis'

            def handle_click(new_type):
                streamlit.session_state.type = new_type

            def wo_click():
                if streamlit.session_state.kind_of_column:
                    streamlit.session_state.type = streamlit.session_state.kind_of_column

            column1, column2 = streamlit.columns(2)
            module = column1.selectbox(
                "What module do you want to visualize?",
                ['Select here', 'Growth heterogeneity', 'Polydisperse droplet analysis'],
                on_change=wo_click, key='kind_of_column'
            )
            type_module = {
                'Select here': ['Select specific module'],
                'Growth heterogeneity': ['Gompertz fitting', 'Single cell viability and MIC probability density'],
                'Polydisperse droplet analysis': ['Size Distribution']
            }
            type_of_column = column1.selectbox("What kind of visualization?", type_module[streamlit.session_state['type']])
            if type_module is not 'Select here':
                label = data_frame['Label']

                detected_labels, second_dataframe = listing_labels_in_the_dataframe(data_frame, label)

                calculate_average_volume(data_frame, detected_labels, label, second_dataframe, data_frame['Volume'])
                calculate_total_negative_in_each_label(data_frame, detected_labels, label, second_dataframe, data_frame['Volume'])
                calculate_total_positive_in_each_label(data_frame, detected_labels, label, second_dataframe, data_frame['Volume'])
                calculate_total_object_and_other(second_dataframe)


                if module == 'Growth heterogeneity':
                    ab_input = render_required_antibiotic_concentration_range()
                    if ab_input:
                        render_growth_heterogeneity_module(ab_input, second_dataframe, type_of_column)

                if module == 'Polydisperse droplet analysis':
                    if type_of_column == 'Size Distribution':
                        render_size_distribution_in_polydisperse_module(data_frame, second_dataframe)
        except:
            streamlit.warning("Please adjust the file input accordingly. For further explanation, check the 'Instruction' tab")




