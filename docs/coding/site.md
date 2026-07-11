---
title: 建站记录
description: suyunax-site 的 Zensical 配置、本地预览和部署记录
tags:
  - 建站
  - 项目
---

# 建站记录

这个网站使用 Zensical 构建，并沿用与 Material for MkDocs 兼容的 Markdown、导航和自定义样式。Zensical 的 Modern 主题负责页面呈现，内容仍然保存在轻便、易维护的 Markdown 文件中。

## 当前结构

```text
docs/
  index.md
  archive.md
  about.md
  learning/
  coding/
  footprints/
  essays/
  javascripts/
  stylesheets/
mkdocs.yml
requirements.txt
```

## 本地预览

```bash
.venv/bin/zensical serve
```

运行后可以在浏览器中打开本地地址预览。

## 生成站点

```bash
.venv/bin/zensical build --clean
```

GitHub Pages 部署也使用相同的构建命令，生成结果写入 `site/`。

## 发布前检查

本地构建后，可以检查生成页面中的站内链接、图片路径和标题锚点：

```bash
.venv/bin/zensical build --clean
.venv/bin/python scripts/check_site_links.py site
```

GitHub Actions 会执行同样的检查。只要发现页面链接、资源路径或锚点失效，就会停止部署并显示具体来源。

## 旅行照片处理

原始旅行照片不直接放入 `docs/`。先使用处理脚本清除 EXIF 信息、纠正拍摄方向、限制最长边，并生成网页使用的 WebP：

```bash
.venv/bin/python scripts/process_travel_images.py \
  ~/Pictures/trip-example \
  --output-dir docs/assets/images/footprints/trip-example
```

默认最长边为 1920 像素、WebP 质量为 84。可以使用 `--max-edge` 和 `--quality` 调整。原始照片不会被修改。

## 后续计划

- 根据内容增长逐步完善文章分类和推荐阅读。
- 有稳定更新频率后再加入 RSS。
- 确定评论服务后加入文章讨论区。
- 补充网站性能与无障碍检查。

## 已启用的能力

- Zensical Modern 主题和深浅色切换。
- 全文搜索、搜索建议和关键词高亮。
- 文章标签、代码复制、注释和内容标签页。
- MathJax 数学公式渲染。
- GLightbox 图片放大浏览。
- GitHub 源码查看、在线编辑和自动部署。
