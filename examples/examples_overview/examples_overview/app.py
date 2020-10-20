import sys
import os
import subprocess
from pathlib import Path
import toga
from toga.style import Pack
from toga.constants import COLUMN


examples_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class ExampleExamplesOverviewApp(toga.App):
    # Button callback functions
    def run(self, widget, **kwargs):

        row = self.table.selection

        env = os.environ.copy()
        env["PYTHONPATH"] = row.path

        self._process = subprocess.Popen(
            [sys.executable, "-m", row.name],
            env=env,
        )

    def reset_code(self, widget, **kwargs):
        pass

    def on_example_selected(self, widget, row):

        readme_path = row.path / "README.rst"

        if readme_path.is_file():
            with open(readme_path) as f:
                readme_text = f.read()
        else:
            readme_text = "No README found"

        self.info_view.value = readme_text

    def startup(self):

        self._process = None

        # ==== Set up main window ======================================================

        self.main_window = toga.MainWindow(title=self.name)

        # Label for user instructions
        label = toga.Label(
            "Please select an example to run",
            style=Pack(padding_bottom=10),
        )

        # ==== Table with examples =====================================================

        self.examples = []

        # search for all folders that contain modules
        for root, dirs, files in os.walk(examples_dir):
            # skip hidden folders
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            if any(name == "__main__.py" for name in files):
                path = Path(root)
                self.examples.append(dict(name=path.name, path=path.parent))

        self.examples.sort(key=lambda e: e["path"])

        self.table = toga.Table(
            headings=["Name", "Path"],
            data=self.examples,
            on_double_click=self.run,
            on_select=self.on_example_selected,
            style=Pack(padding_bottom=10, flex=1),
        )

        # Buttons
        self.btn_run = toga.Button("Run Example", on_press=self.run)
        self.btn_reset = toga.Button("Reset Code", on_press=self.reset_code)

        # ==== View of example code ====================================================

        self.info_view = toga.MultilineTextInput(
            placeholder="Please select example", readonly=True, style=Pack(padding=1)
        )

        # ==== Assemble layout =========================================================

        left_box = toga.Box(
            children=[self.table, self.btn_run],
            style=Pack(
                direction=COLUMN,
                padding=1,
                flex=1,
            ),
        )

        split_container = toga.SplitContainer(content=[left_box, self.info_view])

        outer_box = toga.Box(
            children=[label, split_container],
            style=Pack(padding=10, direction=COLUMN),
        )

        # Add the content on the main window
        self.main_window.content = outer_box

        # Show the main window
        self.main_window.show()


def main():
    return ExampleExamplesOverviewApp(
        "Examples Overview", "org.beeware.widgets.examples_overview"
    )


if __name__ == "__main__":
    app = main()
    app.main_loop()
