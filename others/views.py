import os
import emoji
import datetime
from django.http import HttpResponse
from cbg_backup import settings
from .models import Problems, CbgTrackJsError
from unit.decoration import accept_token
from unit.utility import render_to_response, response_json


@accept_token('qiniu')
def bug_submit_page(request, response, render):
    """上报bug的页面"""
    return render_to_response(request, response, render, 'others/templates/bug_submit.html')


def upload_files(request, type='img'):
    """下载上传的文件
       现在只支持文件的上传
    """
    user_id = str(request.user.id or 0)  # 未登陆的分配0
    now = datetime.datetime.now()
    img_path_list = []
    for name, file in request.FILES.items():
        suffix = os.path.splitext(file.name)[-1].lower()
        if not suffix.startswith('.'):
            continue
        if suffix not in ('.jpg' , '.jpeg' , '.png' , '.gif' , '.bmp'):
            return False, '不支持的文件类型%s' % suffix
        # 创建文件夹
        base_dir = os.path.join(settings.UPLOAD_DIRS, 'user', user_id)
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        file_name = os.path.join(base_dir, now.strftime('%Y%M%d%H%M') + '-' + str(settings.redis3.incr('user_upload')) + suffix)
        img_path_list.append(os.path.join(settings.STATIC_URL, file_name))
        with open(file_name, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)
    return True, img_path_list


def submit_problems(request, response, render):
    """上传问题"""
    # 获取问题类型
    # todo emoji图形控制  xss攻击的防御  forms校验？
    submit_type = request.POST.get('submit_type', 'Bug')  # BUG, Introduce
    type = request.POST.get('type', '')
    title = request.POST.get('title', '')
    content = request.POST.get('content', '')
    img_list = request.POST.get('img_list', '')
    if all([submit_type, type, title, content]):
        return response_json(retcode='FAIL', msg="ErrorParams", description='错误的提交数据！')
    # if request.FILES:
    #     bol, res = upload_files(request)
    #     if not bol:
    #         return response_json(retcode='FAIL', msg="ImageUploadFail", description=res)
    #     img_url = ';'.join(res)
    if submit_type == 'Bug':
        Problems.objects.create(
            user_id=request.user.id,
            type=submit_type,
            subtype=type,
            title=title,
            detail=content,
            img_list=img_list,
        )
    return response_json(retcode='SUCC', msg="ProblemsSubmitSucc")


def track_js(request, response, render):
    """跟踪js的报错信息"""
    err_js = request.POST.get('err_js')
    line = request.POST.get('line')
    col = request.POST.get('col')
    err_msg = request.POST.get('err_msg')
    user_ip = request.META.get('REMOTE_ADDR', '')
    user_agent=request.META['HTTP_USER_AGENT'][:256]
    if user_ip and user_agent:
        CbgTrackJsError.objects.create(
            user_id=request.user.id if render['user_login'] else None,
            js_name=err_js,
            line=line,
            col=col,
            err_stack=err_msg,
            ip=user_ip,
            user_agent=user_agent,
        )
    return HttpResponse('ok')











