import json
import webbrowser
import urllib.parse
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

# अपनी मम्मा का WhatsApp नंबर यहाँ डालें (कंट्री कोड के साथ, बिना '+' या '空格' के)
MUMMA_PHONE_NUMBER = "919706148209"  # उदाहरण: 919876543210

KV = """
MDScreen:
    md_bg_color: "#FAF6F0"  # सॉफ्ट और प्रीमियम क्रीम बैकग्राउंड

    ScrollView:
        do_scroll_x: False
        do_scroll_y: True

        MDBoxLayout:
            orientation: "vertical"
            padding: "24dp"
            spacing: "20dp"
            size_hint_y: None
            height: self.minimum_height

            Widget:
                size_hint_y: None
                height: "15dp"

            # सुंदर लोगो इमेज (For perfect transparency, use a transparent .png file)
            Image:
                source: "logo.jpeg"
                size_hint: None, None
                size: "260dp", "160dp"
                pos_hint: {"center_x": .5}
                radius: [15, ]

            # ब्रांड का नाम (Premium Serif/Attractive Style Layout)
            MDLabel:
                text: "GHAR KI RASOI"
                halign: "center"
                bold: True
                font_style: "H4"
                theme_text_color: "Custom"
                text_color: "#4A2E1B"  # चॉकलेटी ब्राउन कलर प्रीमियम लुक के लिए

            MDLabel:
                id: welcome_label
                text: "Welcome, Foodie!"
                halign: "center"
                font_style: "Subtitle1"
                theme_text_color: "Secondary"

            # मुख्य फॉर्म कार्ड (Premium Shadow & Rounded Corners)
            MDCard:
                orientation: "vertical"
                size_hint_x: 0.95
                size_hint_y: None
                height: "460dp"
                pos_hint: {"center_x": .5}
                padding: "20dp"
                spacing: "15dp"
                radius: [24, ]
                elevation: 2
                md_bg_color: "#FFFFFF"

                MDLabel:
                    text: "Place Your Delicious Order"
                    bold: True
                    font_style: "Subtitle1"
                    theme_text_color: "Custom"
                    text_color: "#D35400"
                    halign: "center"

                # कस्टमर नेम फील्ड
                MDTextField:
                    id: name_field
                    hint_text: "Your Name"
                    mode: "rectangle"
                    icon_left: "account"

                MDRaisedButton:
                    text: "Save Name"
                    pos_hint: {"center_x": .5}
                    md_bg_color: "#4A2E1B"
                    on_release: app.save_name()

                # ड्रॉपडाउन फील्ड्स
                MDTextField:
                    id: product_field
                    hint_text: "Select Product"
                    mode: "rectangle"
                    readonly: True
                    icon_left: "food-variant"
                    on_focus: if self.focus: app.product_menu.open()

                MDTextField:
                    id: weight_field
                    hint_text: "Select Weight"
                    mode: "rectangle"
                    readonly: True
                    icon_left: "weight"
                    on_focus: if self.focus: app.weight_menu.open()

                MDTextField:
                    id: packet_field
                    hint_text: "How many Packets?"
                    mode: "rectangle"
                    readonly: True
                    icon_left: "numeric"
                    on_focus: if self.focus: app.packet_menu.open()

                MDFillRoundFlatButton:
                    text: "＋ ADD ITEM TO CART"
                    pos_hint: {"center_x": .5}
                    md_bg_color: "#E67E22"
                    font_style: "Button"
                    size_hint_x: 0.8
                    on_release: app.add_item()

            # करंट आर्डर सेक्शन
            MDCard:
                orientation: "vertical"
                size_hint_x: 0.95
                size_hint_y: None
                height: "180dp"
                pos_hint: {"center_x": .5}
                padding: "15dp"
                radius: [16, ]
                md_bg_color: "#F3EFE9"
                elevation: 0

                MDLabel:
                    text: "🛒 Current Cart Items:"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: "#4A2E1B"

                ScrollView:
                    MDLabel:
                        id: order_label
                        text: "Cart is empty"
                        theme_text_color: "Secondary"
                        size_hint_y: None
                        height: self.texture_size[1]
                        font_style: "Body2"

            MDLabel:
                id: total_label
                text: "Total Packets: 0"
                halign: "center"
                bold: True
                font_style: "H6"
                theme_text_color: "Custom"
                text_color: "#27AE60"

            # फाइनल सबमिट बटन
            MDFillRoundFlatButton:
                text: "🚀 SUBMIT & SEND ORDER"
                pos_hint: {"center_x": .5}
                md_bg_color: "#27AE60"
                size_hint_x: 0.9
                font_style: "H6"
                on_release: app.submit_order()

            Widget:
                size_hint_y: None
                height: "15dp"

            # सुंदर 'Made with Love' लोगो लेआउट (Beautiful Row Integration)
            MDBoxLayout:
                orientation: "horizontal"
                spacing: "5dp"
                size_hint: None, None
                width: self.minimum_width
                height: "30dp"
                pos_hint: {"center_x": .5}

                MDLabel:
                    text: "Made With"
                    font_style: "Caption"
                    theme_text_color: "Secondary"
                    size_hint_x: None
                    width: "60dp"
                    halign: "right"

                MDIcon:
                    icon: "cards-heart"
                    theme_text_color: "Custom"
                    text_color: "#E74C3C"  # लव रेड कलर फॉर हार्ट लोगो
                    size_hint_x: None
                    width: "20dp"

                MDLabel:
                    text: "By Sharmila & Binod"
                    font_style: "Caption"
                    theme_text_color: "Secondary"
                    size_hint_x: None
                    width: "120dp"
                    halign: "left"
"""

class GharKiRasoi(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "Orange"
        self.orders = []
        self.screen = Builder.load_string(KV)

        self.product_menu = MDDropdownMenu(
            caller=self.screen.ids.product_field,
            items=[
                {"text": "Banana Chips", "viewclass": "OneLineListItem", "on_release": lambda x="Banana Chips": self.set_product(x)},
                {"text": "Mangori", "viewclass": "OneLineListItem", "on_release": lambda x="Mangori": self.set_product(x)},
                {"text": "Adrak Powder", "viewclass": "OneLineListItem", "on_release": lambda x="Adrak Powder": self.set_product(x)},
            ],
            width_mult=4
        )

        self.weight_menu = MDDropdownMenu(
            caller=self.screen.ids.weight_field,
            items=[
                {"text": w, "viewclass": "OneLineListItem", "on_release": lambda x=w: self.set_weight(x)}
                for w in ["200g", "300g", "400g", "500g"]
            ],
            width_mult=3
        )

        self.packet_menu = MDDropdownMenu(
            caller=self.screen.ids.packet_field,
            items=[
                {"text": str(i), "viewclass": "OneLineListItem", "on_release": lambda x=str(i): self.set_packet(x)}
                for i in range(1, 11)
            ],
            width_mult=2
        )

        self.load_user()
        return self.screen

    def load_user(self):
        try:
            with open("user.json", "r") as f:
                name = json.load(f).get("name", "")
                if name:
                    self.screen.ids.welcome_label.text = f"Welcome back, {name}! ✨"
                    self.screen.ids.name_field.text = name
        except:
            pass

    def save_name(self):
        name = self.screen.ids.name_field.text.strip()
        if not name:
            return
        with open("user.json", "w") as f:
            json.dump({"name": name}, f, indent=4)
        self.screen.ids.welcome_label.text = f"Welcome, {name}! ✨"
        MDDialog(title="Saved!", text=f"Name updated to '{name}'", size_hint=(0.8, None)).open()

    def set_product(self, v):
        self.screen.ids.product_field.text = v
        self.product_menu.dismiss()

    def set_weight(self, v):
        self.screen.ids.weight_field.text = v
        self.weight_menu.dismiss()

    def set_packet(self, v):
        self.screen.ids.packet_field.text = v
        self.packet_menu.dismiss()

    def add_item(self):
        p = self.screen.ids.product_field.text
        w = self.screen.ids.weight_field.text
        pk = self.screen.ids.packet_field.text

        if not (p and w and pk):
            MDDialog(title="Error", text="Please select Product, Weight, and Packets first!").open()
            return

        self.orders.append({"product": p, "weight": w, "packets": pk})

        if self.screen.ids.order_label.text == "Cart is empty":
            self.screen.ids.order_label.text = ""

        self.screen.ids.order_label.text += f"• {p} ({w}) — {pk} Packet(s)\n"
        total = sum(int(x["packets"]) for x in self.orders)
        self.screen.ids.total_label.text = f"Total Packets: {total}"
        
        self.screen.ids.product_field.text = ""
        self.screen.ids.weight_field.text = ""
        self.screen.ids.packet_field.text = ""

    def submit_order(self):
        name = self.screen.ids.name_field.text.strip()

        if not name:
            MDDialog(title="Missing Name", text="Please enter and save your name before submitting!").open()
            return

        if not self.orders:
            MDDialog(title="Empty Cart", text="Please add at least one item to your cart!").open()
            return

        try:
            with open("orders.json", "r") as f:
                data = json.load(f)
        except:
            data = []

        data.append({
            "customer": name,
            "items": self.orders
        })

        with open("orders.json", "w") as f:
            json.dump(data, f, indent=4)

        whatsapp_msg = f"*New Order Received from Ghar Ki Rasoi App!* 🎉\n\n"
        whatsapp_msg += f"👤 *Customer Name:* {name}\n"
        whatsapp_msg += f"📦 *Order Details:*\n"
        
        for idx, item in enumerate(self.orders, 1):
            whatsapp_msg += f"  {idx}. {item['product']} | {item['weight']} | {item['packets']} packet(s)\n"
            
        total_p = sum(int(x["packets"]) for x in self.orders)
        whatsapp_msg += f"\n🔢 *Total Packets:* {total_p}\n"
        whatsapp_msg += f" Please prepare this order."

        encoded_msg = urllib.parse.quote(whatsapp_msg)
        whatsapp_url = f"https://wa.me/{MUMMA_PHONE_NUMBER}?text={encoded_msg}"

        self.orders = []
        self.screen.ids.order_label.text = "Cart is empty"
        self.screen.ids.total_label.text = "Total Packets: 0"

        webbrowser.open(whatsapp_url)

        MDDialog(
            title="Order Formed!",
            text="Your order is compiled! Opening WhatsApp to notify Sharmila & Binod... Please click send on WhatsApp.",
        ).open()

if __name__ == "__main__":
    GharKiRasoi().run()












# import json
# import webbrowser
# import urllib.parse
# from kivy.lang import Builder
# from kivymd.app import MDApp
# from kivymd.uix.menu import MDDropdownMenu
# from kivymd.uix.dialog import MDDialog
# from kivymd.uix.button import MDFlatButton

# # अपनी मम्मा का WhatsApp नंबर यहाँ डालें (कंट्री कोड के साथ, बिना '+' या '空格' के)
# MUMMA_PHONE_NUMBER = "91XXXXXXXXXX"  # उदाहरण: 919876543210

# KV = """
# MDScreen:
#     md_bg_color: "#FAF6F0"  # सॉफ्ट और प्रीमियम क्रीम बैकग्राउंड

#     ScrollView:
#         do_scroll_x: False
#         do_scroll_y: True

#         MDBoxLayout:
#             orientation: "vertical"
#             padding: "24dp"
#             spacing: "18dp"
#             size_hint_y: None
#             height: self.minimum_height

#             Widget:
#                 size_hint_y: None
#                 height: "10dp"

#             # सुंदर लोगो इमेज
#             Image:
#                 source: "logo.jpeg"
#                 size_hint: None, None
#                 size: "240dp", "150dp"
#                 pos_hint: {"center_x": .5}
#                 radius: [15, ]

#             # ब्रांड का नाम
#             MDLabel:
#                 text: "GHAR KI RASOI"
#                 halign: "center"
#                 bold: True
#                 font_style: "H4"
#                 theme_text_color: "Custom"
#                 text_color: "#4A2E1B"  # चॉकलेटी ब्राउन कलर प्रीमियम लुक के लिए

#             MDLabel:
#                 id: welcome_label
#                 text: "Welcome, Foodie!"
#                 halign: "center"
#                 font_style: "Subtitle1"
#                 theme_text_color: "Secondary"

#             # मुख्य फॉर्म कार्ड (Premium Shadow & Rounded Corners)
#             MDCard:
#                 orientation: "vertical"
#                 size_hint_x: 0.95
#                 size_hint_y: None
#                 height: "460dp"
#                 pos_hint: {"center_x": .5}
#                 padding: "20dp"
#                 spacing: "15dp"
#                 radius: [24, ]
#                 elevation: 2
#                 md_bg_color: "#FFFFFF"

#                 MDLabel:
#                     text: "Place Your Delicious Order"
#                     bold: True
#                     font_style: "Subtitle1"
#                     theme_text_color: "Custom"
#                     text_color: "#D35400"
#                     halign: "center"

#                 # कस्टमर नेम फील्ड
#                 MDTextField:
#                     id: name_field
#                     hint_text: "Your Name"
#                     mode: "rectangle"
#                     icon_left: "account"

#                 MDRaisedButton:
#                     text: "Save Name"
#                     pos_hint: {"center_x": .5}
#                     md_bg_color: "#4A2E1B"
#                     on_release: app.save_name()

#                 # ड्रॉपडाउन फील्ड्स (Outlined Mode में ज़्यादा सुंदर लगते हैं)
#                 MDTextField:
#                     id: product_field
#                     hint_text: "Select Product"
#                     mode: "rectangle"
#                     readonly: True
#                     icon_left: "food-variant"
#                     on_focus: if self.focus: app.product_menu.open()

#                 MDTextField:
#                     id: weight_field
#                     hint_text: "Select Weight"
#                     mode: "rectangle"
#                     readonly: True
#                     icon_left: "weight"
#                     on_focus: if self.focus: app.weight_menu.open()

#                 MDTextField:
#                     id: packet_field
#                     hint_text: "How many Packets?"
#                     mode: "rectangle"
#                     readonly: True
#                     icon_left: "numeric"
#                     on_focus: if self.focus: app.packet_menu.open()

#                 MDFillRoundFlatButton:
#                     text: "＋ ADD ITEM TO CART"
#                     pos_hint: {"center_x": .5}
#                     md_bg_color: "#E67E22"
#                     font_style: "Button"
#                     size_hint_x: 0.8
#                     on_release: app.add_item()

#             # करंट आर्डर सेक्शन
#             MDCard:
#                 orientation: "vertical"
#                 size_hint_x: 0.95
#                 size_hint_y: None
#                 height: "180dp"
#                 pos_hint: {"center_x": .5}
#                 padding: "15dp"
#                 radius: [16, ]
#                 md_bg_color: "#F3EFE9"
#                 elevation: 0

#                 MDLabel:
#                     text: "🛒 Current Cart Items:"
#                     bold: True
#                     theme_text_color: "Custom"
#                     text_color: "#4A2E1B"

#                 ScrollView:
#                     MDLabel:
#                         id: order_label
#                         text: "Cart is empty"
#                         theme_text_color: "Secondary"
#                         size_hint_y: None
#                         height: self.texture_size[1]
#                         font_style: "Body2"

#             MDLabel:
#                 id: total_label
#                 text: "Total Packets: 0"
#                 halign: "center"
#                 bold: True
#                 font_style: "H6"
#                 theme_text_color: "Custom"
#                 text_color: "#27AE60"

#             # फाइनल सबमिट बटन
#             MDFillRoundFlatButton:
#                 text: "🚀 SUBMIT & SEND ORDER"
#                 pos_hint: {"center_x": .5}
#                 md_bg_color: "#27AE60"
#                 size_hint_x: 0.9
#                 font_style: "H6"
#                 on_release: app.submit_order()

#             Widget:
#                 size_hint_y: None
#                 height: "10dp"

#             MDLabel:
#                 text: "Made With ❤️ By\\nSharmila & Binod"
#                 halign: "center"
#                 font_style: "Caption"
#                 theme_text_color: "Secondary"
# """

# class GharKiRasoi(MDApp):

#     def build(self):
#         self.theme_cls.primary_palette = "Orange"
#         self.orders = []
#         self.screen = Builder.load_string(KV)

#         # ड्रॉपडाउन मेन्यूज़ को सुंदर और थोड़ा चौड़ा बनाया गया है
#         self.product_menu = MDDropdownMenu(
#             caller=self.screen.ids.product_field,
#             items=[
#                 {"text": "Banana Chips", "viewclass": "OneLineListItem", "on_release": lambda x="Banana Chips": self.set_product(x)},
#                 {"text": "Mangori", "viewclass": "OneLineListItem", "on_release": lambda x="Mangori": self.set_product(x)},
#                 {"text": "Adrak Powder", "viewclass": "OneLineListItem", "on_release": lambda x="Adrak Powder": self.set_product(x)},
#             ],
#             width_mult=4
#         )

#         self.weight_menu = MDDropdownMenu(
#             caller=self.screen.ids.weight_field,
#             items=[
#                 {"text": w, "viewclass": "OneLineListItem", "on_release": lambda x=w: self.set_weight(x)}
#                 for w in ["200g", "300g", "400g", "500g"]
#             ],
#             width_mult=3
#         )

#         self.packet_menu = MDDropdownMenu(
#             caller=self.screen.ids.packet_field,
#             items=[
#                 {"text": str(i), "viewclass": "OneLineListItem", "on_release": lambda x=str(i): self.set_packet(x)}
#                 for i in range(1, 11)
#             ],
#             width_mult=2
#         )

#         self.load_user()
#         return self.screen

#     def load_user(self):
#         try:
#             with open("user.json", "r") as f:
#                 name = json.load(f).get("name", "")
#                 if name:
#                     self.screen.ids.welcome_label.text = f"Welcome back, {name}! ✨"
#                     self.screen.ids.name_field.text = name
#         except:
#             pass

#     def save_name(self):
#         name = self.screen.ids.name_field.text.strip()
#         if not name:
#             return
#         with open("user.json", "w") as f:
#             json.dump({"name": name}, f, indent=4)
#         self.screen.ids.welcome_label.text = f"Welcome, {name}! ✨"
        
#         # नाम सेव होने का डायलॉग बॉक्स
#         MDDialog(title="Saved!", text=f"Name updated to '{name}'", size_hint=(0.8, None)).open()

#     def set_product(self, v):
#         self.screen.ids.product_field.text = v
#         self.product_menu.dismiss()

#     def set_weight(self, v):
#         self.screen.ids.weight_field.text = v
#         self.weight_menu.dismiss()

#     def set_packet(self, v):
#         self.screen.ids.packet_field.text = v
#         self.packet_menu.dismiss()

#     def add_item(self):
#         p = self.screen.ids.product_field.text
#         w = self.screen.ids.weight_field.text
#         pk = self.screen.ids.packet_field.text

#         if not (p and w and pk):
#             MDDialog(title="Error", text="Please select Product, Weight, and Packets first!").open()
#             return

#         self.orders.append({"product": p, "weight": w, "packets": pk})

#         if self.screen.ids.order_label.text == "Cart is empty":
#             self.screen.ids.order_label.text = ""

#         self.screen.ids.order_label.text += f"• {p} ({w}) — {pk} Packet(s)\n"
#         total = sum(int(x["packets"]) for x in self.orders)
#         self.screen.ids.total_label.text = f"Total Packets: {total}"
        
#         # फील्ड्स रीसेट करें ताकि अगला आइटम चुन सकें
#         self.screen.ids.product_field.text = ""
#         self.screen.ids.weight_field.text = ""
#         self.screen.ids.packet_field.text = ""

#     def submit_order(self):
#         name = self.screen.ids.name_field.text.strip()

#         if not name:
#             MDDialog(title="Missing Name", text="Please enter and save your name before submitting!").open()
#             return

#         if not self.orders:
#             MDDialog(title="Empty Cart", text="Please add at least one item to your cart!").open()
#             return

#         # 1. लोकल JSON फ़ाइल अपडेट करें
#         try:
#             with open("orders.json", "r") as f:
#                 data = json.load(f)
#         except:
#             data = []

#         data.append({
#             "customer": name,
#             "items": self.orders
#         })

#         with open("orders.json", "w") as f:
#             json.dump(data, f, indent=4)

#         # 2. व्हाट्सऐप के लिए सुंदर मैसेज तैयार करें
#         whatsapp_msg = f"*New Order Received from Ghar Ki Rasoi App!* 🎉\n\n"
#         whatsapp_msg += f"👤 *Customer Name:* {name}\n"
#         whatsapp_msg += f"📦 *Order Details:*\n"
        
#         for idx, item in enumerate(self.orders, 1):
#             whatsapp_msg += f"  {idx}. {item['product']} | {item['weight']} | {item['packets']} packet(s)\n"
            
#         total_p = sum(int(x["packets"]) for x in self.orders)
#         whatsapp_msg += f"\n🔢 *Total Packets:* {total_p}\n"
#         whatsapp_msg += f" Please prepare this order."

#         # यूआरएल इनकोडिंग ताकि व्हाट्सऐप इसे सही से समझ सके
#         encoded_msg = urllib.parse.quote(whatsapp_msg)
#         whatsapp_url = f"https://wa.me/{MUMMA_PHONE_NUMBER}?text={encoded_msg}"

#         # कार्ट साफ़ करें
#         self.orders = []
#         self.screen.ids.order_label.text = "Cart is empty"
#         self.screen.ids.total_label.text = "Total Packets: 0"

#         # व्हाट्सऐप पर मैसेज भेजें
#         webbrowser.open(whatsapp_url)

#         # सक्सेस डायलॉग
#         MDDialog(
#             title="Order Formed!",
#             text="Your order is compiled! Opening WhatsApp to notify Sharmila & Binod... Please click send on WhatsApp.",
#         ).open()

# if __name__ == "__main__":
#     GharKiRasoi().run()



















