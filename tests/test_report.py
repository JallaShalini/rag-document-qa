from app.schemas.report_schema import ReportResponse


def test_report_endpoint_returns_expected_schema(client):
    response = client.get('/report')

    assert response.status_code == 200
    body = response.json()
    report = ReportResponse(**body)

    assert report.system_status == 'healthy'
    assert report.context_precision == 0.90
    assert report.faithfulness == 0.85
