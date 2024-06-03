# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import json
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


class OutputPipeline:
    filename = None
    canvas = None
    width, height = None, None
    y_position = None
    canvas = canvas
    output_format = 'json'

    def open_spider(self, spider):
        self.items = []
        self.filename = 'items.pdf'
        self.canvas = canvas.Canvas(self.filename, pagesize=letter)
        self.width, self.height = letter
        self.y_position = self.height - 40
        self.canvas.setFont("Helvetica", 12)
        self.output_format = spider.crawler.settings.get('OUTPUT_FORMAT', 'json')

    def close_spider(self, spider):
        if self.output_format == 'json':
            self.export_to_json()
        elif self.output_format == 'csv':
            self.export_to_csv()
        elif self.output_format == 'pdf':
            self.export_to_pdf()

    def process_item(self, item, spider):
        self.items.append(dict(item))
        return item

    def export_to_json(self):
        with open('items.json', 'w') as f:
            json.dump(self.items, f, indent=4)

    def export_to_csv(self):
        keys = self.items[0].keys() if self.items else []
        with open('items.csv', 'w', newline='') as f:
            dict_writer = csv.DictWriter(f, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(self.items)

    def export_to_pdf(self):
        for item in self.items:
            if self.y_position < 140:
                self.canvas.showPage()
                self.canvas.setFont("Helvetica", 12)
                self.y_position = self.height - 40

            image = item.get('images', 'N/A').get('image700', 'N/A').get('url', "N/A")

            interaction_stats = item.get('interaction_statistics', {})
            interaction_stats_str = json.dumps(interaction_stats, indent=2)

            self.canvas.drawString(30, self.y_position, f"ID: {item.get('id', 'N/A')}")
            self.canvas.drawString(30, self.y_position - 15, f"Title: {item.get('title', 'N/A')}")
            self.canvas.drawString(30, self.y_position - 30, f"Image: {image}")
            self.canvas.drawString(30, self.y_position - 45, f"Interaction Statistics: {interaction_stats_str}")
            self.canvas.drawString(30, self.y_position - 60, f"Created at: {item.get('created_at', 'N/A')}")

            self.canvas.line(30, self.y_position - 80, self.width - 30, self.y_position - 80)

            self.y_position -= 100

        self.canvas.save()
