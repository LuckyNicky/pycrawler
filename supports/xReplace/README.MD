#python开发的文件内容批量替换小工具

### 安装
>  sudo python setup.py install

### 使用帮助
>  ljd@08:07:37:replace$ replace --help
Usage: replace [options] target_path

    Options:
     --version             show program's version number and exit
     -h, --help            show this help message and exit
     --filter_filename=PATTERN
                        exclude files matching PATTERN
     --include_filename=PATTERN
                        only include files matching PATTERN(high priority)
    -s SOURCE_RE_STRING, --source=SOURCE_RE_STRING
                        source re pattern
    -t TARGET_STRING, --target=TARGET_STRING
                        target string
    -H                    include hidden file
    -i                    prompt before every replace


