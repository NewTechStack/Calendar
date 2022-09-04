from Controller.basic import check
from Object.utils import Utils

def email_to_address(cn, nextc):
    err = [True, {}, None]
    for arg in [cn.pr]:
        copy, ret = Utils.json_email_replace_proxy(
            arg,
            [
                {
                    "func": cn.private["sso"].user_by_email,
                    "res": [1, 'id']
                }
            ]
        )
        arg = {"original": copy, "computed": ret}
    return cn.call_next(nextc, err)
