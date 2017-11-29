
scrapy:
spider_china-10_1 : 抓取一级和二级对应name url
spider_china-10_2 : 抓取二级和三级对应name url
spider_china-10_info : 抓取三级对应品牌信息
(* spider_china-10_info_down : 抓取三级对应 下面几行的品牌信息（有问题，弃用，改成下面两个部分） *)
spider_china-10_info_down_url: 抓取三级对应下面几行品牌url
spider_china-10_info_down_info:抓取三级对应下面几行品牌详情

mongodb
1, content_test_j   一级和二级对应关系内容 有点问题，导出csv自己修改为正确的对应关系后导入为 content_tbl_rank_1and2
2, content_test_q   二级和三级对应关系内容 
3, content_test_info    三级和对应的品牌详情 不包括下面的几行
4, content_test_down_url    三级对应下面的几行品牌的url
5, content_test_down_info   三级对应下面几行品牌详情

(* 6, content_test_n       三级对应下面几行品牌详情（最一开始抓的，导出数据发现有问题，没有抓完，重新设计抓取程序，分为4和5两部分） *)
