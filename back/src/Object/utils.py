import re
import json

class Utils:


    def json_email_replace_proxy(data, modifiers = []):
        copy = json.loads(json.dumps(data))
        result = Utils.json_email_replace(data, modifiers)
        return copy, result

    def json_email_replace(data, modifiers = []):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if isinstance(data, str) and (re.fullmatch(regex, data)):
            done1 = True
            temp_json1 = data
            for modifier in modifiers:
                temp_json1 = modifier['func'](temp_json1)
                temp_json2 = temp_json1
                done2 = True
                for i in modifier['res']:
                    try:
                        temp_json2 = temp_json2[i]
                    except:
                        done2 = False
                        break
                if not done2:
                    done1 = False
                    break
                temp_json1 = temp_json2
            if done1:
                data = temp_json1
        elif isinstance(data, list):
            for idx, elem in enumerate(data):
                if any(isinstance(elem, type) for type in [dict, list, str]):
                    data[idx] = Utils.json_email_replace(elem, modifiers)
        elif isinstance(data, dict):
            for elem in data:
                if any(isinstance(data[elem], type) for type in [dict, list, str]):
                    data[elem] = Utils.json_email_replace(data[elem], modifiers)
        return data

if __name__ == '__main__':
    def test_func(string):
        return f"edited_{string}"

    ret = Utils.json_email_replace_proxy(
        {
            "test@test.fr": 1,
            "test": ["test2@test.fr"]
        },
        [
            {
                "func": test_func,
                "res": []
            }
        ]
    )
    print(ret)
