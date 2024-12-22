"""
    Noorish Application
    
"""

# Importing
from nicegui import Client, ui

#####################################################################################################################################################
## GLOBAL VARIABLES
#####################################################################################################################################################

# Colour palette
color_palette = {
    "main": "#E9E0D8",
    "accent": "#C49450",
    "green": "#79A486",
    "dark": "#161f27",
    "light": "#F7F8F8",
}

#####################################################################################################################################################
## WEB APPLICATION LAYOUT
#####################################################################################################################################################

# Main page
@ui.page('/')
def page(client: Client):
    
    # Main Attributes
    client.layout.style('background-color: {}'.format(color_palette["main"]))

    # Main Header
    with ui.header(elevated=True).style('background-color: {}'.format(color_palette["dark"])).classes('justify-center'):
        noorish_label = ui.label('Noorish')
        noorish_label.tailwind.font_weight('extrabold').text_color(color_palette["light"])
        noorish_label.classes('text-3xl')

    # Menu Header
    with ui.tabs().classes('w-full') as tabs:
        menu_tab = ui.tab('Weekly Menu', icon='edit_calendar')
        recipe_tab = ui.tab('Recipes', icon='menu_book')

    with ui.tab_panels(tabs, value=menu_tab).classes('w-full'):
        # Weekly Menu Tab
        with ui.tab_panel(menu_tab) as menu_tab_box:
            menu_tab_box.style('background-color: {}'.format(color_palette["main"]))
            ui.label('First tab')
        
        # Recipes Tab
        with ui.tab_panel(recipe_tab).style('justify-content: center') as recipe_tab_box:
            # General Attributes
            recipe_tab_box.style('background-color: {}'.format(color_palette["main"]))

            # Search Bar
            with ui.row().classes('w-full').classes('justify-center'):
                # ui.icon('search', color=color_palette["dark"]).classes("justify-center").classes('text-3xl')
                ui.input(placeholder='Search...').props('rounded outlined dense').classes("justify-center")
                ui.chip('Seasonal', selectable=True, icon='calendar_month', color=color_palette["accent"])
                ui.chip('Quick', selectable=True, icon='bolt', color=color_palette["green"])

            # Recipe Cards
            with ui.row().classes("justify-center"):
                for i in range(10):
                    with ui.card().tight():
                        ui.image('https://picsum.photos/id/684/640/360')
                        with ui.card_section():
                            ui.label('Lorem ipsum dolor sit amet, consectetur adipiscing elit, ...')


#####################################################################################################################################################
## RUN
#####################################################################################################################################################

if __name__ in {"__main__", "__mp_main__"}:
    ui.run()