# Hệ thống hỏi đáp các chuyến bay

Hệ thống hỏi đáp các chuyến bay là đề tài hấp dẫn ứng dụng Xử lý ngôn ngữ tự nhiên để truy vấn dữ liệu và trả lời câu hỏi. Gửi lời cảm ơn đến anh Hoàng Lê Hải Thanh đã hỗ trợ em phần baseline của hệ thống bằng ngôn ngữ tiếng Anh và truy vấn với _WHICH_. Ở phần này, em sẽ cải tiến với ngôn ngữ tiếng Việt và hỗ trợ cho 4 loại câu hỏi _WHICH_, _HOWLONG_, _WHEN_, _YESNO_.

-   Co-Author: Doan Tran Cao Tri
-   University: Ho Chi Minh University of Technology
-   Id: 2010733
-   Contact: tri.doan218138@hcmut.edu.vn

## 1. Demo

```
máy_bay nào xuất_phát từ TP. Hồ_Chí_Minh và  lúc mấy giờ  ?
```

```
-------------Parsed structure-------------
(S[SEM=<WHQUERY((WHICH(f2) & FLIGHT(f2)),(SOURCE(CITY(NAME('HoChiMinh'))) & LEAVE(AT((WHEN(t3) & HOUR(t3))))))>]
  (NP[SEM=<(WHICH(f3) & FLIGHT(f3))>]
    (FLIGHT-CNP[SEM=<\f.FLIGHT(f)>, VAR=<f2>]
      (FLIGHT-N[SEM=<\f.FLIGHT(f)>, VAR=<f1>] máy_bay))
    (WHICH-QDET[SEM=<\x.WHICH(x)>] nào))
  (VP[SEM=<(SOURCE(CITY(NAME('HoChiMinh'))) & LEAVE(AT((WHEN(t2) & HOUR(t2)))))>]
    (VP[SEM=<SOURCE(CITY(NAME('HoChiMinh')))>, VAR=<LEAVE>]
      (V[SEM=<LEAVE>] xuất_phát)
      (PP[SEM=<SOURCE(CITY(NAME('HoChiMinh')))>]
        từ
        (CITY-CNP[SEM=<CITY(NAME('HoChiMinh'))>]
          (CITY-N[SEM=<CITY>, VAR=<c1>] TP.)
          (CITY-NAME[SEM=<NAME('HoChiMinh')>] Hồ_Chí_Minh))))
    và
    (PP[SEM=<AT((WHEN(t3) & HOUR(t3)))>]
      (P[SEM=<AT>] lúc)
      (NP[SEM=<(WHEN(t2) & HOUR(t2))>]
        (WHEN-QDET[SEM=<\t.WHEN(t)>] mấy)
        (HOUR-N[SEM=<HOUR>, VAR=<t1>] giờ)))))
```

```
-------------Parsed logical form-------------
WHQUERY((WHICH(f2) & FLIGHT(f2)) (SOURCE(CITY(NAME('HoChiMinh'))) & LEAVE(AT((WHEN(t3) & HOUR(t3))))))
```

```
-------------Procedure semantics-------------
(PRINT-ALL ?f2 (MÁY_BAY ?f2) (ATIME ?f2 ?al ?at) (DTIME ?f2 HCM t3) (RUN-TIME ?f2 HCM ?al ?rt))
(PRINT-ALL ?t3 (MÁY_BAY ?f2) (ATIME ?f2 ?al ?at) (DTIME ?f2 HCM t3) (RUN-TIME ?f2 HCM ?al ?rt))
```

```
-------------Retrieved result-------------
VN1 VJ3 VJ4 VJ2 VN5 VN3
1:00HR 2:00HR 1:00HR 1:30HR 0:45HR 2:00HR
```

## 2. Cấu trúc hệ thống

Cài đặt thư viện

```
pip install -r requirements.txt
```

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
$python3 main.py --rule_file_name=grammar.fcfg --question="Có máy bay nào xuất phát từ Hải Phòng không ?"
```

## 4. Database

```
    "ATIME VN1 HUE 11:00HR",
    "ATIME VJ1 HUE 13:30HR",
    "ATIME VN2 HCM 16:30HR",
    "ATIME VJ2 HN 11:00HR",
    "ATIME VN3 HN 6:30HR",
    "ATIME VJ3 HP 11:45HR",
    "ATIME VN4 ĐN 11:30HR",
    "ATIME VJ4 ĐN 9:30HR",
    "ATIME VN5 KH 17:45HR",
    "ATIME VJ5 KH 10:45HR",

    "DTIME VN1 HCMC 10:00HR",
    "DTIME VJ1 HN 12:30HR",
    "DTIME VN2 ĐN 15:30HR",
    "DTIME VJ2 ĐN 9:30HR",
    "DTIME VN3 HCM 4:30HR",
    "DTIME VJ3 HCMC 9:45HR",
    "DTIME VN4 HN 9:30HR",
    "DTIME VJ4 HCMC 8:30HR",
    "DTIME VN5 HCMC 17:00HR",
    "DTIME VJ5 HN 9:00",

    "RUN-TIME VN1 HCMC HUE 1:00HR",
    "RUN-TIME VJ3 HCM HP 2:00HR",
    "RUN-TIME VJ1 HN HUE 1:00HR",
    "RUN-TIME VN4 HN ĐN 2:00HR",
    "RUN-TIME VN2 ĐN HCM 1:00HR",
    "RUN-TIME VJ4 HCM ĐN 1:00HR",
    "RUN-TIME VJ2 HCMC HN 1:30HR",
    "RUN-TIME VN5 HCM KH 0:45HR",
    "RUN-TIME VN3 HCM HP 2:00HR",
    "RUN-TIME VJ5 HN KH 0:45HR",

    "MÁY_BAY VN1",
    "MÁY_BAY VN2",
    "MÁY_BAY VN3",
    "MÁY_BAY VN4",
    "MÁY_BAY VN5",
    "MÁY_BAY VJ1",
    "MÁY_BAY VJ2",
    "MÁY_BAY VJ3",
    "MÁY_BAY VJ4",
    "MÁY_BAY VJ5",
```
