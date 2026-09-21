from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty
import os
from core.database import get_connection

Builder.load_file(os.path.join(os.path.dirname(__file__), "catalog.kv"))

class CatalogScreen(MDScreen):
    def on_enter(self, *args):
        self.load_activities()
        
    def load_activities(self):
        self.ids.catalog_list.clear_widgets()
        
        from kivymd.uix.list import TwoLineListItem
        
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, category, description FROM activities ORDER BY category, name")
            activities = cursor.fetchall()
            
            for act in activities:
                item = TwoLineListItem(
                    text=f"{act['name']} ({act['category']})",
                    secondary_text=act['description'][:50] + "..." if len(act['description']) > 50 else act['description']
                )
                self.ids.catalog_list.add_widget(item)
