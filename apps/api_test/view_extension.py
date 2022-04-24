from apps.api_test import api_request
from apps.api_test.models import Case, CaseArgument, CaseRunRecord, CaseApiRunRecord
from utils.dictor import dictor


def run_case(case_id, request):
    case = Case.objects.get(pk=case_id)
    case_arguments = CaseArgument.objects.filter(case=case)
    case_record = CaseRunRecord.objects.create(case=case)

    global_arguments = {}
    # 添加用例参数
    for case_argument in case_arguments:
        global_arguments[case_argument.name] = case_argument.value

    # 运行API及添加API参数
    api_models = case.apis.all()
    for api_model in api_models:
        response = api_request.request(api_model, global_arguments)
        CaseApiRunRecord.objects.create(
            url=response.url,
            http_method=response.request.method,
            data=response.request.body,
            headers=response.request.headers,
            user=request.user,
            return_code=response.status_code,
            return_content=response.text,
            api=api_model,
            case_record=case_record
        )

        api_arguments = api_model.arguments.all()
        if api_arguments:
            for api_argument in api_arguments:
                dictor_data = {}
                if api_argument.origin == 'HEAD':
                    dictor_data = response.headers
                elif api_argument.origin == 'COOKIE':
                    dictor_data = response.cookies
                elif api_argument.origin == 'BODY':
                    dictor_data = response.json()

                argument_value = dictor(dictor_data, api_argument.format)
                global_arguments[api_argument.name] = argument_value

    return case_record
