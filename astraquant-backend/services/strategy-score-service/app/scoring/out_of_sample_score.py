class OutOfSampleScore:
    def calculate(self, metrics: dict) -> tuple[float, list[str]]:
        if not metrics.get("out_of_sample"):
            return 50, ["缺少样本外验证，存在过拟合风险"]
        return 80, []
