# Hệ thống hỏi đáp sân bay

Cài đặt thư viện

```
pip install -r requirements.txt
```

## 2. Cấu trúc hệ thống

Gồm 4 files chính

-   [main.py](main.py) : File chạy chương trình.
-   [nlp_parser.py](nlp_parser.py) : Parser.
-   [nlp_data.py](nlp_data.py) : Load data.
-   [nlp_file.py](nlp_file.py) : Xử lý file.

files khác:

-   [grammar.fcfg](grammar.fcfg) : The free context grammar file.

## 3. Chạy mẫu

Use default arguments:

```sh
$python3 main.py
```

Use custom arguments:

```sh
$python3 main.py --question [question] --rule_file_name [rule_file_name]
```

Usage:

-   `--question` : The input question in English. Default: "_Máy bay nào đến thành phố Huế lúc 13:30HR ?_"
-   `--rule_file_name` : The context free grammar file (.fcfg). Default: _grammar.fcfg_

Ví dụ

```sh
$python3 main.py --rule_file_name=grammar.fcfg --question=1
```

## 4. Result
