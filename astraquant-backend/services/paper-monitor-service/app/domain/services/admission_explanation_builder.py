class AdmissionExplanationBuilder:
    def build(self, decision, reasons, warnings, suggestions): return {"decision":decision,"reject_reasons":reasons,"warnings":warnings,"suggestions":suggestions}
