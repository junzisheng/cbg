import os


def get_cbg_path():
    """获取项目的路径"""
    current_dir = os.path.dirname(__file__)
    while 1:
        if os.path.basename(current_dir) == 'operations':
            break
        current_dir = os.path.dirname(current_dir)
    return os.path.dirname(current_dir)

if __name__ == '__main__':
    print(get_cbg_path())

