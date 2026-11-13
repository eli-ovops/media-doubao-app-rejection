# v2 定向精修工程

依据本content_id的PMO-v1审查与定向精修.md，只改两段：新闻384–650帧（6.4–10.85秒，右端不含），片尾6726–6779帧（112.1–113秒）。共重渲321帧。时长、台词、SRT及其余场景不变，v1完整保留。

源码src/Film.tsx仅Opening和Ending变化，差异见qc/source-diff.patch。v2 public/node_modules为同content_id的v1只读依赖；恢复时须保留v1。精确源组件沿manifest.json记录的v1原件与T09i/T04f引用，未引入新组件或重新设计其他场景。

在本目录，以既有Node22运行`node render.mjs`，仅渲染新闻和片尾；再以带Pillow的bundled Python运行`assemble.py`。组装输入为最终已对齐v1，不是v1中间渲染。音轨直接流复制，无二次响度处理或延迟裁剪。视频统一1/60时基后局部替换；完整编码一代H.264，因此未改场景不是压缩字节恒等，但没有重新渲染它们。

qc/delivery.json包含最终MP4与SHA；probe/decode、两版音频PCM hash、逐帧SSIM、49张报道运动采样、24张片尾运动采样、原尺寸单图为本轮检查。全片正常速度连续声画、直接听音仍UNKNOWN，不能把本轮局部图审与技术检查记作05终审通过。
