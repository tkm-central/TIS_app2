import json

import requests
from django import forms
from django.conf import settings

DEFAULT_AMAZON_ML_ENDPOINT="https://realtime.machinelearning.us-east-1.amazonaws.com"

EMP_LENGTH_CHOICES = (
    (0.0, "無し"),
    (0.5, "1年未満"),
    (1.0, "満1年"),
    (2.0, "満2年"),
    (3.0, "満3年"),
    (4.0, "満4年"),
    (5.0, "満5年"),
    (6.0, "満6年"),
    (7.0, "満7年"),
    (8.0, "満8年"),
    (9.0, "満9年"),
    (10.0, "10年以上"),
)

HOME_OWNERSHIP_CHOICES = (
    ("RENT", "賃貸"),
    ("OWN", "持ち家"),
    ("MORTGAGE", "持ち家(抵当)"),
    ("OTHER", "その他"),
)

GRADE_CHOICES = {
    ("A", "A"),
    ("B", "B"),
    ("C", "C"),
    ("D", "D"),
    ("E", "E"),
    ("F", "F"),
    ("G", "G"),
}


class ExaminationForm(forms.Form):
    home_ownership = forms.ChoiceField(
        label="自宅の所有状況",
        choices=HOME_OWNERSHIP_CHOICES,
        required=True,
        widget=forms.Select()
    )
    int_rate = forms.DecimalField(
        label="ローン金利(％)",
        min_value=0,
        max_value=100,
        max_digits=4,
        decimal_places=2,
        required=True,
        widget=forms.NumberInput()
    )
    grade = forms.ChoiceField(
        label="グレード",
        choices=GRADE_CHOICES,
        required=True,
        widget=forms.Select()
    )
    mort_acc = forms.DecimalField(
        label="mort_acc",
        min_value=0,
        max_value=37,
        required=True,
        widget=forms.NumberInput()
    )


    def predict_loan_status(self):
        model_id = getattr(settings, "AMAZON_ML_MODEL_ID")
        amazon_ml_endpoint = getattr(settings, "AMAZON_ML_ENDPOINT", DEFAULT_AMAZON_ML_ENDPOINT)
        api_gateway_endpoint = getattr(settings, "API_GATEWAY_ENDPOINT")
        payload = {
            "MLModelId": model_id,
            "PredictEndpoint": amazon_ml_endpoint,
            "Record": {
                "home_ownership": self.cleaned_data['home_ownership'],
                "int_rate": str(self.cleaned_data['int_rate']),
                "grade": self.cleaned_data['grade'],
                "mort_acc": str(self.cleaned_data['mort_acc'])
            }
        }
        response = requests.post(api_gateway_endpoint, data=json.dumps(payload))
        return response.json()
