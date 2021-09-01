# AUTOGENERATED! DO NOT EDIT! File to edit: 03_gui.ipynb (unless otherwise specified).

__all__ = ['STYLE', 'LAYOUT', 'INITIAL_WIDGET_PARAMS', 'Gui', 'Select_stats_widget', 'Select_plots_widget',
           'Select_downloads_widget', 'Customization_widget', 'Customize_annotations', 'Select_annotations',
           'Customize_y_axis', 'Customize_x_axis', 'Customize_both_axes', 'Customize_other_features']

# Cell
from dcl_stats_n_plots import stats
from dcl_stats_n_plots import plots

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import itertools

import ipywidgets as w
from IPython.display import display

# Cell
STYLE = {'description_width': 'initial'}
LAYOUT = {'width': '100%'} # no longer needed?

# Cell

# Initial params:
INITIAL_WIDGET_PARAMS = {'uploader': {'visibility': 'visible'},
                         'stats_button': {'visibility': 'visible'},
                         'plots_button': {'visibility': 'hidden',
                                          'description': 'Plot the data'},
                         'downloads_button': {'visibility': 'hidden'},

                         'stats_dropdown': {'options': [('Pairwise comparison of two or more independent samples', 0),
                                                        ('Comparison of one group against a fixed value (one-sample test)', 1),
                                                        ('Mixed_model_ANOVA', 2)],
                                            'visibility': 'visible',
                                            'value': 0},
                         'plots_dropdown': {'options': [('something initial', 0)],
                                            'visibility': 'hidden',
                                            'value': 0},
                         'downloads_dropdown': {'visibility': 'hidden',
                                                'value': 2},
                         'customization_accordion': {'visibility': 'hidden'},
                         'set_xlabel_order': {'visibility': 'hidden',
                                              'value': ' '},
                         'set_hue_order': {'visibility': 'hidden',
                                              'value': ' '},
                         'group_colors_vbox': {'children': ()}}

# Cell
class Gui:
    "Top-level outline of the GUI"
    def __init__(self):
        self.params = self.set_initial_params()

        # Widgets, Output, and Layout
        self.uploader = w.FileUpload(accept=('.xlsx, .csv'), multiple=False)
        self.stats_selection = Select_stats_widget(self.params)
        self.plots_selection = Select_plots_widget(self.params)
        self.customization = Customization_widget()
        self.downloads_selection = Select_downloads_widget(self.params)

        self.out = w.Output()
        self.widget = w.VBox([self.uploader,
                              self.stats_selection.widget,
                              self.plots_selection.widget,
                              self.customization.widget,
                              self.downloads_selection.widget,
                              self.out])

        # Link buttons
        self.stats_selection.button.on_click(self.on_stats_button_clicked)
        self.plots_selection.button.on_click(self.on_plots_button_clicked)
        self.downloads_selection.button.on_click(self.on_downloads_button_clicked)


    ## Methods to initialize or update the params, or to update the widgets accordingly
    # Initialzie params
    def set_initial_params(self):
        params = {'data': None, # will be updated when data is uploaded
                  'results': None, # will be updated when statistics are computed
                  'save_plot': False,
                  'widgets': INITIAL_WIDGET_PARAMS}
        return params

    # Update params
    def get_updated_params(self):


        # Dropdowns
        self.params['widgets']['stats_dropdown']['value'] = self.stats_selection.dropdown.value
        self.params['widgets']['plots_dropdown']['value'] = self.plots_selection.dropdown.value
        self.params['widgets']['downloads_dropdown']['value'] = self.downloads_selection.dropdown.value


        # Customization
        self.params['set_fig_width'] = self.customization.other_features.set_fig_width.value
        self.params['set_fig_height'] = self.customization.other_features.set_fig_height.value
        self.params['set_marker_size'] = self.customization.other_features.set_marker_size.value
        self.params['set_show_legend'] = self.customization.other_features.set_show_legend.value

        self.params['set_axes_linewidth'] = self.customization.both_axes.set_axes_linewidth.value
        self.params['set_axes_color'] = self.customization.both_axes.set_axes_color.value
        self.params['set_axes_tick_size'] = self.customization.both_axes.set_axes_tick_size.value


        self.params['set_yaxis_label_text'] = self.customization.yaxis.set_yaxis_label_text.value
        self.params['set_yaxis_label_fontsize'] = self.customization.yaxis.set_yaxis_label_fontsize.value
        self.params['set_yaxis_label_color'] = self.customization.yaxis.set_yaxis_label_color.value
        self.params['set_yaxis_scaling_mode'] = self.customization.yaxis.set_yaxis_scaling_mode.value
        self.params['set_yaxis_lower_lim_value'] = self.customization.yaxis.set_yaxis_lower_lim.value
        self.params['set_yaxis_upper_lim_value'] = self.customization.yaxis.set_yaxis_upper_lim.value

        self.params['set_xaxis_label_color'] = self.customization.xaxis.set_xaxis_label_color.value
        self.params['set_xaxis_label_fontsize'] = self.customization.xaxis.set_xaxis_label_fontsize.value
        self.params['set_xaxis_label_text'] = self.customization.xaxis.set_xaxis_label_text.value

        self.params['distance_stars_to_brackets'] = self.customization.customize_annotations.set_distance_stars_to_brackets.value
        self.params['distance_brackets_to_data'] = self.customization.customize_annotations.set_distance_brackets_to_data.value
        self.params['fontsize_stars'] = self.customization.customize_annotations.set_fontsize_stars.value
        self.params['linewidth_annotations'] = self.customization.customize_annotations.set_linewidth_annotations.value
        if self.customization.customize_annotations.select_bracket_no_bracket.value == 'Brackets':
            self.params['annotation_brackets_factor'] = 1
        else:
            self.params['annotation_brackets_factor'] = 0
        if self.customization.customize_annotations.set_stars_fontweight_bold.value == True:
            self.params['fontweight_stars'] = 'bold'
        else:
            self.params['fontweight_stars'] = 'normal'

        if self.customization.other_features.select_palette_or_individual_color.value == 0:
            self.params['color_palette'] = self.customization.other_features.select_color_palettes.value
        else:
            color_palette = {}
            for group_id in self.params['l_groups']:
                color_palette[group_id] = self.customization.other_features.group_colors_vbox.children[self.params['l_groups'].index(group_id)].value
            self.params['color_palette'] = color_palette



        l_xlabel_order = []
        l_xlabel_string = self.customization.xaxis.set_xlabel_order.value
        while ', ' in l_xlabel_string:
            l_xlabel_order.append(l_xlabel_string[:l_xlabel_string.index(', ')])
            l_xlabel_string = l_xlabel_string[l_xlabel_string.index(', ')+2:]
        l_xlabel_order.append(l_xlabel_string)
        self.params['l_xlabel_order'] = l_xlabel_order

        l_hue_order = []
        l_hue_string = self.customization.xaxis.set_hue_order.value

        while ', ' in l_hue_string:
            l_hue_order.append(l_hue_string[:l_hue_string.index(', ')])
            l_hue_string = l_hue_string[l_hue_string.index(', ')+2:]

        l_hue_order.append(l_hue_string)

        self.params['l_hue_order'] = l_hue_order



    # Update widgets according to params
    def set_updated_params(self):
        # Buttons
        self.stats_selection.button.layout.visibility = self.params['widgets']['stats_button']['visibility']
        self.plots_selection.button.layout.visibility = self.params['widgets']['plots_button']['visibility']
        self.plots_selection.button.description = self.params['widgets']['plots_button']['description']
        self.downloads_selection.button.layout.visibility = self.params['widgets']['downloads_button']['visibility']
        self.uploader.layout.visibility = self.params['widgets']['uploader']['visibility']

        # Dropdowns
        self.plots_selection.dropdown.layout.visibility = self.params['widgets']['plots_dropdown']['visibility']
        self.plots_selection.dropdown.options = self.params['widgets']['plots_dropdown']['options']
        self.downloads_selection.dropdown.layout.visibility = self.params['widgets']['downloads_dropdown']['visibility']

        # Customization
        self.customization.widget.layout.visibility = self.params['widgets']['customization_accordion']['visibility']

        ## Customize annotations
        if len(self.customization.select_annotations.select_annotations_vbox.children) == 0:
            self.customization.select_annotations.select_annotations_vbox.children = self.customization.select_annotations.select_annotations_vbox.children + self.params['checkboxes_to_add']

        ## Customize axes
        ### x-axis
        self.customization.xaxis.set_xlabel_order.value = self.params['widgets']['set_xlabel_order']['value']
        self.customization.xaxis.set_xlabel_order.layout.visibility = self.params['widgets']['set_xlabel_order']['visibility']
        self.customization.xaxis.set_hue_order.value = self.params['widgets']['set_hue_order']['value']
        self.customization.xaxis.set_hue_order.layout.visibility = self.params['widgets']['set_hue_order']['visibility']
        ### y-axis
        self.customization.yaxis.set_yaxis_lower_lim.value = self.params['set_yaxis_lower_lim_value']
        self.customization.yaxis.set_yaxis_upper_lim.value = self.params['set_yaxis_upper_lim_value']

        ## Customize other features
        if len(self.customization.other_features.group_colors_vbox.children) == 0:
            self.customization.other_features.group_colors_vbox.children = self.params['widgets']['group_colors_vbox']['children']


    ## Methods to define button functions
    # Stats button
    def on_stats_button_clicked(self, b):

        self.get_updated_params()

        # Read the data that was selected using the uploader:
        if list(self.uploader.value.keys())[0].endswith('.csv'):
            with open("input.csv", "w+b") as i:
                i.write(self.uploader.value[list(self.uploader.value.keys())[0]]['content'])
            df = pd.read_csv('input.csv', index_col=0)

        elif list(self.uploader.value.keys())[0].endswith('.xlsx'):
            with open("input.xlsx", "w+b") as i:
                i.write(self.uploader.value[list(self.uploader.value.keys())[0]]['content'])
            df = pd.read_excel('input.xlsx', index_col=0)

        self.params['data'] = df

        with self.out:
            self.out.clear_output()
            # This will create & display whatever is defined as output and allow the bound on_click function to return params
            self.params = self.stats_selection.on_button_clicked(self.params)
            display(self.params['results']['summary']['pairwise_comparisons'])

        # Finally, update all widgets according to the newly specified params:
        self.set_updated_params()


    # Plots button
    def on_plots_button_clicked(self, b):
        self.get_updated_params()

        with self.out:
            self.out.clear_output()
            self.params = self.plots_selection.on_button_clicked(self.params)

        # Finally, update all widgets according to the newly specified params:
        self.set_updated_params()

    # Downloads button
    def on_downloads_button_clicked(self, b):
        pass

# Cell
class Select_stats_widget:
    "Creates the part of the widget that allows to select what statistical comparison shall be made"
    def __init__(self, params):
        self.dropdown = w.Dropdown(description = 'Please select which test you want to perform:',
                                   options = params['widgets']['stats_dropdown']['options'],
                                   value = params['widgets']['stats_dropdown']['value'],
                                   layout = {'width': '100%',
                                             'visibility': params['widgets']['stats_dropdown']['visibility']},
                                   style = STYLE)
        self.button = w.Button(description = "Calculate stats", icon = 'rocket', layout = {'visibility': params['widgets']['stats_button']['visibility']})
        self.widget = w.HBox([self.dropdown, self.button])


    def on_button_clicked(self, params):

        stats_value = params['widgets']['stats_dropdown']['value']
        df = params['data']

        # Update params values
        params['widgets']['uploader']['visibility'] = 'hidden'
        params['widgets']['plots_button']['visibility'] = 'visible'
        params['widgets']['plots_dropdown']['visibility'] = 'visible'
        params['widgets']['downloads_button']['visibility'] = 'visible'
        params['widgets']['downloads_dropdown']['visibility'] = 'visible'
        params['widgets']['customization_accordion']['visibility'] = 'visible'

        if stats_value == 0: # comparison of independent samples
            params['widgets']['plots_dropdown']['options'] = [('stripplot', 0),
                                                              ('boxplot', 1),
                                                              ('boxplot with scatterplot overlay', 2),
                                                              ('violinplot', 3)]
        elif stats_value == 1: # one-sample test:
            params['widgets']['plots_dropdown']['options'] = [('sripplot', 0),
                                                              ('boxplot', 1),
                                                              ('boxplot with scatterplot overlay', 2),
                                                              ('violinplot', 3),
                                                              ('histogram', 4)]
        elif stats_value == 2: # mixed-model ANOVA
            params['widgets']['plots_dropdown']['options'] = [('pointplot', 0),
                                                              ('boxplot', 1),
                                                              ('boxplot with scatterplot overlay', 2),
                                                              ('violinplot', 3)]
        else:
            print('Function not implemented. Please go and annoy Dennis to finally do it')

        if stats_value == 0:
            params['data_col'], params['group_col'], params['results'], params['l_groups'], params['performed_test'] = stats.independent_samples(df)
            params = self.create_checkboxes_pairwise_comparisons(params)
        elif stats_value == 1:
            params['data_col'], params['group_col'], params['results'], params['l_groups'], params['performed_test'], params['fixed_val_col'], params['fixed_value'] = stats.one_sample(df)
            params = self.create_checkboxes_pairwise_comparisons()
        elif stats_value == 2:
            params['results'], params['data_col'], params['group_col'], params['subject_col'], params['session_col'], params['l_groups'], params['l_sessions'], params['performed_test'] = stats.mixed_model_ANOVA(df)
            params = self.create_checkboxes_pairwise_comparisons_mma(params)

        params = self.create_group_order_text(params, stats_value)
        params = self.create_ylims(params, df, params['data_col'])
        params = self.create_group_color_pickers(params, params['l_groups'])

        return params


    def create_checkboxes_pairwise_comparisons(self, params):
        l_groups = params['l_groups']

        if len(l_groups) == 1:
            fixed_val_col = params['fixed_val_col']
            l_checkboxes = [w.Checkbox(value=False,description='{} vs. {}'.format(l_groups[0], fixed_val_col))]
        else:
            # Create a checkbox for each pairwise comparison
            l_checkboxes = [w.Checkbox(value=False,description='{} vs. {}'.format(group1, group2))
                                 for group1, group2 in list(itertools.combinations(l_groups, 2))]
        # Arrange checkboxes in a HBoxes with up to 3 checkboxes per HBox
        l_HBoxes = []
        elem = 0
        for i in range(int(len(l_checkboxes)/3)):
            l_HBoxes.append(w.HBox(l_checkboxes[elem:elem+3]))
            elem = elem + 3

        if len(l_checkboxes) % 3 != 0:
            l_HBoxes.append(w.HBox(l_checkboxes[elem:]))

        # Arrange HBoxes in a VBox and select all as tuple to later place in empty placeholder (select_annotations_vbox)
        params['checkboxes_to_add'] = w.VBox(l_HBoxes).children[:]
        params['l_checkboxes'] = l_checkboxes

        return params


    def create_checkboxes_pairwise_comparisons_mma(self, params):
        l_sessions = params['l_sessions']

        annotate_session_stats_accordion = w.Accordion(children=[], selected_index=None)
        l_all_checkboxes = []

        for session_id in l_sessions:
            params = self.create_checkboxes_pairwise_comparisons(params)
            # Little complicated, but neccessary since the output of create_checkboxes_pairwise_comparisons() is a tuple
            checkboxes_to_add_temp_vbox = w.VBox([])
            checkboxes_to_add_temp_vbox.children = checkboxes_to_add_temp_vbox.children + params['checkboxes_to_add']
            annotate_session_stats_accordion.children = annotate_session_stats_accordion.children + (checkboxes_to_add_temp_vbox, )
            l_all_checkboxes = l_all_checkboxes + [(session_id, elem) for elem in params['l_checkboxes']]

        for i in range(len(list(annotate_session_stats_accordion.children))):
            annotate_session_stats_accordion.set_title(i, l_sessions[i])

        params['checkboxes_to_add'] = w.VBox([annotate_session_stats_accordion]).children[:]
        params['l_checkboxes'] = l_all_checkboxes

        return params


    def create_group_order_text(self, params, stats_value):
        l_groups = params['l_groups']
        if stats_value == 0:
            for group_id in l_groups:
                if l_groups.index(group_id) == 0:
                    l_xlabel_string = group_id
                else:
                    l_xlabel_string = l_xlabel_string + ', {}'.format(group_id)
            params['widgets']['set_xlabel_order']['value'] = l_xlabel_string
            params['widgets']['set_xlabel_order']['visibility'] = 'visible'

        elif stats_value == 1:
            params['widgets']['set_xlabel_order']['value'] = l_groups[0]

        elif stats_value == 2:
            l_sessions = params['l_sessions']
            for session_id in l_sessions:
                if l_sessions.index(session_id) == 0:
                    l_xlabel_string = session_id
                else:
                    l_xlabel_string = l_xlabel_string + ', {}'.format(session_id)
            params['widgets']['set_xlabel_order']['value'] = l_xlabel_string
            params['widgets']['set_xlabel_order']['visibility'] = 'visible'

            for group_id in l_groups:
                if l_groups.index(group_id) == 0:
                    l_hue_string = group_id
                else:
                    l_hue_string = l_hue_string + ', {}'.format(group_id)
            params['widgets']['set_hue_order']['value'] = l_hue_string
            params['widgets']['set_hue_order']['visibility'] = 'visible'

        return params

    def create_ylims(self, params, df, data_col):
        if df[data_col].min() < 0:
            params['set_yaxis_lower_lim_value'] = round(df[data_col].min() + df[data_col].min()*0.1, 2)
        else:
            params['set_yaxis_lower_lim_value'] = round(df[data_col].min() - df[data_col].min()*0.1, 2)

        if df[data_col].max() < 0:
            params['set_yaxis_upper_lim_value'] = round(df[data_col].max() - df[data_col].max()*0.1, 2)
        else:
            params['set_yaxis_upper_lim_value'] = round(df[data_col].max() + df[data_col].max()*0.1, 2)

        return params


    def create_group_color_pickers(self, params, l_groups):
        if len(params['widgets']['group_colors_vbox']['children']) == 0:
            for group_id in l_groups:
                set_group_color = w.ColorPicker(concise = False, description = group_id, style = STYLE)
                params['widgets']['group_colors_vbox']['children'] = params['widgets']['group_colors_vbox']['children'] + (set_group_color, )

        return params

# Cell
class Select_plots_widget:
    "Creates the part of the widget that allows to select what statistical comparison shall be made"
    def __init__(self, params):
        self.dropdown = w.Dropdown(description = 'Please select which type of plot you want to create:',
                                   options = params['widgets']['plots_dropdown']['options'],
                                   value = params['widgets']['plots_dropdown']['value'],
                                   layout = {'width': '100%',
                                             'visibility': params['widgets']['plots_dropdown']['visibility']},
                                   style = STYLE)
        self.button = w.Button(description = "Plot the data", layout = {'visibility': params['widgets']['plots_button']['visibility']})
        self.widget = w.HBox([self.dropdown, self.button])


    def on_button_clicked(self, params):
        stats_value = params['widgets']['stats_dropdown']['value']
        plots_value = params['widgets']['plots_dropdown']['value']
        df = params['data']

        params['widgets']['plots_button']['description'] = 'Refresh the plot'

        fig = plt.figure(figsize=(params['set_fig_width']/2.54 , params['set_fig_height']/2.54), facecolor='white')
        ax = fig.add_subplot()

        for axis in ['top', 'right']:
            ax.spines[axis].set_visible(False)

        for axis in ['bottom','left']:
            ax.spines[axis].set_linewidth(params['set_axes_linewidth'])
            ax.spines[axis].set_color(params['set_axes_color'])

        plt.tick_params(labelsize=params['set_axes_tick_size'], colors=params['set_axes_color'])

        if stats_value == 0: # independent_samples()
            if plots_value == 0:
                sns.stripplot(data=df, x=params['group_col'], y=params['data_col'], order=params['l_xlabel_order'],
                              palette=params['color_palette'], size=params['set_marker_size'])
            elif plots_value == 1:
                sns.boxplot(data=df, x=params['group_col'], y=params['data_col'], order=params['l_xlabel_order'], palette=params['color_palette'])
            elif plots_value == 2:
                sns.boxplot(data=df, x=params['group_col'], y=params['data_col'], order=params['l_xlabel_order'],
                            palette=params['color_palette'], showfliers=False)
                sns.stripplot(data=df, x=params['group_col'], y=params['data_col'], order=params['l_xlabel_order'],
                              color='k', size=params['set_marker_size'])
            elif plots_value == 3:
                sns.violinplot(data=df, x=params['group_col'], y=params['data_col'], order=params['l_xlabel_order'],
                               palette=params['color_palette'], cut=0)
                sns.stripplot(data=df, x=params['group_col'], y=params['data_col'], order=params['l_xlabel_order'],
                              color='k', size=params['set_marker_size'])
            else:
                print("Function not implemented. Please go and annoy Dennis to finally do it")


        elif stats_value == 1: # one_sample()
            pass

        elif stats_value == 2: # MMA

            if params['set_show_legend'] == True:
                if plots_value == 0:
                    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=False)
                elif plots_value in [1, 2, 3]:
                    handles, labels = ax.get_legend_handles_labels()
                    new_handles = handles[:len(params['l_hue_order'])]
                    new_labels = labels[:len(params['l_hue_order'])]
                    ax.legend(new_handles, new_labels, loc='center left', bbox_to_anchor=(1, 0.5), frameon=False)
            else:
                ax.get_legend().remove()

        else:
            print("Function not implemented. Please go and annoy Dennis to finally do it")


        # Code to annotate stats

        plt.ylabel(params['set_yaxis_label_text'], fontsize=params['set_yaxis_label_fontsize'], color=params['set_yaxis_label_color'])
        plt.xlabel(params['set_xaxis_label_text'], fontsize=params['set_xaxis_label_fontsize'], color=params['set_xaxis_label_color'])

        if params['set_yaxis_scaling_mode'] == 1:
            plt.ylim(params['set_yaxis_lower_lim_value'], params['set_yaxis_upper_lim_value'])

        plt.tight_layout()

        if params['save_plot'] == True:
            plt.savefig('customized_plot.png', dpi=300)

        plt.show()

        return params




# Cell
class Select_downloads_widget:
    "Creates the part of the widget that allows the user to download the results"
    def __init__(self, params):
        self.dropdown = w.Dropdown(description = 'Please select which type of plot you want to create:',
                                   options = [('statistical results only', 0), ('plot only', 1), ('both', 2)],
                                   value = params['widgets']['downloads_dropdown']['value'],
                                   layout = {'width': '100%',
                                             'visibility': params['widgets']['downloads_dropdown']['visibility']},
                                   style = STYLE)
        self.button = w.Button(description='Download', icon='file-download', layout = {'visibility': params['widgets']['downloads_button']['visibility']})
        self.widget = w.HBox([self.dropdown, self.button])


    def on_button_clicked(self, params):
        pass

# Cell
class Customization_widget:
    "Creates the part of the widget that enables the user to customize the plot"
    def __init__(self):

        # Widgets to select and customize the annoations:
        self.select_annotations = Select_annotations()
        self.customize_annotations = Customize_annotations()
        self.annotations_accordion = w.Accordion(children=[self.select_annotations.widget,
                                                           self.customize_annotations.widget],
                                                           selected_index=None)
        self.annotations_accordion.set_title(0, 'Select which stats shall be annotated')
        self.annotations_accordion.set_title(1, 'Customize annotation features')

        # Widgets to customize the axes:
        self.yaxis = Customize_y_axis()
        self.xaxis = Customize_x_axis()
        self.both_axes = Customize_both_axes()

        self.axes_accordion = w.Accordion(children=[self.yaxis.widget, self.xaxis.widget, self.both_axes.widget])
        self.axes_accordion.set_title(0, 'y-axis')
        self.axes_accordion.set_title(1, 'x-axis')
        self.axes_accordion.set_title(2, 'common features')

        # Widgets to customize other features of the plot:
        self.other_features = Customize_other_features()

        # Throw it all together and "hide" it inside another accordion that serves as the main widget:
        self.customization_accordion = w.Accordion(children=[self.annotations_accordion,
                                                             self.axes_accordion,
                                                             self.other_features.widget],
                                                   selected_index=None)
        self.customization_accordion.set_title(0, 'Customize how statistics are annotated in the plot')
        self.customization_accordion.set_title(1, 'Customize axes')
        self.customization_accordion.set_title(2, 'Customize other features of the plot')
        # Main widget:
        self.widget = w.Accordion(children=[self.customization_accordion], selected_index=None, continous_update=False, layout={'visibility': 'hidden'})
        self.widget.set_title(0, 'Expand me to customize your plot!')








# Cell
class Customize_annotations:
    "Helps with the creation of the customization accordion"
    def __init__(self):
        # How far will the annotation lines be shifted from the data? Calculates as:
        # y_shift_annotation_line = max(data) * set_distance_brackets_to_data.value
        self.set_distance_brackets_to_data = w.BoundedFloatText(description='Distance of the annotation bars to the graph',
                                                                value=0.1, min=0, max=1, step=0.005,
                                                                style={'description_width': 'initial'},
                                                                layout={'width':'initial'})
        # Determines annotation_brackets_factor: 0 for 'No brackets', 1 for 'brackets'
        # brackets_height = y_shift_annotation_line*0.5*annotation_brackets_factor
        self.select_bracket_no_bracket = w.RadioButtons(description='Annotation bar style:',
                                                        options=['Brackets', 'No brackets'],
                                                        value=('Brackets'),
                                                        style={'description_width': 'initial'},
                                                        layout={'width': '300px', 'height': '50px'})
        # How far will the annotation stars be shifted from the annotation lines? Calculates as:
        # y_shift_annotation_text = y_shift_annotation_line + brackets_height + y_shift_annotation_line*0.5*set_distance_stars_to_brackets.value
        self.set_distance_stars_to_brackets = w.BoundedFloatText(description='Distance of the stars to the annotation bars',
                                                                 value=0.5, step=0.05, min=0, max=3,
                                                                 style={'description_width': 'initial'},
                                                                 layout={'width':'initial'})

        self.set_fontsize_stars = w.BoundedFloatText(description='Fontsize of the stars',
                                                     value=10, min=1, max=50,
                                                     style={'description_width': 'initial'},
                                                     layout={'width':'initial'})

        self.set_linewidth_annotations = w.BoundedFloatText(description='Linewidth of the annotation bars',
                                                            value=1.5, min=0, max=10, step=0.1,
                                                            layout={'width':'initial'},
                                                            style={'description_width': 'initial'})

        self.set_stars_fontweight_bold = w.Checkbox(description='Stars bold', value=False)

        self.widget = w.VBox([w.HBox([self.set_stars_fontweight_bold, self.select_bracket_no_bracket]),
                              self.set_distance_stars_to_brackets,
                              self.set_distance_brackets_to_data,
                              self.set_fontsize_stars,
                              self.set_linewidth_annotations])


# Cell
class Select_annotations:
    def __init__(self):

        self.set_annotate_all = w.Checkbox(value=False, description='Annotate all', indent=False)
        self.select_annotations_vbox = w.VBox([])
        self.select_annotations_accordion = w.Accordion(children=[self.select_annotations_vbox])
        self.select_annotations_accordion.set_title(0, 'Select individual comparisons for annotation')

        self.widget = w.VBox([self.select_annotations_accordion, self.set_annotate_all])

# Cell
class Customize_y_axis:
    def __init__(self):
        self.set_yaxis_label_text = w.Text(value='data', placeholder='data', description='y-axis title:', layout={'width': 'auto'})
        self.set_yaxis_label_fontsize = w.IntSlider(value=12, min=8, max=40, step=1, description='fontsize:')
        self.set_yaxis_label_color = w.ColorPicker(concise=False, description='font color', value='#000000')
        self.set_yaxis_scaling_mode = w.RadioButtons(description = 'Please select whether you want to use automatic or manual scaling of the yaxis:',
                                                              options=[('Use automatic scaling', 0), ('Use manual scaling', 1)],
                                                              value=0, layout={'width': '700px', 'height': '75px'}, style={'description_width': 'initial'})
        self.set_yaxis_lower_lim = w.FloatText(value=0.0, description='lower limit:', style={'description_width': 'initial'})
        self.set_yaxis_upper_lim = w.FloatText(value=0.0, description='upper limit:', style={'description_width': 'initial'})
        self.widget =  w.VBox([w.HBox([self.set_yaxis_label_text, self.set_yaxis_label_fontsize, self.set_yaxis_label_color]),
                                       self.set_yaxis_scaling_mode,
                                       w.HBox([self.set_yaxis_lower_lim, self.set_yaxis_upper_lim])])

# Cell
class Customize_x_axis:
    def __init__(self):
        self.set_xaxis_label_text = w.Text(value='group_IDs', placeholder='group_IDs', description='x-axis title:', layout={'width': 'auto'})
        self.set_xaxis_label_fontsize = w.IntSlider(value=12, min=8, max=40, step=1, description='fontsize:')
        self.set_xaxis_label_color = w.ColorPicker(concise=False, description='font color', value='#000000')
        self.set_xlabel_order = w.Text(value='x label order',
                                        placeholder='Specify the desired order of the x-axis labels with individual labels separated by a comma',
                                        description='x-axis label order (separated by comma):',
                                        layout={'width': '800px', 'visibility': 'hidden'},
                                        style={'description_width': 'initial'})
        self.set_hue_order = w.Text(value='hue order',
                                     placeholder='Specify the desired group order with individual groups separated by a comma',
                                     description='group order (separated by comma):',
                                     layout={'width': '800px', 'visibility': 'hidden'},
                                     style={'description_width': 'initial'})
        self.widget =  w.VBox([w.HBox([self.set_xaxis_label_text, self.set_xaxis_label_fontsize, self.set_xaxis_label_color]),
                               self.set_xlabel_order,
                               self.set_hue_order])


# Cell
class Customize_both_axes:
    def __init__(self):
        self.set_axes_linewidth = w.BoundedFloatText(value=1, min=0, max=40, description='Axes linewidth',
                                               style={'description_width': 'initial'}, layout={'width': 'auto'})
        self.set_axes_color = w.ColorPicker(concise=False, description='Axes and tick label color',
                                             value='#000000', style={'description_width': 'initial'}, layout={'width': 'auto'})
        self.set_axes_tick_size = w.BoundedFloatText(value=10, min=1, max=40, description='Tick label size',
                                                style={'description_width': 'initial'}, layout={'width': 'auto'})
        self.widget = w.HBox([self.set_axes_linewidth, self.set_axes_color, self.set_axes_tick_size])


# Cell
class Customize_other_features:
    def __init__(self):
        self.select_palette_or_individual_color = w.RadioButtons(description = 'Please select a color code option and chose from the respective options below:',
                                                                  options=[('Use a pre-defined palette', 0), ('Define colors individually', 1)],
                                                                  value=0, layout={'width': '700px', 'height': '75px'}, style={'description_width': 'initial'})
        self.select_color_palettes = w.Dropdown(options=['colorblind', 'Spectral', 'viridis', 'rocket', 'cubehelix'],
                                                 value='colorblind',
                                                 description='Select a color palette',
                                                 layout={'width': '350'},
                                                 style={'description_width': 'initial'})
        self.set_show_legend = w.Checkbox(value=True, description='Show legend (if applicable):', style={'description_width': 'initial'})
        self.set_marker_size = w.FloatText(value=5,description='marker size (if applicable):', style={'description_width': 'initial'})
        # Empty VBox which will be filled as soon as groups are determined (stats_button.click())
        self.group_colors_vbox = w.VBox([])
        self.set_fig_width = w.FloatSlider(value=28, min=3, max=30, description='Figure width:', style={'description_width': 'inital'})
        self.set_fig_height = w.FloatSlider(value=16, min=3, max=30, description='Figure height:', style={'description_width': 'inital'})
        self.widget = w.VBox([self.select_palette_or_individual_color,
                              w.HBox([self.select_color_palettes, self.group_colors_vbox]),
                              w.HBox([self.set_fig_width, self.set_fig_height]),
                              w.HBox([self.set_show_legend, self.set_marker_size])])