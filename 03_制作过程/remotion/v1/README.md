# 豆包六段完整片 v1 工程

入口 `src/index.tsx` → `src/Film.tsx` → `src/components/Actions.tsx`，1080×1920、60fps、6780帧。原片保留原路径并在public/media复制；source SHA和7段剪辑范围见qc/final-edl.json。完整输入6条，语义顺序6→4→3→2→1→5；第1条分析切成两段。原速，最终113秒。

## 恢复与重新导出

本工程引用既有只读node_modules，实际版本见qc/runtime-versions.json；React/ReactDOM19.2.5、Remotion4.0.451、TypeScript6.0.3。该依赖路径失效时，按runtime-versions.json在本工程恢复相同版本。源码、字体、媒体、音效和选用付费组件副本均已落在本工程，不需要修改全局Fred库。

本机Node：`/Users/USER/.local/nodejs/node-v22.16.0-darwin-arm64/bin/node`。
在本工程目录运行：

```sh
node render.mjs full
/Users/USER/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 final_check.py
/Users/USER/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 audio_verify.py
node serve.mjs
```

最终播放入口：`http://127.0.0.1:4247`；也可直接打开02_最终输出内的MP4或播放.html。服务器仅绑定本机，不上传。若端口已被同一服务占用，复用它；不可任意终止别的进程。

`final_check.py`对本轮Remotion实际输出执行定点字幕修复、明确色彩范围转换，以及经波形测量确认的2048个48kHz样本延迟校正。换用其他编码器或版本时必须重新测量该延迟，不把此常数当通用规则。`render/film-picture-audio.mp4`是中间渲染，唯一交付以02_最终输出及最终SHA为准。

## 证据

- manifest.json：准确组件、参考图、源代码/调用点SHA、字幕时码与编排。
- 组件与来源调用表.md：各镜头动作与来源。
- qc/planning.json、implementation.json、library-keyframes.json：各层真实工具检查。
- qc/final：最终文件探测、完整解码、音频测量、逐秒采样及剪口10fps采样。
- 02_最终输出：唯一交付视频、字幕、首帧/收束候选和播放页。

正常速度连续看听未核实，不能将规划/实现/静态检查PASS写成整片声画终审PASS；05由PMO审查后释放。本期生成文件保留用于追溯与恢复，不自动清理原片或付费资产。
