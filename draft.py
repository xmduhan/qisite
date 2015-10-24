#!/usr/bin/env python
# encoding: utf-8

qi设计上存在的问题：
1、缺少业务逻辑层，只有view和model层，导致过多的逻辑都遗留在view层。
2、id应用上不应使用签名方式，导致了业务逻辑的复杂。
3、url需要进行同意规划,并且应考虑采用类restful方式。
4、最好用jinja模板体系替换django原声模板体系

