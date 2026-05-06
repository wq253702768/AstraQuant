import csv, io, json
class AuditExportBuilder:
    def csv(self, rows):
        buf=io.StringIO(); writer=csv.DictWriter(buf, fieldnames=["event_type","resource_type","resource_id"]); writer.writeheader(); writer.writerows(rows); return buf.getvalue()
    def json(self, rows): return json.dumps(rows, ensure_ascii=False)
