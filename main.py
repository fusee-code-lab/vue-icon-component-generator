import click
import os
from fontTools.ttLib import TTFont
from pathlib import Path

# TODO 生成 css fontfamily
# TODO 检测文件是否为空
templatePath = str(Path(__file__).parent.joinpath("./icon.vue.template"))

def to_abs_path(path: str) -> str:
    abs_path: str = ""
    if os.path.isabs(path):
        abs_path = path
    else:
        abs_path = os.path.abspath(path)
    return abs_path


def check_ttf_path(path: str) -> bool:
    abs_path = to_abs_path(path)

    if not os.path.isfile(path):
        return False

    return True


def generate(path: str, target_dir: str):
    abs_path = to_abs_path(path)
    target_dir = to_abs_path(target_dir)
    font_name = Path(abs_path).stem

    with open(templatePath, 'r') as temp:
        content: str = temp.read()

        with TTFont(abs_path) as font:
            cmap: dict[str, int] = font.getBestCmap()
            for (code, name) in cmap.items():
                eachContent = content
                uni_code = chr(code).encode(
                    'raw_unicode_escape').decode("utf-8").replace("\\u", "\\")

                class_name = "{font}-{name}".format(font=font_name, name=name)
                component_name = "{font}-icon-{name}".format(
                    font=font_name, name=name)
                file_name = "{name}Icon.vue".format(name=name.capitalize())

                target_file = os.path.join(target_dir, file_name)

                eachContent = eachContent.replace("$FONT_NAME$", font_name)
                eachContent = eachContent.replace("$CLASS$", class_name)
                eachContent = eachContent.replace("$NAME$", component_name)
                eachContent = eachContent.replace("$UNICODE$", uni_code)

                with open(target_file, 'w') as component_file:
                    component_file.write(eachContent)


@click.command()
@click.option("--outpath", default="./", help="目标路径, 默认为当前路径 (支持相对路径与绝对路径)")
@click.option("--ttf", prompt="ttf 文件路径", help="ttf 文件路径 (支持相对路径与绝对路径)")
def main(outpath: str, ttf: str):
    """基于 ttf 文件生成 vue3 图标组件"""

    if not check_ttf_path(ttf):
        click.echo("无法找到指定文件 {path}".format(path=ttf))
        return
    else:
        click.echo("开始生成 {path}".format(path=ttf))
        if not os.path.exists(outpath):
            Path(outpath).mkdir(parents=True)
        generate(path=ttf, target_dir=outpath)


if __name__ == '__main__':
    main()
