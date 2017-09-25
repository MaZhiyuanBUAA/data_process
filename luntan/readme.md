
v1
on文件转成txt文件，json2txt，规则如下：
#  通用规则：
#     //1.将开头的<>,【】,##,以及非法字符\u200b替换为空（该条论坛数据不适用）
#     //2.替换句尾地点信息"我在:2<地点>·<地点>"或者"2<地点>"为空(该条论坛数据不适用)
#     3.开头的标点替换为空
#  经过通用规则处理之后：
#  1.滤掉整个post-comment pair的情况：
#     a.post去重
#     //b.去掉开头的@xx，去掉不可见字符，如果post中不含中字或者句中含有@（该条论坛数据不适用）
#     c.post或这comment中含有"图片","照片","视频","配图","链接","展开全文"
#  2.comment的选择：
#     a.该post下出现多次的滤掉（广告）
#     b.通用规则处理后不含中字的滤掉
#     //c.含有@的滤掉（回复的post下某条comment）（该条论坛数据不适用）
#     d.满足条件的第一条
#
#第二步，txt文件处理，规则如下：
#   1.长度post长度>15或则<2,comment长度大于20或者<2，滤掉
#   2.post或comment中含有.com等域名，滤掉
#   //3.post或comment中含有罗马数字0-9，滤掉（论坛数据保留数字）
#   //4.含有中字和常见标点之外的，滤掉

v2
#1.把规则的抽象成两大类：过滤规则（只要包含相关字符就过滤掉，包含敏感词和正则两个过滤器），
#  替换规则（将句子中的相关字符替换为目标字符，正则）；可通过配置文件修改
#2.优化处理流程，先经过过滤器，再经过替换器
#3.增加动态敏感词过滤模块，避免敏感词库更新后从头处理数据
#4.保留网址、UID信息，并输出为json字符串