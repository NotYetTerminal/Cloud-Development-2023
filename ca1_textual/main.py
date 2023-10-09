import os
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Select, ListView, ListItem, Label, Button
import swim_utils
import webbrowser

class SwimApp(App):
    CSS_PATH = "style.tcss"

    data_dict: dict = {}
    selected_person_name: str = ""
    complete_file_name: str = ""

    top_label: Label = None

    name_label: Label = None
    name_select: Select = None

    type_Label: Label = None
    type_select: Select = None

    generate_button: Button = None

    popup_label: Label = None
    dummy_button: Button = None
    popup_button_yes: Button = None
    popup_button_no: Button = None

    popup_open: str = "none"


    def compose(self) -> ComposeResult:
        self.top_label = Label("Swimmers Data Chart Creator", classes = "title")
        yield self.top_label

        self.name_label = Label("Swimmers Names:")
        yield self.name_label
        data_dict = self.gather_files_informations()
        self.name_select = Select(((key, f"{key}:{value}") for key, value in data_dict.items()), id = "name", prompt = "")
        yield self.name_select

        self.type_Label = Label("Swimmer Age - Stroke - Distance:")
        yield self.type_Label
        self.type_select = Select([], id = "type", prompt = "")
        yield self.type_select

        self.generate_button = Button("Generate Chart!", id = "generate", disabled = True)
        yield self.generate_button

        self.popup_label = Label("Do you want to continue?", classes = "title")
        self.popup_label.styles.display = "none"
        yield self.popup_label

        self.dummy_button = Button(id = "dummy")
        yield self.dummy_button

        self.popup_button_yes = Button("Yes", id = "yes", variant = "success")
        self.popup_button_yes.styles.display = "none"
        yield self.popup_button_yes

        self.popup_button_no = Button("No", id = "no", variant = "error")
        self.popup_button_no.styles.display = "none"
        yield self.popup_button_no


    @on(Select.Changed)
    def change_list_view(self, event: Select.Changed) -> None:
        if event.select.id == "name":
            self.type_select.set_options([])
            self.type_select.value = ""
            self.generate_button.disabled = True
            if event.value != None:
                self.selected_person_name = event.value.split(":")[0]
                correct_data: list = event.value.split(":")[1].replace("[", "").replace("]", "").replace("'", "").split(", ")
                self.type_select.set_options((file_data, file_data) for file_data in correct_data)

        elif event.select.id == "type":
            if event.value != None:
                file_value: str = f"{event.value.split(' - ')[0]} - {event.value.split(' - ')[2]} - {event.value.split(' - ')[1]}"
                self.complete_file_name: str = f"{self.selected_person_name}-{file_value}".replace(" ", "") + ".txt"
                self.generate_button.disabled = False
        return

    @on(Button.Pressed)
    def generate_chart(self, event: Button.Pressed) -> None:
        if event.button.id == "no":
            self.exit()
            return
        elif event.button.id == "yes":
            self.toggle_popup()
            return
        elif event.button.id == "dummy":
            return
        name, age, distance, stroke, times, converts, average = swim_utils.get_swimmers_data(self.complete_file_name)

        file_header: str = f"""<!DOCTYPE html>
<html>
    <head>
        <title>
            {name} (Under {age}) {distance} - {stroke}
        </title>
    </head>
    <body>
        <h3>{name} (Under {age}) {distance} - {stroke}</h3>"""


        file_footer: str = f"""<p>Average: {average}</p>
    </body>
</html>
        """
        chart_path: str = f"ca1_textual/charts/{name}-{age}-{distance}-{stroke}-Chart.html"

        with open(chart_path, "w+") as f:
            f.write(file_header)

            for time, convert in zip(times, converts):
                file_body: str = f"""
                <svg height="30" width="400">
                        <rect height="30" width="{swim_utils.convert2range(convert, min(converts) - 100, max(converts) + 100, 0, 400)}" style="fill:rgb(0,0,255);" />
                </svg>{time}<br />
"""
                f.write(file_body)

            f.write(file_footer)

        webbrowser.open(chart_path)

        self.toggle_popup()
        return


    def toggle_popup(self) -> None:
        self.top_label.styles.display = self.popup_open
        self.name_label.styles.display = self.popup_open
        self.name_select.styles.display = self.popup_open
        self.type_Label.styles.display = self.popup_open
        self.type_select.styles.display = self.popup_open
        self.generate_button.styles.display = self.popup_open

        if self.popup_open == "none":
            self.popup_open = "block"
        else:
            self.popup_open = "none"

        self.popup_label.styles.display = self.popup_open
        self.popup_button_yes.styles.display = self.popup_open
        self.popup_button_no.styles.display = self.popup_open
        return

    def gather_files_informations(self) -> dict:
        """
        Returns a dictionary of all of the file names.
        Structure: Name - Age: [list of distances and types]
        """
        data_dict: dict = {}

        for file_name in os.listdir(swim_utils.FOLDER):
            if ".txt" in file_name:
                name, age, distance, swim_type = file_name.replace(".txt", "").split("-")
                if name in data_dict.keys():
                    data_dict[name].append(f"{age} - {swim_type} - {distance}")
                else:
                    data_dict[name] = [f"{age} - {swim_type} - {distance}"]
        
        data_dict = self.sort_dict_by_keys(data_dict)

        for key, value in data_dict.items():
            data_dict[key].sort()

        return data_dict
    

    def sort_dict_by_keys(self: object, old_dict: dict) -> dict:
        """
        Sorts a dictionary by the keys.
        """
        return {key: old_dict[key] for key in sorted(list(old_dict.keys()))}


def main() -> None:
    swim_app: SwimApp = SwimApp()
    swim_app.run()

    return



if __name__ == "__main__":
    main()
